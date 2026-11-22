"""Discover and execute the KiCad agent's MCP and local tools.

The caller owns the MCP session, conversation history and run statistics::

    runner = await ToolRunner.create(session, output_dir)
    # Pass runner.tools to client.responses.create(...).
    output, record = await runner.run(call)
    items.append(output)
    result["tool_calls"].append(record)

Run calls sequentially: KiCad operations can depend on earlier calls. Context
pruning stays in the agent; this module only caps each individual tool result.
"""

import json
import re
import time
from copy import deepcopy
from pathlib import Path


TOOL_CATEGORIES = [
    "schematic",
    "schematic_batch",
    "schematic_layout",
    "symbol_library",
    "symbol_pins",
    "library",
    "validation",
]

EXTRA_TOOLS = {"create_project", "open_project", "save_project", "get_project_info"}
BLOCKED_TOOLS = {
    "digikey_check_library_availability",  # Online part catalog.
    "sync_schematic_to_board",           # Writes the PCB.
    "backannotate_footprints",           # Writes the PCB.
}

# Installed KiCad libraries may be used as inputs, never as output paths.
READ_ONLY_ROOTS = [
    root for root in (Path("/usr/share/kicad"), Path("/usr/share/kicad-nightly"))
    if root.is_dir()
]

READ_LIMIT = 20_000
FILE_LIMIT = 500
RESULT_LIMIT = 8_000
RECORD_LIMIT = 4_000

LOCAL_TOOLS = [
    {
        "type": "function",
        "name": "list_project_files",
        "strict": False,
        "description": "List files recursively inside the project directory or a subfolder.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Folder inside the project; defaults to the project directory.",
                },
            },
        },
    },
    {
        "type": "function",
        "name": "read_project_file",
        "strict": False,
        "description": (
            "Read a text file inside the project directory "
            "(notes, specs, .kicad_sch, .kicad_sym, ...). "
            f"Returns at most {READ_LIMIT} characters."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File path inside the project directory.",
                },
            },
            "required": ["path"],
        },
    },
]
LOCAL_TOOL_NAMES = {tool["name"] for tool in LOCAL_TOOLS}

PATH_KEY = re.compile(r"(?i)(path|dir|file|folder|^filename$)s?$")
OUTPUT_KEY = re.compile(r"(?i)output|target|dest")


class PathRefused(Exception):
    """A tool argument requests access outside the permitted directories."""


def _resolve_path(value, output_dir):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = output_dir / path
    return path.resolve()


def guard_args(args, output_dir):
    """Copy arguments and resolve path fields, enforcing the original agent policy.

    Paths must stay in the project, except installed KiCad library inputs.
    Keys ending in path/dir/file/folder (including plurals) identify paths;
    their values may be strings or lists of strings. Library table scope must
    be 'project'. This is an argument check, not an OS-level filesystem sandbox.
    """
    output_dir = Path(output_dir).resolve()

    def check_path(key, value):
        if not isinstance(value, str) or not value.strip():
            return value

        path = _resolve_path(value, output_dir)
        if path.is_relative_to(output_dir):
            return str(path)

        if not OUTPUT_KEY.search(key):
            for root in READ_ONLY_ROOTS:
                if path.is_relative_to(root.resolve()):
                    return str(path)

        raise PathRefused(
            f"{key}={value!r} is outside the project directory {output_dir}"
        )

    guarded = {}
    for key, value in args.items():
        if not PATH_KEY.search(key):
            guarded[key] = value
        elif isinstance(value, list):
            guarded[key] = [check_path(key, item) for item in value]
        else:
            guarded[key] = check_path(key, value)

    if guarded.get("scope") not in (None, "project"):
        raise PathRefused(
            f"scope={guarded['scope']!r}: only project-scope library tables are allowed"
        )

    return guarded


def run_local_tool(name, args, output_dir):
    """Run a local file tool. Paths are checked even when called directly.

    File tools only access the project; the MCP library exception does not
    apply here. Path refusals raise PathRefused; missing files return errors.
    """
    if name not in LOCAL_TOOL_NAMES:
        raise ValueError(f"unknown local tool {name}")

    output_dir = Path(output_dir).resolve()
    path = _resolve_path(args.get("path") or output_dir, output_dir)
    if not path.is_relative_to(output_dir):
        raise PathRefused(f"path={str(path)!r} is outside the project directory {output_dir}")

    if name == "list_project_files":
        if not path.is_dir():
            return {"is_error": True, "error": f"not a folder: {path}"}

        files = []
        for entry in path.rglob("*"):
            if entry.name.startswith("_") or not entry.is_file():
                continue
            # Do not advertise symlinks to files outside the project.
            if entry.resolve().is_relative_to(output_dir):
                files.append(str(entry.relative_to(output_dir)))

        return {"is_error": False, "result": sorted(files)[:FILE_LIMIT]}

    if not args.get("path"):
        return {"is_error": True, "error": "read_project_file requires path"}
    if not path.is_file():
        return {"is_error": True, "error": f"file not found: {path}"}

    # Read one extra character to detect truncation without loading the file.
    with path.open(encoding="utf-8", errors="replace") as source:
        text = source.read(READ_LIMIT + 1)

    return {
        "is_error": False,
        "result": text[:READ_LIMIT],
        "truncated": len(text) > READ_LIMIT,
    }


