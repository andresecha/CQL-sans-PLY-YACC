"""Tests for the core CQLEngine class."""

import pytest

from corpus_query_language.core.core import CQLEngine


class TestCQLEngine:
    """Test suite for CQLEngine class."""

    def test_engine_initialization(self):
        """Test that CQLEngine can be initialized."""
        engine = CQLEngine()
        assert engine is not None

    def test_findall_basic_query(self, sample_corpus):
        """Test findall with a basic lemma query."""
        engine = CQLEngine()
        results = engine.findall(sample_corpus, "[lemma='rey']", verbose=False)
        assert len(results) == 1
        assert results[0] == (3, 4)

    def test_findall_pos_query(self, sample_corpus):
        """Test findall with a POS query."""
        engine = CQLEngine()
        results = engine.findall(sample_corpus, "[pos='NOUN']", verbose=False)
        assert len(results) == 2  # paz and rey

    def test_findall_no_match(self, sample_corpus):
        """Test findall when there are no matches."""
        engine = CQLEngine()
        results = engine.findall(sample_corpus, "[lemma='notfound']", verbose=False)
        assert len(results) == 0

    def test_findall_empty_corpus(self, empty_corpus):
        """Test findall with an empty corpus."""
        engine = CQLEngine()
        results = engine.findall(empty_corpus, "[lemma='test']", verbose=False)
        assert len(results) == 0

    def test_findall_invalid_query(self, sample_corpus):
        """Test findall with an invalid/empty query."""
        engine = CQLEngine()
        with pytest.raises(ValueError):
            engine.findall(sample_corpus, "", verbose=False)

    def test_match_found(self, sample_corpus):
        """Test match when pattern is found."""
        engine = CQLEngine()
        result = engine.match(sample_corpus, "[lemma='rey']", verbose=False)
        assert result is True

    def test_match_not_found(self, sample_corpus):
        """Test match when pattern is not found."""
        engine = CQLEngine()
        result = engine.match(sample_corpus, "[lemma='notfound']", verbose=False)
        assert result is False

    def test_match_empty_corpus(self, empty_corpus):
        """Test match with an empty corpus."""
        engine = CQLEngine()
        result = engine.match(empty_corpus, "[lemma='test']", verbose=False)
        assert result is False

    def test_match_invalid_query(self, sample_corpus):
        """Test match with an invalid/empty query."""
        engine = CQLEngine()
        with pytest.raises(ValueError):
            engine.match(sample_corpus, "", verbose=False)

    def test_findall_and_query(self, sample_corpus):
        """Test findall with AND operator."""
        engine = CQLEngine()
        results = engine.findall(sample_corpus, "[lemma='rey' & pos='NOUN']", verbose=False)
        assert len(results) == 1
        assert results[0] == (3, 4)

    def test_findall_regex_pattern(self, sample_corpus):
        """Test findall with regex pattern."""
        engine = CQLEngine()
        results = engine.findall(sample_corpus, "[lemma='re.*']", verbose=False)
        assert len(results) == 1  # Should match 'rey'

    def test_verbose_output(self, sample_corpus, capsys):
        """Test that verbose mode produces output."""
        engine = CQLEngine()
        engine.findall(sample_corpus, "[lemma='rey']", verbose=True)
        captured = capsys.readouterr()
        assert "Query:" in captured.out
        assert "[lemma='rey']" in captured.out
