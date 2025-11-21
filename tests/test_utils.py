"""Tests for utility functions."""

import json
import tempfile
from pathlib import Path

import pytest

from corpus_query_language.utils import utils


class TestSimpleMatch:
    """Test suite for simple_match function."""

    def test_simple_match_equals(self):
        """Test simple_match with equals operator."""
        query = ("lemma", "=", "test")
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.simple_match(query, token) is True

    def test_simple_match_not_equals(self):
        """Test simple_match with not-equals operator."""
        query = ("lemma", "!=", "other")
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.simple_match(query, token) is True

    def test_simple_match_regex(self):
        """Test simple_match with regex pattern."""
        query = ("lemma", "=", "te.*")
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.simple_match(query, token) is True

    def test_simple_match_missing_annotation(self):
        """Test simple_match with missing annotation."""
        query = ("lemma", "=", "test")
        token = {"pos": "NOUN", "word": "test"}
        with pytest.raises(KeyError):
            utils.simple_match(query, token)

    def test_simple_match_invalid_query(self):
        """Test simple_match with invalid query format."""
        query = ("lemma", "test")  # Missing operator
        token = {"lemma": "test", "pos": "NOUN"}
        with pytest.raises(ValueError):
            utils.simple_match(query, token)


class TestAlternativeMatch:
    """Test suite for alternative_match function."""

    def test_alternative_match_single(self):
        """Test alternative_match with single query."""
        queries = [("lemma", "=", "test")]
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.alternative_match(queries, token) is True

    def test_alternative_match_multiple(self):
        """Test alternative_match with multiple alternatives."""
        queries = [("lemma", "=", "other"), ("lemma", "=", "test")]
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.alternative_match(queries, token) is True

    def test_alternative_match_no_match(self):
        """Test alternative_match when no alternatives match."""
        queries = [("lemma", "=", "other1"), ("lemma", "=", "other2")]
        token = {"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}
        assert utils.alternative_match(queries, token) is False


class TestImportCorpus:
    """Test suite for import_corpus function."""

    def test_import_corpus_valid(self):
        """Test import_corpus with valid JSON file."""
        corpus_data = [
            {"word": "test", "lemma": "test", "pos": "NOUN", "morph": ""},
            {"word": "word", "lemma": "word", "pos": "NOUN", "morph": ""},
        ]

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(corpus_data, f)
            temp_path = f.name

        try:
            corpus = utils.import_corpus(temp_path)
            assert len(corpus) == 2
            assert corpus[0]["word"] == "test"
        finally:
            Path(temp_path).unlink()

    def test_import_corpus_file_not_found(self):
        """Test import_corpus with non-existent file."""
        with pytest.raises(FileNotFoundError):
            utils.import_corpus("/nonexistent/path.json")

    def test_import_corpus_invalid_json(self):
        """Test import_corpus with invalid JSON."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                utils.import_corpus(temp_path)
        finally:
            Path(temp_path).unlink()


class TestBuildGrammar:
    """Test suite for build_grammar function."""

    def test_build_grammar_basic(self):
        """Test build_grammar with basic query."""
        query = "[lemma='test']"
        ast = utils.build_grammar(debug=False, query=query)
        assert isinstance(ast, list)
        assert len(ast) > 0

    def test_build_grammar_empty_query(self):
        """Test build_grammar with empty query."""
        with pytest.raises(ValueError):
            utils.build_grammar(debug=False, query="")

    def test_build_grammar_complex(self):
        """Test build_grammar with complex query."""
        query = "[lemma='test' & pos='NOUN']"
        ast = utils.build_grammar(debug=False, query=query)
        assert isinstance(ast, list)
        assert len(ast) > 0
