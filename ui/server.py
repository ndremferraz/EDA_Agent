"""Web UI for the KiCad agent.

    .venv/bin/python ui/server.py            # -> http://127.0.0.1:8765

Start a run from a free-form request or a benchmark task, watch its tool calls
live, and preview the schematic as the agent draws it. Past runs (ui/runs/ and
eval/output/) can be browsed too.
"""

import argparse
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import keyring
import uvicorn
from openai import AsyncOpenAI, AuthenticationError
from sse_starlette.sse import EventSourceResponse
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse, JSONResponse, Response
from starlette.routing import Route

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
import agent  # noqa: E402
from eval import tasks as evaltasks  # noqa: E402

UI_RUNS = HERE / "runs"
ROOTS = [UI_RUNS, evaltasks.OUTPUT_ROOT]


def _inside(path, root):
    return Path(path).is_relative_to(root)


def _kicad_env_defaults():
    """agent.run_agent passes KICAD_PYTHON and PYTHONPATH to the MCP server and
    needs both set; fill them in for the usual setups when the shell has not."""
    venv_python = REPO / ".venv" / "bin" / "python"
    os.environ.setdefault("KICAD_PYTHON", str(venv_python if venv_python.exists() else sys.executable))
    if "PYTHONPATH" not in os.environ:
        import importlib.util
        spec = importlib.util.find_spec("pcbnew")
        os.environ["PYTHONPATH"] = str(Path(spec.origin).parent) if spec and spec.origin else ""


_kicad_env_defaults()
TASKS_FILE = REPO / "eval" / "tasks.jsonl"
# Tools that change the schematic; the preview is refreshed after these.
EDIT_TOOL = re.compile(r"add|connect|place|move|delete|remove|edit|create|wire|label|annotate|update|set_")


def load_tasks():
    if not TASKS_FILE.exists():
        return {}
    return {t["id"]: t for t in map(json.loads, TASKS_FILE.read_text().splitlines()) if t}


class LiveRun:
    """A run started from this server; keeps every event for late subscribers."""

    def __init__(self, rid, run_dir, question, model, max_steps, task_id=None, approach="default"):
        self.rid, self.run_dir = rid, run_dir
        self.summary = {"id": rid, "question": question, "model": model, "max_steps": max_steps,
                        "task_id": task_id, "approach": approach,
                        "started": time.time(), "status": "running"}
        self.events, self.subscribers, self.task = [], set(), None

    def emit(self, kind, data):
        ev = {"kind": kind, "data": data, "t": round(time.time() - self.summary["started"], 2)}
        if kind == "tool_call":
            ev["schematic_changed"] = bool(EDIT_TOOL.search(data.get("name", "")))
        self.events.append(ev)
        for q in list(self.subscribers):
            q.put_nowait(ev)

    def snapshot(self):
        calls = [e["data"] for e in self.events if e["kind"] == "tool_call"]
        models = [e["data"] for e in self.events if e["kind"] == "model_call"]
        return {**self.summary, "output_dir": str(self.run_dir), "answer": "", "stop_reason": None,
                "turns": len(models), "tool_calls": calls, "model_calls": models,
                "events": list(self.events),
                "input_tokens": sum(m["input_tokens"] for m in models),
                "cached_input_tokens": sum(m["cached_input_tokens"] for m in models),
                "output_tokens": sum(m["output_tokens"] for m in models),
                "seconds": round(time.time() - self.summary["started"], 2),
                "schematic": str(s) if (s := agent.find_schematic(self.run_dir)) else None}


LIVE: dict[str, LiveRun] = {}


def rid_for(path):
    return str(Path(path).resolve().relative_to(REPO))


def run_dir_for(rid):
    p = (REPO / rid).resolve()
    if not any(_inside(p, r.resolve()) for r in ROOTS) or not p.is_dir():
        raise HTTPException(404, "no such run")
    return p


def read_run(run_dir):
    f = run_dir / "_run.json"
    return json.loads(f.read_text()) if f.exists() else None


# --------------------------------------------------------------------------
# API
# --------------------------------------------------------------------------

