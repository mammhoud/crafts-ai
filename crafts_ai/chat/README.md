# crafts_ai.chat

> Part of **nawaai** — Chat REST & Rasa clients

## Installation

```bash
uv add nawaai
# or
pip install nawaai
```

## Usage

```python
from crafts_ai.chat import CraftsClient, ChatBubble, RasaClient

# REST chat client
client = CraftsClient(base_url="http://localhost:8765")
bubble = ChatBubble(client=client)
reply = bubble.send("Hello!", session_id="user123")
print(reply.text)

# Rasa client
rasa = RasaClient(base_url="http://localhost:5005")
response = rasa.send_message("Hi there", sender="user1")
```

## Public API

| Symbol | Description |
|---|---|
| `CraftsClient` | HTTP client for the crafts chat server |
| `ChatBubble` | High-level chat interface |
| `RasaClient` | Rasa NLU/Core REST client |
