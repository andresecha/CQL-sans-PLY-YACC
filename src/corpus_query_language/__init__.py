"""Corpus Query Language - A powerful CQL engine for linguistic corpus queries.

This package provides a complete implementation of a Corpus Query Language (CQL)
engine for querying annotated text corpora. It supports pattern matching over
linguistic annotations such as lemmas, parts of speech, morphological features,
and word forms.

Examples:
    Basic usage::

        import corpus_query_language as cql

        # Create engine
        engine = cql.CQLEngine()

        # Load corpus
        corpus = cql.utils.import_corpus("corpus.json")

        # Execute queries
        matches = engine.findall(corpus, "[lemma='test']")
        has_match = engine.match(corpus, "[pos='VERB']")
"""

from corpus_query_language import core, engine, language, utils
from corpus_query_language.core.core import CQLEngine

__version__ = "0.1.0"
__all__ = ["CQLEngine", "core", "engine", "language", "utils", "__version__"]
