"""Core CQL Engine for executing queries against annotated corpora."""

import logging
from typing import Any

from corpus_query_language.engine import engine
from corpus_query_language.utils import utils

logger = logging.getLogger(__name__)


class CQLEngine:
    """Main CQL (Corpus Query Language) engine.

    This class provides the primary interface for executing CQL queries against
    annotated text corpora. It supports two main operations:
    - match: Check if a pattern exists (returns boolean)
    - findall: Find all occurrences of a pattern (returns list of spans)

    Examples:
        >>> engine = CQLEngine()
        >>> corpus = [
        ...     {"word": "The", "lemma": "the", "pos": "DET", "morph": ""},
        ...     {"word": "cat", "lemma": "cat", "pos": "NOUN", "morph": "Number=Sing"},
        ... ]
        >>> engine.match(corpus, "[lemma='cat']", verbose=False)
        True
        >>> spans = engine.findall(corpus, "[pos='NOUN']", verbose=False)
        >>> len(spans)
        1
    """

    def findall(
        self,
        corpus: list[dict[str, str]],
        query: str,
        verbose: bool = True,
        debug: bool = False,
    ) -> list[tuple[int, int]]:
        """Find all matches of a CQL query in a corpus.

        This method searches through the entire corpus and returns the positions
        (start, end) of all matching token sequences.

        Args:
            corpus: The annotated text as a list of dictionaries, where each
                   dictionary contains annotations (lemma, pos, morph, word).
            query: A CQL query string (e.g., "[lemma='rey']", "[pos='VERB' & lemma='ser']").
            verbose: If True, prints query results to stdout.
            debug: If True, enables detailed debug logging.

        Returns:
            A list of tuples, each containing (start_index, end_index) for matches.
            The indices are inclusive for start and exclusive for end.

        Raises:
            ValueError: If the query is invalid or empty.
            KeyError: If required annotations are missing from corpus tokens.

        Examples:
            >>> engine = CQLEngine()
            >>> corpus = [
            ...     {"word": "Da", "lemma": "dar", "pos": "VERB", "morph": ""},
            ...     {"word": "paz", "lemma": "paz", "pos": "NOUN", "morph": ""},
            ... ]
            >>> results = engine.findall(corpus, "[pos='NOUN']", verbose=False)
            >>> results
            [(1, 2)]
        """
        if not query or not query.strip():
            msg = "Query cannot be empty"
            raise ValueError(msg)

        if not corpus:
            logger.warning("Empty corpus provided to findall")
            return []

        logger.info(f"Executing findall query: {query}")

        try:
            query_ast = utils.build_grammar(debug=debug, query=query)
            result = engine.parse_corpus(query_ast, corpus, mode="find", debug=debug)
        except Exception as e:
            logger.error(f"Error executing findall query: {e}")
            raise

        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Query: {query}")
            if debug:
                print(f"AST: {query_ast}")
            print(f"Matches found: {len(result)}")
            if result:
                print("Spans:")
                for start, end in result:
                    print(f"  [{start}:{end}] -> {corpus[start:end]}")
            print("=" * 60)

        logger.info(f"Found {len(result)} matches")
        return result

    def match(
        self,
        corpus: list[dict[str, str]],
        query: str,
        verbose: bool = True,
        debug: bool = False,
    ) -> bool:
        """Check if a CQL query matches anywhere in a corpus.

        This method stops at the first match and returns True, making it more
        efficient than findall when you only need to know if a pattern exists.

        Args:
            corpus: The annotated text as a list of dictionaries, where each
                   dictionary contains annotations (lemma, pos, morph, word).
            query: A CQL query string (e.g., "[lemma='rey']", "[pos='VERB']").
            verbose: If True, prints query results to stdout.
            debug: If True, enables detailed debug logging.

        Returns:
            True if the query matches at least once, False otherwise.

        Raises:
            ValueError: If the query is invalid or empty.
            KeyError: If required annotations are missing from corpus tokens.

        Examples:
            >>> engine = CQLEngine()
            >>> corpus = [
            ...     {"word": "test", "lemma": "test", "pos": "NOUN", "morph": ""},
            ... ]
            >>> engine.match(corpus, "[lemma='test']", verbose=False)
            True
            >>> engine.match(corpus, "[lemma='other']", verbose=False)
            False
        """
        if not query or not query.strip():
            msg = "Query cannot be empty"
            raise ValueError(msg)

        if not corpus:
            logger.warning("Empty corpus provided to match")
            return False

        logger.info(f"Executing match query: {query}")

        try:
            query_ast = utils.build_grammar(debug=debug, query=query)
            result = engine.parse_corpus(query_ast, corpus, mode="match", debug=debug)
        except Exception as e:
            logger.error(f"Error executing match query: {e}")
            raise

        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Query: {query}")
            if debug:
                print(f"AST: {query_ast}")
            print(f"Match: {result}")
            print("=" * 60)

        logger.info(f"Match result: {result}")
        return result
