# django-seed

This package contains two things: **nawaai** (new standalone AI toolkit) and **django_seed** (deprecated shim).

---

## nawaai — Standalone AI/MCP Toolkit

nawaai is a pure Python AI/MCP toolkit. No Django required. It is bundled inside the `django-seed` package.

### Install

```bash
pip install django-seed                    # includes nawaai
pip install django-seed[openai]            # + openai>=1.0
pip install django-seed[anthropic]         # + anthropic>=0.3
pip install django-seed[mcp]               # + mcp
```

### AI Integrations

```python
from nawaai.ai.integrations import AIIntegrationRegistry, OpenAIIntegration

# API keys from environment (OPENAI_API_KEY, ANTHROPIC_API_KEY)
ai = AIIntegrationRegistry.get("openai")
response = ai.generate("Explain MCP in one sentence")

# Or pass key directly
ai = AIIntegrationRegistry.get("claude", api_key="sk-ant-...")
for chunk in ai.stream("Write a haiku"):
    print(chunk, end="")
```

### MCP Server

```python
from nawaai.mcp.server import MCPServer

server = MCPServer(name="my-tools", version="1.0.0")

@server.tool("summarize")
def summarize(text: str) -> str:
    return text[:100] + "..."

print(server.list_tools())  # ["summarize"]
server.run(host="localhost", port=8765)
```

### Seeder (Faker-based)

```python
# Note: nawaai.seeder re-exports from django_rseal.seeder (Django required)
# For standalone use without Django, use Faker directly:
from faker import Faker
fake = Faker()
print(fake.name(), fake.email())
```

### Orchestrator (Spec Task Engine)

```bash
# CLI entry point
nawaai scan
nawaai load
nawaai list --category auth
nawaai tasks --status not_started
nawaai progress --category auth --spec my-spec
nawaai export --output specs.json
```

```python
from nawaai.orchestrator import SpecTaskOrchestrator

orch = SpecTaskOrchestrator()
orch.load_specs(".kiro/specs")
summary = orch.get_overall_summary()
```

---

## django_seed — Deprecated Shim

> **Deprecated.** The seeding functionality has moved to `django_rseal.seeder`. Use that directly in new code.

```python
# Old (deprecated)
from django_seed import Seed

# New
from django_rseal.seeder import Seeder
```

The `django_seed` package in this repo is a compatibility shim that re-exports from `django_rseal.seeder`. It will be removed in a future version.