async def list_runs(request):
    out = {}
    for root in ROOTS:
        for f in root.glob("**/_run.json"):
            try:
                r = json.loads(f.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            rid = rid_for(f.parent)
            out[rid] = {"id": rid, "question": r.get("question", ""), "task_id": r.get("task_id"),
                        "status": r.get("stop_reason") or "unknown", "model": r.get("model"),
                        "turns": r.get("turns"), "tool_calls": len(r.get("tool_calls", [])),
                        "seconds": r.get("seconds"), "started": f.stat().st_mtime - (r.get("seconds") or 0),
                        "source": "ui" if _inside(f.parent, UI_RUNS) else "eval"}
    for rid, live in LIVE.items():
        if live.summary["status"] == "running":
            out[rid] = {**live.summary, "tool_calls": sum(e["kind"] == "tool_call" for e in live.events),
                        "source": "ui" if _inside(live.run_dir, UI_RUNS) else "eval"}
    return JSONResponse(sorted(out.values(), key=lambda r: -(r.get("started") or 0)))


async def list_tasks(request):
    return JSONResponse([{"id": t["id"], "type": t["type"], "question": t["question"]}
                         for t in load_tasks().values()])


async def get_run(request):
    rid = request.path_params["rid"]
    live = LIVE.get(rid)
    if live and live.summary["status"] == "running":
        return JSONResponse(live.snapshot())
    run_dir = run_dir_for(rid)
    r = read_run(run_dir)
    if r is None:
        raise HTTPException(404, "run has no _run.json")
    r["id"], r["status"] = rid, r.get("stop_reason")
    return JSONResponse(r)


async def start_run(request):
    body = await json_body(request)
    if not key_status()["configured"]:
        raise HTTPException(400, "No OpenAI API key set. Add one under API key in the sidebar.")
    model = (body.get("model") or agent.MODEL).strip()
    max_steps = int(body.get("max_steps") or agent.MAX_STEPS)
    approach = body.get("approach", "default")
    if approach not in ("default", "react", "plan-and-replan"):
        raise HTTPException(400, "Approach must be default, react, or plan-and-replan.")
    task_id = body.get("task_id")
    if task_id:
        task = load_tasks().get(task_id)
        if not task:
            raise HTTPException(400, f"unknown task {task_id}")
        n = 0
        while (evaltasks.OUTPUT_ROOT / task_id / f"run{n}").exists():
            n += 1
        run_dir = evaltasks.OUTPUT_ROOT / task_id / f"run{n}"
        try:
            question = evaltasks.prepare(task, run_dir)
        except FileNotFoundError as exc:
            raise HTTPException(400, str(exc))
    else:
        question = (body.get("question") or "").strip()
        if not question:
            raise HTTPException(400, "empty request")
        slug = re.sub(r"[^a-z0-9]+", "-", question.lower())[:40].strip("-") or "run"
        run_dir = UI_RUNS / f"{datetime.now():%Y%m%d-%H%M%S}-{slug}"
        run_dir.mkdir(parents=True)
    rid = rid_for(run_dir)
    live = LiveRun(rid, run_dir.resolve(), question, model, max_steps, task_id, approach=approach)
    LIVE[rid] = live
    live.task = asyncio.create_task(_execute(live, task if task_id else None))
    return JSONResponse({"id": rid})


async def _execute(live, task):
    kw = dict(model=live.summary["model"], max_steps=live.summary["max_steps"],
              approach=live.summary["approach"], on_event=live.emit)
    try:
        result = await agent.run_agent(live.summary["question"], live.run_dir, **kw)
    except asyncio.CancelledError:
        result = live.snapshot()
        result.update(stop_reason="stopped", answer="(stopped from the UI)")
    except Exception as exc:  # agent.run_agent lets errors through
        while isinstance(exc, BaseExceptionGroup) and len(exc.exceptions) == 1:
            exc = exc.exceptions[0]  # stdio_client wraps errors in a TaskGroup
        result = live.snapshot()
        result.update(stop_reason="error", error=f"{type(exc).__name__}: {exc}")
    if task:
        result["task_id"] = task["id"]
    result["approach"] = live.summary["approach"]
    result["events"] = live.events
    (live.run_dir / "_run.json").write_text(json.dumps(result, indent=1, default=str))
    live.summary["status"] = result.get("stop_reason") or "error"
    live.emit("done", {"stop_reason": result.get("stop_reason"), "error": result.get("error")})


async def stop_run(request):
    await json_body(request)
    live = LIVE.get(request.path_params["rid"])
    if not live or live.summary["status"] != "running":
        raise HTTPException(409, "run is not active")
    live.task.cancel()
    return JSONResponse({"ok": True})


async def run_events(request):
    live = LIVE.get(request.path_params["rid"])
    if not live:
        raise HTTPException(404, "run is not live")

    async def gen():
        q = asyncio.Queue()
        backlog = list(live.events)
        live.subscribers.add(q)
        try:
            for ev in backlog:
                yield {"data": json.dumps(ev, default=str)}
            if live.summary["status"] != "running":
                return
            while True:
                ev = await q.get()
                yield {"data": json.dumps(ev, default=str)}
                if ev["kind"] == "done":
                    return
        finally:
            live.subscribers.discard(q)

    return EventSourceResponse(gen(), ping=15)


async def schematic_svg(request):
    run_dir = run_dir_for(request.path_params["rid"])
    sch = agent.find_schematic(run_dir)
    if not sch:
        raise HTTPException(404, "no schematic yet")
    cache = run_dir / "_preview"
    svg = cache / (sch.stem + ".svg")
    if not svg.exists() or svg.stat().st_mtime < sch.stat().st_mtime:
        cache.mkdir(exist_ok=True)
        proc = await asyncio.create_subprocess_exec(
            "kicad-cli", "sch", "export", "svg", "--exclude-drawing-sheet", "-o", str(cache), str(sch),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = await proc.communicate()
        if proc.returncode != 0 or not svg.exists():
            raise HTTPException(500, out.decode(errors="replace")[-2000:])
    return FileResponse(svg, media_type="image/svg+xml", headers={"Cache-Control": "no-store"})


async def run_files(request):
    run_dir = run_dir_for(request.path_params["rid"])
    files = [{"path": str(p.relative_to(run_dir)), "size": p.stat().st_size}
             for p in sorted(run_dir.rglob("*")) if p.is_file() and "_preview" not in p.parts]
    return JSONResponse(files)


async def run_file(request):
    run_dir = run_dir_for(request.path_params["rid"])
    p = (run_dir / request.query_params.get("path", "")).resolve()
    if not _inside(p, run_dir) or not p.is_file():
        raise HTTPException(404, "no such file")
    return FileResponse(p, filename=p.name, media_type="text/plain; charset=utf-8"
                        if request.query_params.get("view") else None)


async def delete_run(request):
    await json_body(request)
    rid = request.path_params["rid"]
    if rid in LIVE and LIVE[rid].summary["status"] == "running":
        raise HTTPException(409, "stop the run first")
    run_dir = run_dir_for(rid)
    shutil.rmtree(run_dir)
    LIVE.pop(rid, None)
    return JSONResponse({"ok": True})


async def config(request):
    return JSONResponse({"model": agent.MODEL, "max_steps": agent.MAX_STEPS,
                         "kicad_cli": bool(shutil.which("kicad-cli")),
                         "mcp_server": agent.MCP_SERVER.is_file()})


# --------------------------------------------------------------------------
# OpenAI API key (stored in the keyring entry agent._api_key() reads)
# --------------------------------------------------------------------------

KEYRING = ("KiCAD_Agent", "OPENAI_API_KEY")


def _keyring_key():
    try:
        return keyring.get_password(*KEYRING)
    except Exception:
        return None


def key_status():
    # agent._api_key() prefers the environment variable over the keyring.
    env, stored = os.environ.get("OPENAI_API_KEY"), _keyring_key()
    key = env or stored
    return {"configured": bool(key),
            "source": "environment" if env else "keyring" if stored else None,
            "hint": f"{key[:3]}…{key[-4:]}" if key and len(key) > 10 else None,
            "keyring_ok": _keyring_backend_ok()}


def _keyring_backend_ok():
    try:
        return keyring.get_keyring().priority > 0
    except Exception:
        return False


async def get_key(request):
    return JSONResponse(key_status())


async def set_key(request):
    key = ((await json_body(request)).get("key") or "").strip()
    if not key:
        raise HTTPException(400, "empty key")
    try:  # cheap check: listing models costs no tokens
        await AsyncOpenAI(api_key=key, max_retries=1, timeout=20).models.list()
    except AuthenticationError:
        raise HTTPException(400, "OpenAI rejected this key")
    except Exception as exc:
        raise HTTPException(502, f"Could not reach OpenAI to check the key: {exc}")
    try:
        keyring.set_password(*KEYRING, key)
    except Exception as exc:
        raise HTTPException(500, f"Could not save to the system keyring: {exc}")
    # The environment variable would win over the keyring; make the new key take effect now.
    if os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = key
    return JSONResponse(key_status())


async def delete_key(request):
    await json_body(request)
    try:
        if _keyring_key():
            keyring.delete_password(*KEYRING)
    except Exception as exc:
        raise HTTPException(500, f"Could not remove the key from the keyring: {exc}")
    return JSONResponse(key_status())


async def json_body(request):
    # Requiring a JSON content type makes browsers preflight cross-site requests,
    # which this server never approves, so other web pages cannot call it.
    if request.headers.get("content-type", "").split(";")[0].strip() != "application/json":
        raise HTTPException(415, "expected application/json")
    try:
        return await request.json()
    except ValueError:
        return {}


async def index(request):
    return FileResponse(HERE / "index.html", headers={"Cache-Control": "no-store"})


app = Starlette(routes=[
    Route("/", index),
    Route("/api/config", config),
    Route("/api/tasks", list_tasks),
    Route("/api/key", get_key, methods=["GET"]),
    Route("/api/key", set_key, methods=["POST"]),
    Route("/api/key", delete_key, methods=["DELETE"]),
    Route("/api/runs", list_runs, methods=["GET"]),
    Route("/api/runs", start_run, methods=["POST"]),
    Route("/api/run/{rid:path}/events", run_events),
    Route("/api/run/{rid:path}/stop", stop_run, methods=["POST"]),
    Route("/api/run/{rid:path}/schematic.svg", schematic_svg),
    Route("/api/run/{rid:path}/files", run_files),
    Route("/api/run/{rid:path}/file", run_file),
    Route("/api/run/{rid:path}", get_run, methods=["GET"]),
    Route("/api/run/{rid:path}", delete_run, methods=["DELETE"]),
])


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    print(f"KiCad agent UI on http://{a.host}:{a.port}")
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")
