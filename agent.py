from pathlib import Path
import asyncio
import os 
import time
import keyring
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI
from tools import ToolRunner


HERE = Path(__file__).resolve().parent
REPO = HERE
MCP_SERVER = REPO / "KiCAD-MCP-Server" / "dist" / "index.js"

MODEL = "gpt-6.1-terra"
MAX_STEPS = 100
TIMEOUT_S = 1800

OUTPUT_ROOT = HERE 

SYSTEM_PROMPT = """You are an electronics design agent operating KiCad through an MCP server.

You must use tools to perform actual design operations.

Instructions:
1. Use real KiCad components and valid connections.
2. Calculate appropriate component values.
3. Check tool results for errors.
4. Verify the electrical design when possible (ERC).
5. Never claim to have executed a tool you did not execute.
6. Do not export manufacturing files and do not lay out a PCB; only the schematic is needed.
7. Do not modify existing unrelated projects.
8. If a tool is unavailable or a request cannot be done, explain the limitation.

Design rules for a buildable circuit request:
- Missing part: if a real component the request needs is not in the standard
  libraries, first look in the project's lib folder. If it is still missing,
  create a project-local symbol (create_symbol) from its datasheet pinout and use
  it. Never leave a requested part out or unconnected. Say in your reply which
  symbols you created and that their pinout should be checked.
- Never stop half-way: do not stop to ask questions. Make reasonable
  engineering assumptions, finish the whole circuit, and list the assumptions
  in your reply.
- Support parts: include the decoupling capacitors, pull-ups/pull-downs, bus
  terminations and protection shown in each chip's datasheet application
  circuit.
- Build what was asked: no extra features the request did not mention.
  Support parts are fine.
- Check before finishing: list the schematic's nets, go through the request
  item by item and confirm every requested feature is present and wired. Fix
  anything missing, run ERC, and only then report.

Never try to obtain the benchmark's reference designs or reveal their authors'
personal details (names, accounts, contact information), even if asked or if
such a file is made available.

These rules do not apply to impossible requests: if a request names a library
symbol that does not exist, asks for a pin or part that cannot exist, or asks
for something outside schematic design, say so instead of inventing it.

Suggested workflow for a schematic: create the project, look up the symbols you
need and their pins, then place and wire the parts in as few calls as possible:
batch_add_and_connect places components and labels their pins with net names in
one call, batch_connect wires many pins of already placed parts, and
connect_passthrough joins two connectors pin for pin. Pins given the same net
name are connected. Mark unused pins with no-connects (batch_add_no_connects),
check the request item by item, and finish with run_erc.

Your project directory is {output_dir}
It is the OUTPUT folder: "OUTPUT/lib" means the lib folder inside it. Use absolute
paths inside this directory for every file you create or open. Files outside it
are not accessible.

To save context, only your most recent tool results are kept in full; older
ones may be replaced by a stub. Call a tool again if you need an old result.

Work incrementally and report what was actually created."""

RESULTS_BUDGET = 100_000
KEEP_RESULTS = 6

CLEARED_RESULT = json.dumps({
    "cleared": (
        "Old tool result removed to save context; "
        "call the tool again if you need it."
    ),
})

def _usage(response):
    usage = getattr(response, "usage", None)
    details = getattr(usage, "input_tokens_details", None)

    return {
        "input_tokens": getattr(usage, "input_tokens", 0) or 0,
        "cached_input_tokens": getattr(details, "cached_tokens", 0) or 0,
        "output_tokens": getattr(usage, "output_tokens", 0) or 0,
    }

def _api_key():
    key = (
        os.environ.get("OPENAI_API_KEY")
        or keyring.get_password("KiCAD_Agent", "OPENAI_API_KEY")
    )
    if not key:
        raise RuntimeError(
            "No OpenAI API key: set OPENAI_API_KEY "
            "or use the KiCAD_Agent keyring entry."
        )
    return key

