# Django Seed - Enhanced Edition

Django Seed is an enhanced Django package that combines:

1. **Spec Task Orchestrator** - Comprehensive spec management and task execution system
2. **MCP Designer** - Model Context Protocol integration for AI-assisted development
3. **Django Components** - Reusable Wagtail/Django components

## Features

### 🎯 Spec Task Orchestrator
- Discover and index spec directories
- Parse requirements, design, and task files
- Track tasks by category and status
- Execute tasks with multiple handlers
- Property-based testing support
- Comprehensive error handling
- Progress tracking and reporting

### 🤖 MCP Designer
- AI-safe template and style editing
- Live preview generation
- Component style updates
- File patching with SEARCH/REPLACE
- Webhook support for CI/CD integration

### 🧩 Django Components
- Pre-built Wagtail StreamField blocks
- Template tag integration
- Asset manifest management
- Reusable component system

## Installation

### Using uv (Recommended)

```bash
uv pip install django-seed
```

### Using pip

```bash
pip install django-seed
```

## Quick Start

### 1. Add to Django Settings

```python
INSTALLED_APPS = [
    # ...
    "django_seed.orchestrator",
    "django_seed.mcp_designer",
    "django_seed.comp",
    # ...
]
```

### 2. Use the Orchestrator

```python
from django_seed.orchestrator import SpecTaskOrchestrator

orchestrator = SpecTaskOrchestrator()
result = orchestrator.load_specs()
print(f"Loaded {result['loaded']} specs")

# Get tasks by category
tasks = orchestrator.get_tasks_by_category("auth")

# Execute a task
result = orchestrator.execute_task("task-id")

# Get progress
progress = orchestrator.get_spec_progress("auth", "spec-name")
```

### 3. Start MCP Server

```bash
mcp-django-server
```

### 4. Use CLI

```bash
orchestrator scan
orchestrator load
orchestrator list --category auth
orchestrator progress --category auth --spec spec-name
```

## Configuration

### Environment Variables

```bash
export ORCHESTRATOR_BASE_PATH=".kiro/specs-organized"
export ORCHESTRATOR_PBT_FRAMEWORK="hypothesis"
export ORCHESTRATOR_PBT_ITERATIONS="100"
export MCP_CREATE_BACKUPS="true"
export MCP_WEBHOOK_URL="https://example.com/webhook"
```

### Django Settings

```python
# Orchestrator settings
ORCHESTRATOR_BASE_PATH = ".kiro/specs-organized"
ORCHESTRATOR_PBT_FRAMEWORK = "hypothesis"
ORCHESTRATOR_PBT_ITERATIONS = 100

# MCP Designer settings
MCP_CREATE_BACKUPS = True
MCP_WEBHOOK_URL = None
MCP_TEMPLATE_EXTENSIONS = [".html"]
MCP_STYLE_EXTENSIONS = [".css", ".scss"]
MCP_EXTRA_TEMPLATE_DIRS = []
MCP_EXTRA_STATIC_DIRS = []
```

## Architecture

```
django-seed/
├── orchestrator/          # Spec Task Orchestrator
│   ├── models.py         # Data models
│   ├── scanner.py        # Spec discovery
│   ├── parser.py         # File parsing
│   ├── tracker.py        # Task tracking
│   ├── executor.py       # Task execution
│   ├── pbt.py           # Property-based testing
│   ├── progress.py      # Progress tracking
│   ├── filter.py        # Task filtering
│   ├── errors.py        # Error handling
│   ├── config.py        # Configuration
│   ├── compatibility.py # Backward compatibility
│   ├── orchestrator.py  # Main orchestrator
│   └── cli.py          # CLI interface
├── mcp_designer/         # MCP Designer
│   ├── mcp_server.py    # MCP server
│   ├── utils.py         # Utilities
│   ├── signals.py       # Django signals
│   └── management/      # Django management commands
├── comp/                 # Components
│   ├── blocks.py        # Wagtail blocks
│   └── tags.py          # Template tags
└── contrib/             # Utilities
    ├── conf.py          # Configuration
    └── helpers.py       # Helper functions
```

## Testing

### Run Tests

```bash
# Using pytest
pytest tests/

# Using uv
uv run pytest tests/

# With coverage
pytest tests/ --cov=django_seed
```

### Run Property-Based Tests

```bash
pytest tests/test_properties.py -v
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/mammhoud/django-seed.git
cd django-seed

# Install with uv
uv sync

# Run tests
uv run pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Documentation

- [Orchestrator Guide](docs/orchestrator.md)
- [MCP Designer Guide](docs/mcp_designer.md)
- [Component Guide](docs/components.md)
- [API Reference](docs/api.md)

## License

MIT License - See LICENSE file for details

## Support

- GitHub Issues: https://github.com/mammhoud/django-seed/issues
- Documentation: https://django-seed.readthedocs.io
- Email: support@example.com

## Changelog

### Version 1.0.0 (2024)
- Initial release with Spec Task Orchestrator
- MCP Designer integration
- Full test coverage
- Comprehensive documentation
