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

## Path to KiCAD python
```bash
conda activate kicad-mcp

conda env config vars set \
  KICAD_PYTHON="$CONDA_PREFIX/bin/python" \
  PYTHONPATH="$("$CONDA_PREFIX/bin/python" -B -c 'import sysconfig; print(sysconfig.get_path("purelib"))'):/usr/lib/python3/dist-packages"

conda deactivate
conda activate kicad-mcp
```
or if you use venv use(everytime you create a new terminal):
```
export KICAD_PYTHON="$VIRTUAL_ENV/bin/python"
export PYTHONPATH="/usr/lib/python3/dist-packages"
```

## Run

```bash
python mcp_test_client.py
```

## Web UI

```bash
.venv/bin/python ui/server.py        # then open http://127.0.0.1:8765
```

Type a circuit request (or pick a task from `eval/tasks.jsonl`) and watch the agent's tool calls live, with a schematic preview that refreshes as the agent edits it (rendered with `kicad-cli`). Runs started from a request are saved in `ui/runs/`, task runs in `eval/output/<task>/runN/`; both can be browsed, stopped and deleted from the sidebar.

## Evaluation

Run evaluation tasks in parallel (stop the sequential runner first if it uses
the same run number):

```bash
./eval/run_tasks_parallel.sh --jobs 4
```

This defaults to ReAct run 4, skips existing output folders, and writes separate
logs to `eval/logs/react-run4/`. Use `--run`, `--approach`, or trailing task IDs
to select other runs or tasks. Preview the selection with `--dry-run`.

Needs [KiCAD_benchmark](https://github.com/ndremferraz/KiCAD_benchmark) (dev branch) cloned next to this repo, or pass its path with `--benchmark` (`benchmark=` in Python).

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt -r KiCAD-MCP-Server/requirements.txt
```

Run the agent on one task from `eval/tasks.jsonl`:

```bash
python eval/prepare_dependencies.py
python eval/agent.py b37
```

`prepare_dependencies.py` copies only the task's named local libraries from
`../KiCAD_benchmark/data` into `OUTPUT/<task id>/lib`. The agent copies that
folder into its run directory before each build task.

Or from Python:

```python
from agent import run_task  # eval/agent.py
result = await run_task(task, "eval/output/b37/run0")  # task = one line of tasks.jsonl
result["schematic"]  # path to the agent's .kicad_sch, or None
```

The output goes to `eval/output/b37/run0/`: the agent's schematic, plus `_run.json` with the answer, turns, tokens, latency and every tool call.

The agent only sees the task's question and can only access files in its output folder.
