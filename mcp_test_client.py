
import asyncio
import json
import os
import keyring
from pathlib import Path

from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# --------------------------------------------------
# Configuration
# --------------------------------------------------
api_key = keyring.get_password("KiCAD_Agent", "OPENAI_API_KEY")

os.environ["OPENAI_API_KEY"] = api_key

MODEL = "gpt-6.1-terra"

MCP_SERVER = Path(__file__).parent / "KiCAD-MCP-Server" / "dist" / "index.js"

PROJECT_DIR = Path.home() / "Documents" / "KiCad"

MAX_STEPS = 20

TASK = """
Create a new KiCad project for a simple LED indicator
circuit powered by a 5V external supply.

Requirements:
- One LED
- One current-limiting resistor
- One 2-pin power connector
- Target LED current approximately 10 mA
- Use standard KiCad library components

Start by creating the project and schematic.
Verify component connections and run ERC if supported.
Do not claim a successful design without validation.
"""


SYSTEM_PROMPT = """
You are an electronics design agent operating KiCad
through an MCP server.

You must use tools to perform actual design operations.

Instructions:
1. Inspect available tools before planning operations.
2. Use real KiCad components and valid connections.
3. Calculate appropriate component values.
4. Check tool results for errors.
5. Verify the electrical design when possible.
6. Never claim to have executed a tool you did not execute.
7. Do not export manufacturing files unless requested.
8. Do not modify existing unrelated projects.
9. If a tool is unavailable, explain the limitation.

Work incrementally and report what was actually created.

Use the following project directory for all operations:
""" + str(PROJECT_DIR)

# --------------------------------------------------
# Convert MCP tools into OpenAI function tools
# --------------------------------------------------

def to_openai_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.input_schema,
        "strict": False,
    }


# --------------------------------------------------
# Agent execution
# --------------------------------------------------

async def run_agent(session: ClientSession):
    client = AsyncOpenAI()

    # Step 1: Discover MCP tools
    discovered = []

    page = await session.list_tools()
    discovered.extend(page.tools)

    tools = [to_openai_tool(t) for t in discovered]
    tool_names = {t.name for t in discovered}

    print(f"Discovered {len(tools)} MCP tools:")
    for name in sorted(tool_names):
        print(" -", name)

    # Step 2: Send initial request to OpenAI
    response = await client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input=TASK,
        tools=tools,
        parallel_tool_calls=False,
    )

    # Step 3: Run the agent loop
    for step in range(MAX_STEPS):
        print(f"\n=== Agent step {step + 1} ===")

        calls = [
            item for item in response.output
            if item.type == "function_call"
        ]

        # No tool calls: model has finished
        if not calls:
            print("\nAgent response:")
            print(response.output_text)
            return

        outputs = []

        for call in calls:
            print(f"\nTool: {call.name}")
            print(f"Arguments: {call.arguments}")

            try:
                args = json.loads(call.arguments)

                if call.name not in tool_names:
                    raise ValueError("Unknown tool")

                # Execute the actual KiCad MCP tool
                result = await session.call_tool(
                    call.name,
                    arguments=args,
                )

                # Preserve structured results when available
                if result.structured_content is not None:
                    payload = result.structured_content
                else:
                    payload = [
                        block.model_dump(mode="json")
                        for block in result.content
                    ]

                result_text = json.dumps({
                    "is_error": bool(result.is_error),
                    "result": payload,
                }, default=str)

                print("Result:", result_text[:1000])

            except Exception as exc:
                result_text = json.dumps({
                    "is_error": True,
                    "error": str(exc),
                })
                print("Tool error:", exc)

            outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            })

        # Step 4: Feed tool results back into the LLM
        response = await client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            previous_response_id=response.id,
            input=outputs,
            tools=tools,
            parallel_tool_calls=False,
        )

    print("\nMaximum agent steps reached.")
    print("Last model response:", response.output_text)


# --------------------------------------------------
# Connect to MCP server
# --------------------------------------------------

async def main():
    if not MCP_SERVER.is_file():
        raise FileNotFoundError(
            f"MCP server not found: {MCP_SERVER}"
        )

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set")

    # Pass KiCad-specific configuration to the
    # server only, keeping it out of the agent's
    # Python 3.13 environment.
    server_env = {
        "KICAD_BACKEND": "auto",
        "LOG_LEVEL": "info",
    }

    params = StdioServerParameters(
        command="node",
        args=[str(MCP_SERVER)],
        cwd=str(MCP_SERVER.parent.parent),
        env=server_env,
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to KiCad MCP server!")
            await run_agent(session)


if __name__ == "__main__":
    asyncio.run(main())
