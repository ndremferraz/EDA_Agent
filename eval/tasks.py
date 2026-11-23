import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

from agent import run_agent

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

MCP_SERVER = REPO / "KiCAD-MCP-Server" / "dist" / "index.js"

DEFAULT_BENCHMARK = REPO.parent / "KiCAD_benchmark"
OUTPUT_ROOT = HERE / "output"

MODEL = "gpt-6.1-terra"
MAX_STEPS = 100
TIMEOUT_S = 1800

BUILD_PREAMBLE = ("Create a new KiCad project named {name} in the project directory and "
                  "draw its schematic for the following request.\n\n")


def prepare(task, run_dir, benchmark=DEFAULT_BENCHMARK):

    run_dir = Path(run_dir).resolve()
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)

    for rel, content in task.get("setup_files", {}).items():
        (run_dir / rel).parent.mkdir(parents=True, exist_ok=True)
        (run_dir / rel).write_text(content)

    question = task["question"]

    if task["type"] == "build":

        if not (Path(benchmark) / "data").is_dir():
            raise FileNotFoundError(
                f"KiCAD_benchmark not found at {benchmark}; clone it next to "
                "EDA_Agent or pass --benchmark / benchmark=")

        deps = Path(benchmark) / Path(task["instructions"]).parent / "OUTPUT"

        if deps.is_dir():
            shutil.copytree(deps, run_dir, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns(".gitkeep"))
            
        question = BUILD_PREAMBLE.format(name=task["id"]) + question

    return question


async def run_task(task, run_dir, benchmark=DEFAULT_BENCHMARK, **kw):

    question = prepare(task, run_dir, benchmark)
    result = await run_agent(question, run_dir, **kw)

    result["task_id"] = task["id"]

    with open(Path(run_dir) / "_run.json", "w") as f:
        json.dump(result, f, indent=1, default=str)

    return result


def main():

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("task_id")
    ap.add_argument("--tasks", type=Path, default=HERE / "tasks.jsonl")
    ap.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    ap.add_argument("--run", type=int, default=0)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--max-steps", type=int, default=MAX_STEPS)
    a = ap.parse_args()

    tasks = {t["id"]: t for t in map(json.loads, a.tasks.read_text().splitlines()) if t}
    run_dir = OUTPUT_ROOT / a.task_id / f"run{a.run}"

    r = asyncio.run(run_task(tasks[a.task_id], run_dir, a.benchmark,
                             model=a.model, max_steps=a.max_steps))

    
    print(json.dumps({k: r[k] for k in ("task_id", "stop_reason", "error", "turns", "input_tokens",
                                         "cached_input_tokens", "output_tokens", "seconds", "schematic")}, indent=1))
    print(f"tool calls: {len(r['tool_calls'])} "
          f"({sum(1 for c in r['tool_calls'] if c.get('refused'))} refused)")
    print("\n" + (r["answer"] or "")[:1500])


if __name__ == "__main__":
    sys.exit(main())