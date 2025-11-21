"""Pytest configuration and fixtures for CQL tests."""

import pytest


@pytest.fixture
def sample_corpus():
    """Provide a sample annotated corpus for testing."""
    return [
        {"word": "Da", "lemma": "dar", "pos": "VERB", "morph": "Mood=Imp"},
        {"word": "paz", "lemma": "paz", "pos": "NOUN", "morph": "Gender=Masc"},
        {"word": "al", "lemma": "al", "pos": "ADP", "morph": ""},
        {"word": "rey", "lemma": "rey", "pos": "NOUN", "morph": "Gender=Masc"},
        {"word": "santo", "lemma": "santo", "pos": "ADJ", "morph": "Gender=Masc"},
    ]


@pytest.fixture
def empty_corpus():
    """Provide an empty corpus for testing edge cases."""
    return []


@pytest.fixture
def single_token_corpus():
    """Provide a single-token corpus for testing."""
    return [{"word": "test", "lemma": "test", "pos": "NOUN", "morph": ""}]
