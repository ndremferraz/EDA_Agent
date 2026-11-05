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