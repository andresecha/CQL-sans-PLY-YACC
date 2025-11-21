# Contributing to Corpus Query Language

First off, thank you for considering contributing to Corpus Query Language! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include any error messages or stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (PEP 8)
* Include tests for new features
* Update documentation as needed
* End all files with a newline

## Development Setup

1. Fork the repo and clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/CQL.git
cd CQL
```

2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

3. Install pre-commit hooks

```bash
pre-commit install
```

4. Create a new branch for your changes

```bash
git checkout -b feature/your-feature-name
```

## Code Standards

### Style Guide

We use the following tools to ensure code quality:

* **Black**: Code formatting
* **Ruff**: Linting
* **MyPy**: Type checking

Run these before committing:

```bash
black src tests
ruff check src tests
mypy src
```

### Type Hints

All new code must include type hints:

```python
def process_query(query: str, corpus: list[dict[str, str]]) -> list[tuple[int, int]]:
    """Process a CQL query."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.

    Examples:
        >>> example_function("test", 42)
        True
    """
    ...
```

### Testing

All new features must include tests:

```bash
pytest tests/
pytest --cov=corpus_query_language --cov-report=html
```

Tests should:
* Be descriptive
* Test edge cases
* Have good coverage
* Be fast and isolated

## Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

Examples:
```
Add support for wildcard queries

Implement wildcard matching in the lexer and parser to support
queries like [lemma='test*'].

Fixes #123
```

## Project Structure

```
CQL/
├── src/
│   └── corpus_query_language/
│       ├── __init__.py
│       ├── __main__.py
│       ├── core/
│       ├── engine/
│       ├── language/
│       └── utils/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_core.py
│   └── test_utils.py
├── pyproject.toml
├── README.md
└── CONTRIBUTING.md
```

## Questions?

Feel free to open an issue with the tag "question" or contact the maintainers directly.

## License

By contributing, you agree that your contributions will be licensed under the CC-BY-NC-SA-4.0 License.
