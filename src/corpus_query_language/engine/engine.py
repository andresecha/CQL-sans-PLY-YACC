"""Query execution engine for matching CQL queries against corpus data."""

import logging
from typing import Any

from corpus_query_language.utils import utils

logger = logging.getLogger(__name__)

# Annotation types supported by the engine
ANNOTATION_TYPES = ["lemma", "pos", "morph", "word"]


def parse_corpus(
    ast: list[Any], corpus: list[dict[str, str]], mode: str, debug: bool = False
) -> bool | list[tuple[int, int]]:
    """Parse a corpus using an Abstract Syntax Tree.

    This is the main query execution engine that matches an AST against a corpus
    to find matching sequences of tokens.

    Args:
        ast: The Abstract Syntax Tree to match against the corpus.
        corpus: The corpus as a list of annotated token dictionaries.
        mode: Query mode - either "match" (returns bool) or "find" (returns list of spans).
        debug: If True, enables debug logging.

    Returns:
        - If mode is "match": Returns True if any match is found, False otherwise.
        - If mode is "find": Returns a list of (start, end) tuples for all matches.

    Raises:
        ValueError: If mode is not "match" or "find".
        KeyError: If required annotations are missing from tokens.

    Examples:
        >>> ast = [("lemma", "=", "test")]
        >>> corpus = [{"lemma": "test", "pos": "NOUN", "word": "test", "morph": ""}]
        >>> parse_corpus(ast, corpus, "match")
        True
    """
    if mode not in ("match", "find"):
        msg = f"Invalid mode: {mode}. Must be 'match' or 'find'"
        raise ValueError(msg)

    if not corpus:
        logger.warning("Empty corpus provided")
        return False if mode == "match" else []

    if not ast:
        logger.warning("Empty AST provided")
        return False if mode == "match" else []

    text_index = 0
    tree_index = 0
    current_initial_state = 0
    first_matching_index: int | None = None
    all_spans: list[tuple[int, int]] = []

    ast_length = len(ast)
    corpus_length = len(corpus)

    if debug:
        logger.debug("AST contents:")
        for item in ast:
            logger.debug(f"  {item}")
        logger.debug(f"AST length: {ast_length}")
        logger.debug(f"Corpus length: {corpus_length}")

    # Text-directed parsing engine
    while text_index < corpus_length or tree_index == ast_length:
        # Check if we've matched the entire AST
        if tree_index == ast_length:
            all_spans.append((first_matching_index, text_index))
            if debug:
                logger.debug(f"Complete match: span ({first_matching_index}, {text_index})")

            if mode == "match":
                return True

            # Reset for next potential match
            text_index += 1
            tree_index = 0
            first_matching_index = None
            current_initial_state += 1
            continue

        # Check if we've reached the end of the corpus
        if text_index >= corpus_length:
            if debug:
                logger.debug("Reached end of corpus")
            break

        # Get current token and query
        current_token = corpus[text_index]
        current_query = ast[tree_index]
        operator = current_query[0] if isinstance(current_query, tuple) else None

        if debug:
            logger.debug("-" * 40)
            logger.debug(f"Token {text_index}: {current_token}")
            logger.debug(f"Tree index: {tree_index}/{ast_length}")
            logger.debug(f"Current query: {current_query}")

        # Handle different query operators
        if operator in ANNOTATION_TYPES:
            # Simple annotation match
            try:
                if utils.simple_match(current_query, current_token):
                    if debug:
                        logger.debug("Match found - advancing tree and text")
                    if first_matching_index is None:
                        first_matching_index = text_index
                    tree_index += 1
                    text_index += 1
                else:
                    if debug:
                        logger.debug("No match - resetting and advancing text")
                    tree_index = 0
                    current_initial_state += 1
                    text_index = current_initial_state
                    first_matching_index = None
            except KeyError as e:
                logger.error(f"Missing annotation in token: {e}")
                tree_index = 0
                current_initial_state += 1
                text_index = current_initial_state
                first_matching_index = None

        elif operator == "or":
            # Alternative match (OR operation)
            if utils.alternative_match(current_query[1:], current_token):
                if debug:
                    logger.debug("Alternative match found - advancing tree and text")
                if first_matching_index is None:
                    first_matching_index = text_index
                tree_index += 1
                text_index += 1
            else:
                if debug:
                    logger.debug("No alternative match - resetting")
                tree_index = 0
                current_initial_state += 1
                text_index = current_initial_state
                first_matching_index = None

        elif operator == "distance":
            # Distance operator (skip tokens)
            if debug:
                logger.debug(f"Distance operator: {current_query}")

            distance_range = current_query[1]
            min_distance, max_distance = distance_range
            submatch = False

            for i in range(min_distance, max_distance):
                if text_index >= corpus_length:
                    break

                next_query = ast[tree_index + 1] if tree_index + 1 < ast_length else None
                if next_query and utils.simple_match(next_query, corpus[text_index]):
                    if debug:
                        logger.debug(f"Distance match at offset {i}")
                    submatch = True
                    tree_index += 2  # Skip distance operator and matched query
                    text_index += 1
                    break

                text_index += 1

            if not submatch:
                if debug:
                    logger.debug("No distance match - resetting")
                tree_index = 0
                current_initial_state += 1
                text_index = current_initial_state
                first_matching_index = None

        elif operator == "and":
            # AND operator (all conditions must match)
            try:
                all_matches = [
                    utils.simple_match(item, current_token) for item in current_query[1:]
                ]

                if all(all_matches):
                    if debug:
                        logger.debug("AND match found - advancing tree and text")
                    if first_matching_index is None:
                        first_matching_index = text_index
                    tree_index += 1
                    text_index += 1
                else:
                    if debug:
                        logger.debug("AND match failed - resetting")
                    tree_index = 0
                    current_initial_state += 1
                    text_index = current_initial_state
                    first_matching_index = None
            except (KeyError, ValueError) as e:
                logger.error(f"Error in AND match: {e}")
                tree_index = 0
                current_initial_state += 1
                text_index = current_initial_state
                first_matching_index = None

        elif operator == "?":
            # Optional operator (zero or one match)
            try:
                if utils.alternative_match(current_query[1:], current_token):
                    if debug:
                        logger.debug("Optional match found - advancing tree and text")
                    if first_matching_index is None:
                        first_matching_index = text_index
                    tree_index += 1
                    text_index += 1
                else:
                    if debug:
                        logger.debug("Optional match not found - advancing tree only")
                    tree_index += 1  # Skip the optional query without advancing text
            except (KeyError, ValueError) as e:
                logger.warning(f"Error in optional match: {e}")
                tree_index += 1

        else:
            logger.warning(f"Unknown operator: {operator}")
            tree_index += 1

    # Return results based on mode
    if mode == "match":
        return len(all_spans) > 0

    return all_spans
