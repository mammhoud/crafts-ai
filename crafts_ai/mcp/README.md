# crafts_ai.mcp

> Part of **nawaai** — Model Context Protocol server utilities

## Installation

```bash
uv add "nawaai[mcp]"
# or
pip install "nawaai[mcp]"
```

## Usage

```python
from crafts_ai.mcp import MCPServer

server = MCPServer(name="my-server", version="1.0.0")

@server.tool()
def my_tool(query: str) -> str:
    return f"Result for: {query}"

server.run()
```

## Directory Tree

```
mcp/
├── server.py    # MCPServer class & tool decorator
└── __init__.py
```
