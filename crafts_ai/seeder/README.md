# crafts_ai.seeder

> Part of **nawaai** — Faker-based data seeding, no Django required

## Installation

```bash
uv add "nawaai[faker]"
# or
pip install "nawaai[faker]"
```

## Usage

```python
from crafts_ai.seeder import SimpleSeeder, FakerProvider

# Generate fake data
seeder = SimpleSeeder()
users = seeder.generate(count=10, schema={
    "name": "name",
    "email": "email",
    "phone": "phone_number",
})

# Custom provider
provider = FakerProvider(locale="ar_SA")
data = provider.generate_batch("name", count=5)
```

## Public API

| Symbol | Description |
|---|---|
| `SimpleSeeder` | High-level seeder with schema support |
| `FakerProvider` | Faker wrapper with locale support |