def _openai_tool(tool):
    """Convert an MCP tool to an OpenAI Responses function definition."""
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
        "strict": False,
    }


async def allowed_tool_names(session):
    """Read the server's category membership and apply the agent's exclusions."""
    names = set(EXTRA_TOOLS)
    for category in TOOL_CATEGORIES:
        response = await session.call_tool(
            "get_category_tools", arguments={"category": category}
        )
        data = response.structured_content
        if data is None:
            text = " ".join(getattr(block, "text", "") for block in response.content)
            data = json.loads(text)

        if response.is_error or "error" in data:
            raise RuntimeError(f"Cannot list tool category {category}: {data}")

        for tool in data.get("tools", []):
            names.add(tool["name"] if isinstance(tool, dict) else tool)

    return names - BLOCKED_TOOLS


async def discover_tools(session):
    """Return allowed MCP schemas plus local schemas, ready for the model."""
    allowed = await allowed_tool_names(session)
    tools = []
    cursor = None

    while True:
        if cursor is None:
            page = await session.list_tools()
        else:
            page = await session.list_tools(cursor=cursor)
        tools.extend(
            _openai_tool(tool) for tool in page.tools
            if tool.name in allowed and tool.name not in LOCAL_TOOL_NAMES
        )
        cursor = page.next_cursor
        if cursor is None:
            break

    return tools + deepcopy(LOCAL_TOOLS)


class ToolRunner:
    """Tool definitions and execution for one initialized session and project.

    Use ``await ToolRunner.create(session, output_dir)`` to discover tools.
    Session startup/shutdown and model calls remain the agent's responsibility.
    """

    def __init__(self, session, output_dir, tools):
        self.session = session
        self.output_dir = Path(output_dir).resolve()
        self.tools = tools
        self.names = {tool["name"] for tool in tools}

    @classmethod
    async def create(cls, session, output_dir):
        tools = await discover_tools(session)
        return cls(session, output_dir, tools)

    async def _execute(self, name, args):
        if name in LOCAL_TOOL_NAMES:
            return run_local_tool(name, args, self.output_dir)

        response = await self.session.call_tool(name, arguments=args)
        payload = response.structured_content
        if payload is None:
            payload = [block.model_dump(mode="json") for block in response.content]

        return {"is_error": bool(response.is_error), "result": payload}

    async def run(self, call):
        """Return ``(function_call_output, log_record)`` for a model tool call.

        Accepts a Responses function-call item with name, arguments and call_id.
        JSON, path and execution errors become tool error outputs, so the model
        can recover. Cancellation propagates to the caller. Record fields and
        truncation match eval/agent.py; no conversation or run state is mutated.
        """
        started = time.monotonic()
        record = {"name": call.name, "arguments": call.arguments}

        try:
            args = json.loads(call.arguments or "{}")
            record["arguments"] = args
            if call.name not in self.names:
                raise ValueError(f"unknown or unavailable tool {call.name}")
            if not isinstance(args, dict):
                raise ValueError("tool arguments must be a JSON object")

            args = guard_args(args, self.output_dir)
            result = await self._execute(call.name, args)
            record["is_error"] = result["is_error"]
            text = json.dumps(result, default=str)

        except PathRefused as exc:
            record.update(is_error=True, refused=str(exc))
            text = json.dumps({"is_error": True, "error": f"Refused: {exc}"})
        except Exception as exc:
            record.update(is_error=True, error=str(exc))
            text = json.dumps({"is_error": True, "error": str(exc)})

        record["seconds"] = round(time.monotonic() - started, 2)
        record["result"] = text[:RECORD_LIMIT]

        if len(text) > RESULT_LIMIT:
            removed = len(text) - RESULT_LIMIT
            text = text[:RESULT_LIMIT] + f"... [truncated {removed} chars]"

        output = {
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": text,
        }
        return output, record
