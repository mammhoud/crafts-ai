# crafts_ai.ai

> Part of **nawaai** — AI integrations, no Django required

## Installation

```bash
uv add nawaai
# or
pip install nawaai
```

## Usage

```python
from crafts_ai.ai import OpenAIIntegration, ClaudeIntegration, AIIntegrationRegistry

# OpenAI
ai = OpenAIIntegration(api_key="sk-...")
response = ai.generate("Summarize: ...")
print(response.text)

# Claude
ai = ClaudeIntegration(api_key="...")
response = ai.generate("Explain this code")

# Registry — use by name
registry = AIIntegrationRegistry()
registry.register("openai", OpenAIIntegration(api_key="..."))
ai = registry.get("openai")
```

## Public API

| Symbol | Description |
|---|---|
| `AIIntegration` | Abstract base class |
| `OpenAIIntegration` | OpenAI GPT integration |
| `ClaudeIntegration` | Anthropic Claude integration |
| `AIIntegrationRegistry` | Named registry for integrations |
