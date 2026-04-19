# crafts_ai

> Part of **nawaai** — Pure Python AI/MCP toolkit

## Installation

```bash
uv add nawaai
# or
pip install nawaai
```

## Directory Tree

```
crafts_ai/
├── ai/              # AI integrations (OpenAI, Claude)
├── chat/            # Chat REST & Rasa clients
├── mcp/             # Model Context Protocol server
├── orchestrator/    # Spec task execution engine
├── seeder/          # Faker-based data seeding
├── __init__.py
└── py.typed
```

## Usage

```python
from crafts_ai.ai import OpenAIIntegration, ClaudeIntegration
from crafts_ai.chat import CraftsClient, ChatBubble
from crafts_ai.mcp import MCPServer
from crafts_ai.orchestrator import SpecTaskOrchestrator
from crafts_ai.seeder import SimpleSeeder
```

## Public API

| Symbol | Module |
|---|---|
| `OpenAIIntegration` | `crafts_ai.ai` |
| `ClaudeIntegration` | `crafts_ai.ai` |
| `CraftsClient` | `crafts_ai.chat` |
| `ChatBubble` | `crafts_ai.chat` |
| `RasaClient` | `crafts_ai.chat` |
| `SpecTaskOrchestrator` | `crafts_ai.orchestrator` |
| `SimpleSeeder` | `crafts_ai.seeder` |
