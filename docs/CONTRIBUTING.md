# 🤝 Guide de Contribution - AstroWikiBuilder

Thank you for your interest in contributing to AstroWikiBuilder! This document provides guidelines and best practices for contributors.

---

## 📋 Table des matières

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Coding Standards](#coding-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Project Structure](#project-structure)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Git
- Virtual environment tool (venv)

### Setup

```bash
# Clone the repository
git clone https://github.com/votre-username/AstroWikiBuilder.git
cd AstroWikiBuilder

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-cov pytest-mock mypy
```

---

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Your Changes

Follow the coding standards (see below) and ensure your changes:
- Are well-documented
- Include unit tests
- Pass all existing tests
- Follow the project architecture

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html  # or start htmlcov/index.html on Windows
```

### 4. Code Quality Checks

```bash
# Type checking with mypy
mypy src/
```

### 5. Commit Your Changes

Use conventional commit messages:

```bash
# Format: <type>: <description>
# Examples:
git commit -m "feat: Add support for Exoplanet.eu data source"
git commit -m "fix: Correct reference formatting in Wikipedia articles"
git commit -m "docs: Update README with new CLI options"
git commit -m "test: Add tests for StarRepository"
git commit -m "refactor: Extract main.py logic into orchestration module"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `perf`: Performance improvements
- `chore`: Maintenance tasks

---

## 📝 Coding Standards

### Python Style Guide

We follow **PEP 8** with strict typing enforcement via **mypy**.

#### Key Rules:

1. **Type Hints**: All functions must have type hints
```python
def collect_entities(source: str) -> Tuple[List[Exoplanet], List[Star]]:
    pass
```

2. **Docstrings**: All public functions and classes must have docstrings
```python
def parse_cli_arguments() -> argparse.Namespace:
    """
    Configure et parse les arguments de la ligne de commande.

    Returns:
        argparse.Namespace: Arguments parsés

    Example:
        >>> args = parse_cli_arguments()
        >>> print(args.sources)
        ['nasa_exoplanet_archive']
    """
    pass
```

3. **Naming Conventions**:
   - Files: `snake_case.py`
   - Classes: `PascalCase`
   - Functions/Variables: `snake_case`
   - Constants: `SCREAMING_SNAKE_CASE`
   - Private methods: `_leading_underscore`

4. **Line Length**: Maximum 100 characters

5. **Imports**: Organize imports in this order:
   ```python
   # Standard library
   import os
   from datetime import datetime

   # Third-party
   import pandas as pd
   import requests

   # Local
   from src.models.entities.exoplanet_entity import Exoplanet
   ```

---

## ✅ Testing Guidelines

### Test Structure

```
tests/
├── unit/                    # Unit tests
│   ├── test_collectors/
│   ├── test_models/
│   ├── test_services/
│   ├── test_generators/
│   ├── test_orchestration/
│   └── test_utils/
├── integration/             # Integration tests
└── conftest.py             # Shared fixtures
```

### Writing Tests

1. **Use descriptive names**:
```python
def test_create_exoplanet_with_all_fields():
    """Test de création d'une exoplanète avec tous les champs."""
    pass
```

2. **Follow AAA pattern** (Arrange, Act, Assert):
```python
def test_parse_cli_arguments():
    # Arrange
    args_list = ['--sources', 'nasa_exoplanet_archive']

    # Act
    args = parse_cli_arguments(args_list)

    # Assert
    assert 'nasa_exoplanet_archive' in args.sources
```

3. **Use fixtures** for shared setup:
```python
@pytest.fixture
def sample_exoplanet():
    return Exoplanet(pl_name="Test Planet b", ...)

def test_something(sample_exoplanet):
    assert sample_exoplanet.pl_name == "Test Planet b"
```

4. **Test Coverage**: Aim for >80% coverage
   - All new features must include tests
   - Bug fixes should include regression tests

---

## 🔍 Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted (Ruff)
- [ ] No linting errors (Ruff)
- [ ] Type checking passes (mypy)
- [ ] Documentation is updated
- [ ] CHANGELOG is updated (if applicable)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Review Process

1. Maintainer reviews code
2. CI/CD checks must pass
3. At least one approval required
4. Changes requested must be addressed
5. Squash and merge into `main`

---

## 🏗️ Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

### Key Principles

1. **Separation of Concerns (SOC)**
   - Each module has one clear responsibility
   - No mixing of data collection, processing, and presentation

2. **Single Responsibility Principle (SRP)**
   - Each class/function does one thing well
   - Easy to test and maintain

3. **Dependency Inversion**
   - Depend on abstractions, not concrete implementations
   - Use abstract base classes (e.g., `BaseCollector`)

4. **Don't Repeat Yourself (DRY)**
   - Shared logic goes in `utils/`
   - Reuse via composition

---

## 🆕 Adding New Features

### Adding a New Data Source

1. Create collector in `src/collectors/implementations/`
```python
# src/collectors/implementations/my_source_collector.py
from src.collectors.base_collector import BaseCollector

class MySourceCollector(BaseCollector):
    def get_data_download_url(self) -> str:
        return "https://my-source-api.com/data"

    # Implement other abstract methods
```

2. Register in `src/orchestration/service_initializer.py`
```python
def _get_collector_instance(source, use_mock, cache_path):
    if source == "my_source":
        return MySourceCollector(...)
```

3. Add tests in `tests/unit/test_collectors/`

4. Update documentation

### Adding New Article Sections

1. Create generator in `src/generators/articles/<entity>/parts/`
2. Integrate in main article generator
3. Add tests
4. Update documentation

---

## 📞 Questions?

- Open an issue for bugs or feature requests
- For general questions, use Discussions
- Check existing issues before creating new ones

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AstroWikiBuilder! 🚀✨**
