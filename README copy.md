# Corpus Query Language (CQL)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful and flexible Corpus Query Language (CQL) engine for linguistic queries over annotated text corpora.

## Overview

This package provides a complete implementation of a Corpus Query Language engine specifically designed for linguists and NLP researchers. It enables sophisticated pattern matching queries over annotated text corpora, supporting multiple annotation layers including lemmas, parts of speech (POS), morphological features, and word forms.

### Key Features

- 🔍 **Pattern Matching**: Search for complex patterns across annotated tokens
- 📊 **Multiple Annotations**: Query over word, lemma, POS, and morphological annotations
- 🎯 **Boolean Operators**: Combine conditions with AND (`&`) and OR (`|`) operators
- 📏 **Distance Queries**: Find patterns within specified token distances
- 🔄 **Optional Patterns**: Support for zero-or-one (`?`) quantifiers
- 🚀 **High Performance**: Efficient text-directed parsing engine
- 📝 **Type Hints**: Fully typed for better IDE support and code quality
- ✅ **Well Tested**: Comprehensive test suite with pytest

## Installation

### From PyPI

```bash
pip install corpus-query-language
```

### From Source

```bash
git clone https://github.com/matgille/CQL.git
cd CQL
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/matgille/CQL.git
cd CQL
pip install -e ".[dev]"
```

## Quick Start

### Basic Usage

```python
import corpus_query_language as cql

# Create the CQL engine
engine = cql.CQLEngine()

# Load your corpus (list of annotated tokens)
corpus = [
    {"word": "Da", "lemma": "dar", "pos": "VERB", "morph": "Mood=Imp|Person=2"},
    {"word": "paz", "lemma": "paz", "pos": "NOUN", "morph": "Gender=Masc|Number=Sing"},
    {"word": "al", "lemma": "al", "pos": "ADP", "morph": ""},
    {"word": "rey", "lemma": "rey", "pos": "NOUN", "morph": "Gender=Masc|Number=Sing"},
    {"word": "santo", "lemma": "santo", "pos": "ADJ", "morph": "Gender=Masc"},
]

# Execute a simple query
matches = engine.findall(corpus, "[lemma='rey']", verbose=False)
print(f"Found {len(matches)} match(es)")
# Output: Found 1 match(es)

# Check if a pattern exists
has_verb = engine.match(corpus, "[pos='VERB']", verbose=False)
print(f"Contains verb: {has_verb}")
# Output: Contains verb: True
```

### Loading from JSON

```python
import corpus_query_language as cql

# Load corpus from JSON file
corpus = cql.utils.import_corpus("path/to/corpus.json")

engine = cql.CQLEngine()
results = engine.findall(corpus, "[lemma='rey']", verbose=False)
```

## Query Syntax

### Annotation Types

Four annotation types are supported:

- `word`: The surface form
- `lemma`: The dictionary/base form
- `pos`: Part of speech tag
- `morph`: Morphological features

### Basic Queries

```python
# Match by lemma
"[lemma='rey']"

# Match by POS
"[pos='NOUN']"

# Match by morphological feature
"[morph='Gender=Masc']"
```

### Combining Annotations (AND)

```python
# Match tokens that are both NOUNs and have lemma 'rey'
"[lemma='rey' & pos='NOUN']"

# Multiple conditions
"[lemma='rey' & pos='NOUN' & morph='Number=Sing']"
```

### Regular Expressions

```python
# Match lemmas starting with 're'
"[lemma='re.*']"

# Match any verb form
"[pos='VERB.*']"

# Optional 's' at the end
"[lemma='reyes?']"
```

### Alternative Patterns (OR)

```python
# Match either 'rey' or 'príncipe'
"([lemma='rey']|[lemma='príncipe'])"
```

### Distance Queries

```python
# Match 'rey' followed by 'santo' within 0-5 tokens
"[lemma='rey'][]{,5}[lemma='santo']"

# Exact distance of 3 tokens
"[lemma='rey'][]{3,3}[lemma='santo']"
```

### Optional Patterns

```python
# Optional article before noun
"[pos='DET']?[pos='NOUN']"
```

### Complex Queries

```python
# Combine multiple features
"([lemma='rey']|[lemma='príncipe'])[pos='ADP']?[]{,5}[lemma='santo' & pos='ADJ']"
```

## Corpus Format

The corpus must be a list of dictionaries, where each dictionary represents an annotated token:

```python
corpus = [
    {
        "word": "Da",
        "lemma": "dar",
        "pos": "VERB",
        "morph": "Mood=Imp|Number=Sing|Person=2"
    },
    {
        "word": "paz",
        "lemma": "paz",
        "pos": "NOUN",
        "morph": "Gender=Masc|Number=Sing"
    }
]
```

### JSON Format

```json
[
  {
    "word": "Da",
    "lemma": "dar",
    "pos": "VERB",
    "morph": "Mood=Imp|Number=Sing|Person=2"
  },
  {
    "word": "paz",
    "lemma": "paz",
    "pos": "NOUN",
    "morph": "Gender=Masc|Number=Sing"
  }
]
```

## API Reference

### CQLEngine

The main interface for executing queries.

#### Methods

##### `findall(corpus, query, verbose=True, debug=False)`

Find all occurrences of a pattern in the corpus.

**Parameters:**
- `corpus` (list[dict]): Annotated corpus
- `query` (str): CQL query string
- `verbose` (bool): Print results (default: True)
- `debug` (bool): Enable debug logging (default: False)

**Returns:**
- `list[tuple[int, int]]`: List of (start, end) index tuples

**Example:**
```python
results = engine.findall(corpus, "[lemma='rey']", verbose=False)
# [(3, 4)]
```

##### `match(corpus, query, verbose=True, debug=False)`

Check if a pattern exists in the corpus (stops at first match).

**Parameters:**
- `corpus` (list[dict]): Annotated corpus
- `query` (str): CQL query string
- `verbose` (bool): Print results (default: True)
- `debug` (bool): Enable debug logging (default: False)

**Returns:**
- `bool`: True if pattern found, False otherwise

**Example:**
```python
found = engine.match(corpus, "[pos='VERB']", verbose=False)
# True
```

## Command-Line Interface

```bash
# Find all matches
cql "[lemma='rey']" corpus.json

# Match mode (returns boolean)
cql -m match "[pos='VERB']" corpus.json

# Verbose output
cql -v "[lemma='rey']" corpus.json

# Debug mode
cql -d "[lemma='rey']" corpus.json
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/matgille/CQL.git
cd CQL

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=corpus_query_language --cov-report=html

# Run specific test file
pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC-BY-NC-SA-4.0). See the [LICENSE](LICENSE) file for details.

## Citation

If you use this software in your research, please cite:

```bibtex
@software{corpus_query_language,
  author = {Gille Levenson, Matthias},
  title = {Corpus Query Language: A CQL Engine for Linguistic Corpus Queries},
  year = {2025},
  url = {https://github.com/matgille/CQL}
}
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes in each version.

## Support

- **Issues**: [GitHub Issues](https://github.com/matgille/CQL/issues)
- **Documentation**: [GitHub README](https://github.com/matgille/CQL#readme)

## Acknowledgments

This project uses [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/) for lexical analysis and parsing.

## Related Projects

- [Corpus Workbench (CWB)](http://cwb.sourceforge.net/)
- [CQPweb](http://cwb.sourceforge.net/cqpweb.php)
- [BlackLab](https://github.com/INL/BlackLab)
