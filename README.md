# EDA_Agent

## Prerequisites

1. KiCad 9+
2. Node.js 18+
3. Python 3.10+

Check that KiCad's Python module loads:

```bash
python3 -c "import pcbnew; print(pcbnew.Version())"
```

## Setup

```bash
git clone <repo>
cd EDA_Agent

# Clone and build KiCAD MCP Server inside this repo
git clone https://github.com/mixelpixx/KiCAD-MCP-Server.git
cd KiCAD-MCP-Server
npm install
npm run build
python3 -m pip install --user -r requirements.txt
cd ..

# Install the EDA agent's python dependencies
python -m pip install -r requirements.txt
```

## OpenAI API key

Get a key from https://platform.openai.com/api-keys and add it to `~/.bashrc`:

```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.bashrc
source ~/.bashrc
```

## Run

```bash
python mcp_test_client.py
```

## Evaluation (`eval/`)

The eval agent and tasks live in `eval/`. It needs the
[KiCAD_benchmark](https://github.com/ndremferraz/KiCAD_benchmark) repo (dev branch)
checked out next to this one, as `../KiCAD_benchmark`: ground-truth netlists are
in its `netlists/`, project-local libraries in `data/*/OUTPUT`.

### Setup

```bash
python3 -m venv --system-site-packages .venv    # system site: KiCad's pcbnew
.venv/bin/pip install -r requirements.txt
.venv/bin/pip install -r KiCAD-MCP-Server/requirements.txt
```

The agent starts the MCP server with `KICAD_PYTHON=.venv/bin/python` when the venv
exists. The OpenAI key is read from `OPENAI_API_KEY`, or from the keyring entry
`KiCAD_Agent` / `OPENAI_API_KEY`.

### Tasks (`eval/tasks.jsonl`)

50 tasks, written by `eval/make_tasks.py`:

| Type | n | What the agent gets | Reference |
|---|---|---|---|
| build | 39 | The short "Build requirements" (+ local dependencies) from a KiCAD_benchmark instructions file | `reference_netlist`: netlist of the original project |
| unanswerable | 11 | Impossible, off-topic, out-of-capability, info-leak, credential, destructive and prompt-injection requests | `rubric`, `forbidden_in_answer`, `forbidden_in_files`, `workdir_only`, `setup_files` |

Edge cases are tagged `edge:*` (no-nets board, mostly mechanical board, custom
symbol, connector pass-through, near-duplicate pair, 177-part board,
contradictory request).

### Running the agent

```bash
.venv/bin/python eval/agent.py b37            # one task -> eval/output/b37/run0/
.venv/bin/python eval/agent.py b37 --run 1    # second run of the same task
```

From Python:

```python
from agent import run_task, run_agent
result = await run_task(task, "eval/output/b37/run0")   # a tasks.jsonl task
result = await run_agent("Draw an LED circuit ...", "some/output/dir")
```

`result` holds `answer`, `schematic` (path to the saved root `.kicad_sch`, or
`None`), `stop_reason` (done / max_steps / timeout / error), `error`, `turns`,
`input_tokens`, `cached_input_tokens`, `output_tokens`, `seconds`,
`cleared_results` and `tool_calls` (name, arguments, result, errors, duration).
Each run folder also gets `_run.json` (the whole result, usable as a trace),
`_answer.md` and `_mcp_server.log`. `eval/output/` is git-ignored.

### What the agent can see

- Only `task["question"]`; the task's `project`, `instructions` and
  `reference_netlist` fields are never shown to it.
- A fresh output folder per run, seeded with the benchmark's `OUTPUT/` folder
  (build tasks) or the task's `setup_files` (prompt-injection task).
- Every path in a tool call is checked first: anything outside the output
  folder is refused, except reading KiCad's installed libraries. Global
  library tables are refused too.
- 49 schematic, project and library tools from the MCP server (out of 244), plus
  three client-side tools: `list_project_files`, `read_project_file` and
  `connect_pins_to_nets` (wires many pins to named nets in one call).

### Context management

The client sends the conversation itself each turn. Tool results are capped at
8,000 characters; once the tool results in the history pass ~100K characters,
the oldest are replaced by a stub (the last 6 always stay). `MAX_STEPS` is 100
model turns, `TIMEOUT_S` 30 minutes per run.

### Notes for grading

- Build tasks: export the agent's schematic with
  `kicad-cli sch export netlist --format kicadxml` and compare it with
  `task["reference_netlist"]` (relative to KiCAD_benchmark).
- Unanswerable tasks: check `forbidden_in_files` only on `*.kicad_*` files. The
  u11 setup file `notes.txt` and `_run.json` contain the injected text on purpose.