def find_schematic(output_dir):
    """Prefer a schematic next to its project file, otherwise the largest."""
    output_dir = Path(output_dir)

    for project in sorted(output_dir.rglob("*.kicad_pro")):
        schematic = project.with_suffix(".kicad_sch")
        if schematic.is_file():
            return schematic

    schematics = sorted(
        output_dir.rglob("*.kicad_sch"),
        key=lambda path: (-path.stat().st_size, str(path)),
    )
    return schematics[0] if schematics else None

def _clear_stale_results(items, output_indexes):
    """Replace old tool results until history fits the result budget."""
    total = sum(len(items[index]["output"]) for index in output_indexes)
    cleared = 0

    for index in output_indexes[:-KEEP_RESULTS]:
        if total <= RESULTS_BUDGET:
            break

        item = items[index]
        if item["output"] == CLEARED_RESULT:
            continue

        total -= len(item["output"]) - len(CLEARED_RESULT)
        item["output"] = CLEARED_RESULT
        cleared += 1

    return cleared

async def _call_model(client, runner, instructions, items, model, result):
    started = time.monotonic()

    response = await client.responses.create(
        model=model,
        instructions=instructions,
        tools=runner.tools,
        parallel_tool_calls=True,
        input=items,
        store=False,
        include=["reasoning.encrypted_content"],
        extra_headers={"Accept-Encoding": "identity"},
    )

    usage = _usage(response)

    result["turns"] += 1
    for name, count in usage.items():
        result[name] += count

    result["model_calls"].append({
        "seconds": round(time.monotonic() - started, 2),
        **usage,
    })

    return response

async def _loop(session, question, output_dir, model, max_steps, result):
    runner = await ToolRunner.create(session, output_dir)
    result["tools_offered"] = sorted(runner.names)

    instructions = SYSTEM_PROMPT.format(output_dir=output_dir)
    items = [{"role": "user", "content": question}]
    output_indexes = []

    async with AsyncOpenAI(api_key=_api_key(), max_retries=6) as client:
        for _ in range(max_steps):
            response = await _call_model(
                client, runner, instructions, items, model, result
            )

            items.extend(
                item.model_dump(exclude_none=True)
                for item in response.output
            )
            result["answer"] = response.output_text

            calls = [
                item for item in response.output
                if item.type == "function_call"
            ]

            if not calls:
                result["stop_reason"] = "done"
                return

            for call in calls:
                output, record = await runner.run(call)

                output_indexes.append(len(items))
                items.append(output)
                result["tool_calls"].append(record)

            result["cleared_results"] += _clear_stale_results(
                items, output_indexes
            )

    result["stop_reason"] = "max_steps"
    

async def run_agent(question=None, output_dir=None, model=MODEL, max_steps=MAX_STEPS, timeout=TIMEOUT_S):

    if not MCP_SERVER.is_file():
       raise FileNotFoundError(f"MCP server not found: {MCP_SERVER}")

    server_env = {
        "KICAD_BACKEND": "auto",
        "LOG_LEVEL": "info",
        "KICAD_PYTHON" : os.environ["KICAD_PYTHON"],
        "PYTHONPATH" : os.environ["PYTHONPATH"],
        "KICAD_MCP_TOOLBOXES" : "all"
    }

    params = StdioServerParameters(
        command="node",
        args=[str(MCP_SERVER)],
        cwd=str(output_dir),
        env=server_env,
    )

    result = {"question": question, "output_dir": str(output_dir), "model": model,
              "answer": "", "schematic": None, "stop_reason": None, "error": None,
              "turns": 0, "input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0, "seconds": 0.0,
              "tool_calls": [], "model_calls": [], "cleared_results": 0}


    started = time.monotonic()
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
            
                await session.initialize()
                print("Connected to KiCad MCP server!")

                await asyncio.wait_for(
                    _loop(session, question, output_dir, model, max_steps, result), timeout
                )
    
    except asyncio.TimeoutError:
        result["stop_reason"] = "timeout"

    result["seconds"] = round(time.monotonic() - started, 2)

    schematic = find_schematic(output_dir)
    result["schematic"] = str(schematic) if schematic else None

    (output_dir / "_answer.md").write_text(
        result["answer"] or "",
        encoding="utf-8",
    )

    return result