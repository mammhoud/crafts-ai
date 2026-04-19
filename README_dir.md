# nawaai

Pure Python AI/MCP toolkit — zero Django dependencies.

## Installation

```bash
uv add nawaai
# or
pip install nawaai
```

## Directory Tree

```
nawaai/
├── crafts_ai/
│   ├── ai/              # AI integrations (OpenAI, Claude)
│   ├── chat/            # Chat REST & Rasa clients
│   ├── mcp/             # Model Context Protocol server
│   ├── orchestrator/    # Spec task execution engine
│   ├── seeder/          # Faker-based data seeding
│   ├── __init__.py
│   ├── py.typed
│   └── README.md
├── docs/
│   └── README.md
├── assets/
│   └── cover.png
├── CHANGELOG.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Usage

```python
# AI integrations
from crafts_ai.ai import OpenAIIntegration
ai = OpenAIIntegration(api_key="...")
response = ai.generate("Summarize this text")

# Chat client
from crafts_ai.chat import CraftsClient, ChatBubble
client = CraftsClient(base_url="http://localhost:8765")
bubble = ChatBubble(client=client)
reply = bubble.send("Hello!", session_id="user123")

# Orchestrator CLI
# craftsai scan
# craftsai list
# craftsai execute --task-id 1

# Seeder
from crafts_ai.seeder import SimpleSeeder
seeder = SimpleSeeder()
data = seeder.generate(count=10)
```

## Related Packages

- [django-grep](../django-grep/) — Testing framework
- [django-osoul](../django-osoul/) — Pure Django foundation
- [django-rseal](../django-rseal/) — Automation layer
