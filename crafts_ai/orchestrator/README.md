# crafts_ai.orchestrator

> Part of **nawaai** — Spec task execution engine, pure Python

## Installation

```bash
uv add nawaai
# or
pip install nawaai
```

## Usage

```python
from crafts_ai.orchestrator import SpecTaskOrchestrator

# Programmatic usage
orchestrator = SpecTaskOrchestrator(spec_dir=".kiro/specs")
tasks = orchestrator.scan()
for task in tasks:
    print(task.id, task.title, task.status)

orchestrator.execute(task_id="1")
```

```bash
# CLI usage
craftsai scan              # discover all spec tasks
craftsai list              # list tasks with status
craftsai execute --task-id 1   # run a specific task
```

## Directory Tree

```
orchestrator/
├── cli.py           # CLI entry point
├── config.py        # Configuration
├── errors.py        # Custom exceptions
├── executor.py      # Task executor
├── filter.py        # Task filtering
├── interfaces.py    # Abstract interfaces
├── models.py        # Task data models
├── orchestrator.py  # Core orchestrator
├── parser.py        # Spec file parser
├── progress.py      # Progress tracking
├── scanner.py       # Spec directory scanner
├── tracker.py       # Execution tracker
└── __init__.py
```

## Public API

| Symbol | Description |
|---|---|
| `SpecTaskOrchestrator` | Main orchestrator class |
