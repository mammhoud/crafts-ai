# craftsai

Standalone AI/MCP toolkit — **no Django required**.

## Install

```bash
pip install craftsai
pip install craftsai[openai]    # + OpenAI
pip install craftsai[anthropic] # + Anthropic Claude
pip install craftsai[mcp]       # + MCP server
```

## Sub-packages

| Package | Description |
|---------|-------------|
| `craftsai.ai` | OpenAI, Claude, and generic AI integrations |
| `craftsai.mcp` | Model Context Protocol server utilities |
| `craftsai.seeder` | Faker-based data seeding (framework-agnostic) |
| `craftsai.orchestrator` | Spec task orchestration engine |

## Quick Usage

```python
# AI integrations
from craftsai.ai.integrations import AIIntegrationRegistry
ai = AIIntegrationRegistry.get("openai", api_key="sk-...")
response = ai.generate("Summarize this article: ...")

# MCP server
from craftsai.mcp.server import MCPServer
server = MCPServer(name="my-tools")

@server.tool("search")
def search(query: str) -> list:
    return []  # your implementation

# Seeder
from faker import Faker
from craftsai.seeder import Seeder
seeder = Seeder(Faker())
seeder.add_entity(MyModel, 10)
seeder.execute()

# Orchestrator CLI
craftsai --help
```

## django_seed (deprecated)

The `django_seed` package in this repo is a deprecated shim. Use:
- `craftsai` for standalone AI/MCP/seeding
- `django_rseal` for Django-integrated automation
