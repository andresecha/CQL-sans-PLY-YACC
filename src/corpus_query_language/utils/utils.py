"""Utility functions for the Corpus Query Language engine."""

import json
import logging
import re
from pathlib import Path
from typing import Any

from corpus_query_language.language.parser import CQLParser

logger = logging.getLogger(__name__)

# Type alias for query tuples
QueryTuple = tuple[str, str, str]
AnnotatedToken = dict[str, str]


def build_grammar(debug: bool, query: str) -> list[Any]:
    """Build an Abstract Syntax Tree from a CQL query.

    Args:
        debug: If True, outputs detailed parsing information.
        query: The CQL query string to parse.

    Returns:
        The Abstract Syntax Tree as a list of query elements.

    Raises:
        ValueError: If the query is empty or invalid.

    Examples:
        >>> ast = build_grammar(False, "[lemma='test']")
        >>> isinstance(ast, list)
        True
    """
    if not query or not query.strip():
        msg = "Query string cannot be empty"
        raise ValueError(msg)

    logger.debug(f"Building grammar for query: {query}")

    parser = CQLParser(debug=debug)
    ast = parser.parse(query)

    if debug:
        logger.debug(f"Generated AST: {ast}")

    return ast


def simple_match(query: QueryTuple, text_token: AnnotatedToken) -> bool:
    """Check if a simple query matches a token.

    This function compares a query tuple (annotation, operator, pattern) against
    a text token to determine if there's a match using regex.

    Args:
        query: A tuple containing (annotation_name, operator, regex_pattern).
               The operator can be '=' (equals) or '!=' (not equals).
        text_token: A dictionary of annotations for a single token.

    Returns:
        True if the query matches the token, False otherwise.

    Raises:
        KeyError: If the annotation is not present in the token.
        ValueError: If the query tuple is malformed.

    Examples:
        >>> token = {"lemma": "test", "pos": "NOUN"}
        >>> simple_match(("lemma", "=", "test"), token)
        True
        >>> simple_match(("lemma", "!=", "other"), token)
        True
    """
    if len(query) != 3:
        msg = f"Query tuple must have 3 elements, got {len(query)}"
        raise ValueError(msg)

    annotation, equality, regexp = query

    if annotation not in text_token:
        msg = f"Annotation '{annotation}' not found in token: {text_token}"
        raise KeyError(msg)

    # Compile the regex pattern with anchors
    try:
        compiled_regexp = re.compile(rf"^{regexp}$")
    except re.error as e:
        msg = f"Invalid regex pattern '{regexp}': {e}"
        raise ValueError(msg) from e

    # Check if the pattern matches
    token_value = text_token[annotation]
    matches = bool(re.match(compiled_regexp, token_value))

    # Apply equality operator
    if equality == "=":
        return matches
    if equality == "!=":
        return not matches

    msg = f"Invalid equality operator: {equality}"
    raise ValueError(msg)


def alternative_match(queries: list[QueryTuple], text_token: AnnotatedToken) -> bool:
    """Check if any of the alternative queries matches a token.

    This function tests multiple query alternatives (OR operation) against
    a single token.

    Args:
        queries: A list of query tuples to test.
        text_token: A dictionary of annotations for a single token.

    Returns:
        True if any query matches the token, False otherwise.

    Examples:
        >>> token = {"lemma": "test", "pos": "NOUN"}
        >>> queries = [("lemma", "=", "test"), ("lemma", "=", "other")]
        >>> alternative_match(queries, token)
        True
    """
    for query in queries:
        # Handle AND queries
        if isinstance(query, tuple) and query[0] == "and":
            all_matches = [simple_match(item, text_token) for item in query[1:]]
            if all(all_matches):
                return True
        # Handle simple queries
        elif isinstance(query, tuple) and len(query) == 3:
            try:
                if simple_match(query, text_token):
                    return True
            except (KeyError, ValueError) as e:
                logger.warning(f"Query match failed: {e}")
                continue
        else:
            logger.warning(f"Unexpected query format: {query}")
            continue

    return False


def import_corpus(path: str | Path) -> list[AnnotatedToken]:
    """Load a corpus from a JSON file.

    Args:
        path: Path to the JSON file containing the corpus.

    Returns:
        The corpus as a list of dictionaries, where each dictionary
        represents an annotated token.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
        ValueError: If the JSON structure is invalid.

    Examples:
        >>> # corpus = import_corpus("corpus.json")  # doctest: +SKIP
        >>> # len(corpus) > 0  # doctest: +SKIP
        True
    """
    corpus_path = Path(path)

    if not corpus_path.exists():
        msg = f"Corpus file not found: {corpus_path}"
        raise FileNotFoundError(msg)

    logger.info(f"Loading corpus from: {corpus_path}")

    try:
        with corpus_path.open(encoding="utf-8") as f:
            corpus = json.load(f)
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON in corpus file: {e}"
        raise json.JSONDecodeError(msg, e.doc, e.pos) from e

    if not isinstance(corpus, list):
        msg = f"Corpus must be a list, got {type(corpus).__name__}"
        raise ValueError(msg)

    logger.info(f"Loaded corpus with {len(corpus)} tokens")
    return corpus
