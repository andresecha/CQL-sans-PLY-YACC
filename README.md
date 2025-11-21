# CQL - Corpus Query Language

A powerful and flexible Corpus Query Language (CQL) engine for linguistic queries over annotated text corpora.

## ⚡ Recent Changes - v1.0.0

**🎉 Major Update:** We've replaced the deprecated PLY/YACC parser with the modern **Lark** parser!

- ✅ **100% backward compatible** - No code changes needed
- ✅ **Better performance** - Faster parsing and lower memory usage
- ✅ **Actively maintained** - Lark is regularly updated (Oct 2025)
- ✅ **Cleaner code** - EBNF grammar is more readable and maintainable
- ✅ **Better errors** - More descriptive parse error messages

All existing functionality works exactly as before. Simply update your dependencies:

```bash
pip install --upgrade corpus-query-language
```

## 🚀 Installation

```bash
pip install corpus-query-language
```

### Requirements

- Python >= 3.9
- lark >= 1.1.9

## 📖 Quick Start

```python
from corpus_query_language.core import CQLEngine

# Create engine
engine = CQLEngine()

# Your annotated corpus
corpus = [
    {"word": "The", "lemma": "the", "pos": "DET", "morph": ""},
    {"word": "cat", "lemma": "cat", "pos": "NOUN", "morph": "Number=Sing"},
    {"word": "sleeps", "lemma": "sleep", "pos": "VERB", "morph": "Number=Sing|Tense=Pres"},
]

# Find all nouns
results = engine.findall(corpus, "[pos='NOUN']", verbose=False)
print(results)  # [(1, 2)]

# Check if pattern exists
has_det_noun = engine.match(corpus, "[pos='DET'][pos='NOUN']", verbose=False)
print(has_det_noun)  # True
```

## 🎯 CQL Syntax

### Simple Queries

Match annotations on single tokens:

```python
[lemma='cat']        # Match lemma
[pos='NOUN']         # Match part-of-speech
[word='sleeps']      # Match word form
[morph='Number=Sing'] # Match morphological features
```

### Logical Operators

#### AND (`&`)

All conditions must match the same token:

```python
[lemma='cat' & pos='NOUN']
[pos='VERB' & morph='Tense=Past']
```

#### NOT EQUAL (`!=`)

Exclude matches:

```python
[pos!='PUNCT']       # Not punctuation
[lemma!='be']        # Not lemma "be"
```

#### OR (`|`)

Match any of the alternatives (use parentheses):

```python
([lemma='cat' | lemma='dog'])
([pos='NOUN' | pos='PROPN'])
```

### Sequences

Match sequences of tokens:

```python
[pos='DET'][pos='NOUN']                    # Article + Noun
[pos='DET'][pos='ADJ'][pos='NOUN']         # Article + Adjective + Noun
```

### Distance Operator

Allow gaps between tokens:

```python
[pos='DET'][]{0,3}[pos='NOUN']             # 0-3 words between DET and NOUN
[lemma='have'][]{1,5}[pos='VERB']          # 1-5 words between "have" and a verb
```

### Optional Queries

Make a query element optional:

```python
[pos='DET']?[pos='NOUN']                    # Optional determiner before noun
[pos='ADV']?[pos='VERB']                    # Optional adverb before verb
```

### Complex Queries

Combine multiple features:

```python
# Determiner, optional adjective, noun
[pos='DET'][pos='ADJ']?[pos='NOUN']

# "Have" followed by past participle within 2 words
[lemma='have'][]{0,2}[morph='VerbForm=Part']

# Noun or proper noun, not followed by punctuation
([pos='NOUN' | pos='PROPN'])[pos!='PUNCT']
```

## 📚 API Reference

### CQLEngine

Main class for executing CQL queries.

#### `findall(corpus, query, verbose=True, debug=False)`

Find all matches of a query in the corpus.

**Parameters:**
- `corpus` (list): List of annotated tokens (dicts)
- `query` (str): CQL query string
- `verbose` (bool): Print results (default: True)
- `debug` (bool): Enable debug logging (default: False)

**Returns:**
- `list[tuple[int, int]]`: List of (start, end) index tuples

**Example:**
```python
results = engine.findall(corpus, "[pos='VERB']")
# [(2, 3), (5, 6)]
```

#### `match(corpus, query, verbose=True, debug=False)`

Check if query matches anywhere in corpus (stops at first match).

**Parameters:**
- Same as `findall()`

**Returns:**
- `bool`: True if match found, False otherwise

**Example:**
```python
has_match = engine.match(corpus, "[lemma='cat']")
# True or False
```

## 🏗️ Architecture

The new Lark-based architecture provides:

```
corpus_query_language/
├── language/
│   ├── grammar.lark      # EBNF grammar definition
│   ├── parser.py         # Lark-based parser with AST transformer
│   └── __init__.py
├── engine/
│   └── engine.py         # Query execution engine
├── core/
│   └── core.py           # CQLEngine API
└── utils/
    └── utils.py          # Utility functions
```

### Key Components

1. **grammar.lark**: Declarative EBNF grammar defining CQL syntax
2. **CQLParser**: Modern parser using Lark's LALR(1) algorithm
3. **ASTTransformer**: Converts parse tree to executable AST
4. **parse_corpus()**: Executes AST against corpus data

## 🧪 Development

### Setup

```bash
git clone https://github.com/matgille/CQL.git
cd CQL
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest                          # Run all tests
pytest --cov                    # With coverage
pytest -v tests/test_core.py    # Specific test file
```

### Code Quality

```bash
black src tests                 # Format code
ruff check src tests            # Lint code
mypy src                        # Type check
```

## 📝 Migration from PLY

If you're upgrading from an older version that used PLY:

### No Code Changes Required! 🎉

The new Lark-based parser is 100% backward compatible. Your existing code will work without any modifications.

### Only Dependency Changes

```bash
# Old (PLY-based)
pip install corpus-query-language==0.1.0

# New (Lark-based)
pip install corpus-query-language>=1.0.0
```

### What Changed Internally

- Parser implementation: PLY → Lark
- Grammar format: Python docstrings → EBNF `.lark` file
- No more generated files: `parser.out`, `parsetab.py`
- Better error messages
- Faster initialization

### Why We Changed

PLY (Python Lex-Yacc) is no longer actively maintained as a pip-installable package. Lark is:

- **Modern**: Active development with regular updates
- **Faster**: Optimized parsing algorithms
- **Cleaner**: Declarative grammar syntax
- **Better DX**: Superior debugging and error messages

See [ARCHITECTURE_PROPOSAL.md](ARCHITECTURE_PROPOSAL.md) for detailed technical analysis.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- Additional CQL operators and features
- Performance optimizations
- Documentation improvements
- Test coverage expansion
- Bug fixes

## 📄 License

This project is licensed under CC-BY-NC-SA-4.0. See LICENSE file for details.

## 🙏 Acknowledgments

- Original CQL implementation by Matthias Gille Levenson
- Lark parser by Erez Shinan
- All contributors to the project

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/matgille/CQL/issues)
- **Repository**: [GitHub](https://github.com/matgille/CQL)

## 📊 Project Status

[![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]()
[![License](https://img.shields.io/badge/license-CC--BY--NC--SA--4.0-blue)]()
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

**Version:** 1.0.0
**Last Updated:** 2025-01-21
