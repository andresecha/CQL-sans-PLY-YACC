"""CQL Parser using Lark.

This module replaces the PLY-based parser with a modern Lark implementation
while maintaining the same AST output format for backward compatibility.
"""

import logging
from pathlib import Path
from typing import Any

from lark import Lark, Transformer, v_args, Token, Tree

logger = logging.getLogger(__name__)

# Path to grammar file
GRAMMAR_FILE = Path(__file__).parent / "grammar.lark"


class ASTTransformer(Transformer):
    """Transform Lark parse tree into CQL AST.

    This transformer converts the Lark parse tree into the same AST format
    used by the original PLY-based parser, ensuring backward compatibility.

    The AST format consists of tuples representing queries:
    - Simple query: (annotation, operator, value)
      Example: ('lemma', '=', 'casa')

    - AND query: ('and', query1, query2, ...)
      Example: ('and', ('lemma', '=', 'casa'), ('pos', '=', 'NOUN'))

    - OR query: ('or', query1, query2)
      Example: ('or', ('lemma', '=', 'casa'), ('lemma', '=', 'hogar'))

    - Distance: ('distance', (min, max))
      Example: ('distance', (0, 3))

    - Optional: ('?', query)
      Example: ('?', ('pos', '=', 'ADV'))

    Examples:
        >>> transformer = ASTTransformer()
        >>> # Used internally by Lark parser
    """

    @v_args(inline=True)
    def equals_query(self, annotation: Token, equal_op: Token, value: Token) -> tuple[str, str, str]:
        """Transform equals query: annotation='value'.

        Args:
            annotation: The annotation type (lemma, pos, morph, word).
            equal_op: The equals operator token (=).
            value: The value to match (in quotes).

        Returns:
            Tuple of (annotation, '=', value).

        Examples:
            >>> # [lemma='casa'] -> ('lemma', '=', 'casa')
        """
        return (str(annotation), "=", self._clean_value(value))

    @v_args(inline=True)
    def not_equals_query(self, annotation: Token, notequal_op: Token, value: Token) -> tuple[str, str, str]:
        """Transform not-equals query: annotation!='value'.

        Args:
            annotation: The annotation type (lemma, pos, morph, word).
            notequal_op: The not-equals operator token (!=).
            value: The value to not match (in quotes).

        Returns:
            Tuple of (annotation, '!=', value).

        Examples:
            >>> # [pos!='PUNCT'] -> ('pos', '!=', 'PUNCT')
        """
        return (str(annotation), "!=", self._clean_value(value))

    def and_query(self, items: list[Any]) -> tuple[str, ...]:
        """Transform AND query: atom & atom & ...

        Args:
            items: List of query atoms and AND tokens to combine.

        Returns:
            Tuple starting with 'and' followed by all query atoms (tokens filtered).

        Examples:
            >>> # [lemma='casa' & pos='NOUN'] -> ('and', ('lemma', '=', 'casa'), ('pos', '=', 'NOUN'))
        """
        # Filter out AND tokens, keep only query atoms
        atoms = [item for item in items if not isinstance(item, Token)]
        return ("and",) + tuple(atoms)

    def optional_query(self, items: list[Any]) -> tuple[str, Any]:
        """Transform optional query: query?

        Args:
            items: List containing the optional query.

        Returns:
            Tuple of ('?', query).

        Examples:
            >>> # [pos='ADV']? -> ('?', ('pos', '=', 'ADV'))
        """
        return ("?", items[0])

    def distance_query(self, items: list[Any]) -> list[Any]:
        """Transform distance query: query[]{n,m}query.

        Args:
            items: List containing [query1, distance_token, query2].

        Returns:
            List of [query1, ('distance', (min, max)), query2].

        Examples:
            >>> # [pos='DET'][]{0,3}[pos='NOUN']
            >>> # -> [('pos', '=', 'DET'), ('distance', (0, 3)), ('pos', '=', 'NOUN')]
        """
        query1, distance_token, query2 = items
        min_dist, max_dist = self._parse_distance(distance_token)
        return [query1, ("distance", (min_dist, max_dist)), query2]

    def or_query(self, items: list[Any]) -> tuple[str, ...]:
        """Transform OR query: (query | query).

        Args:
            items: List containing LPAREN, queries, OR tokens, and RPAREN.

        Returns:
            Tuple starting with 'or' followed by the alternatives (tokens filtered).

        Examples:
            >>> # ([lemma='casa' | lemma='hogar']) -> ('or', ('lemma', '=', 'casa'), ('lemma', '=', 'hogar'))
        """
        # Filter out tokens (LPAREN, OR, RPAREN), keep only queries
        queries = [item for item in items if not isinstance(item, Token)]
        return ("or",) + tuple(queries)

    def queries(self, items: list[Any]) -> list[Any]:
        """Transform list of queries into flat list.

        Args:
            items: List of parsed queries.

        Returns:
            Flattened list of all queries.

        Examples:
            >>> # [pos='DET'][pos='NOUN'] -> [('pos', '=', 'DET'), ('pos', '=', 'NOUN')]
        """
        result = []
        for item in items:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return result

    def query(self, items: list[Any]) -> Any:
        """Transform single query.

        Args:
            items: List containing the query.

        Returns:
            The query itself if single item, or list of items.
        """
        return items[0] if len(items) == 1 else items

    @v_args(inline=True)
    def bracketed_query(self, lbrack: Token, content: Any, rbrack: Token) -> Any:
        """Transform bracketed query [content].

        Args:
            lbrack: Left bracket token.
            content: The query content.
            rbrack: Right bracket token.

        Returns:
            The content itself (without brackets).
        """
        return content

    def query_content(self, items: list[Any]) -> Any:
        """Transform query content.

        Args:
            items: List containing the content.

        Returns:
            The content itself if single item, or list of items.
        """
        return items[0] if len(items) == 1 else items

    def simple_query(self, items: list[Any]) -> Any:
        """Transform simple query (for OR queries).

        Args:
            items: List containing the query.

        Returns:
            The query itself.
        """
        return items[0]

    def annotation(self, items: list[Token]) -> str:
        """Transform annotation token to string.

        Args:
            items: List containing the annotation token.

        Returns:
            String representation of the annotation.
        """
        return str(items[0])

    def distance(self, items: list[Token]) -> Token:
        """Pass through distance token.

        Args:
            items: List containing the distance token.

        Returns:
            The distance token.
        """
        return items[0]

    @staticmethod
    def _clean_value(value: Token) -> str:
        """Remove quotes from value token.

        Args:
            value: Token containing a quoted value.

        Returns:
            The value without surrounding quotes.

        Examples:
            >>> _clean_value("'casa'") -> "casa"
        """
        s = str(value)
        return s[1:-1] if s.startswith("'") and s.endswith("'") else s

    @staticmethod
    def _parse_distance(distance_token: Token) -> tuple[int, int]:
        """Parse distance token []{min,max} to (min, max).

        Args:
            distance_token: Token containing distance specification.

        Returns:
            Tuple of (min_distance, max_distance).

        Examples:
            >>> _parse_distance("[]{0,3}") -> (0, 3)
            >>> _parse_distance("[]{,5}") -> (0, 5)
        """
        s = str(distance_token)
        # Extract numbers from []{min,max}
        # Remove [] and {}
        numbers_part = s.split("]")[-1][1:-1]
        min_str, max_str = numbers_part.split(",")

        # Handle empty min (defaults to 0)
        min_val = int(min_str.strip()) if min_str.strip() else 0
        max_val = int(max_str.strip())

        return (min_val, max_val)


class CQLParser:
    """CQL Parser using Lark.

    This parser replaces the PLY-based parser with a modern Lark implementation
    while maintaining the same AST output format for backward compatibility.

    The parser uses LALR(1) algorithm by default, which is fast and sufficient
    for the CQL grammar. If needed, can be switched to Earley parser for more
    complex grammars.

    Attributes:
        debug: Whether debug mode is enabled.
        parser: The Lark parser instance.

    Examples:
        >>> parser = CQLParser()
        >>> ast = parser.parse("[lemma='test']")
        >>> print(ast)
        [('lemma', '=', 'test')]

        >>> ast = parser.parse("[pos='DET'][pos='NOUN']")
        >>> print(ast)
        [('pos', '=', 'DET'), ('pos', '=', 'NOUN')]
    """

    def __init__(self, debug: bool = False) -> None:
        """Initialize the CQL parser.

        Args:
            debug: If True, enables debug mode with verbose logging.

        Raises:
            FileNotFoundError: If grammar file is not found.
            Exception: If grammar parsing fails.
        """
        self.debug = debug

        # Load grammar file
        if not GRAMMAR_FILE.exists():
            msg = f"Grammar file not found: {GRAMMAR_FILE}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with GRAMMAR_FILE.open(encoding="utf-8") as f:
            grammar = f.read()

        # Create Lark parser with LALR algorithm
        # LALR(1) is fast and handles CQL grammar well
        # Can switch to 'earley' if more power is needed
        try:
            self.parser = Lark(
                grammar,
                parser='lalr',
                transformer=ASTTransformer(),
                start='start',
                debug=debug,
            )
            logger.info("CQL Parser initialized successfully with Lark")
        except Exception as e:
            logger.error(f"Failed to initialize parser: {e}")
            raise

    def parse(self, query: str) -> list[Any]:
        """Parse a CQL query string into an AST.

        Args:
            query: The CQL query string to parse.

        Returns:
            The Abstract Syntax Tree as a list of query elements.

        Raises:
            ValueError: If the query is empty or has invalid syntax.

        Examples:
            >>> parser = CQLParser()
            >>> ast = parser.parse("[pos='NOUN']")
            >>> ast
            [('pos', '=', 'NOUN')]

            >>> ast = parser.parse("[lemma='casa' & pos='NOUN']")
            >>> ast[0][0]
            'and'
        """
        if not query or not query.strip():
            msg = "Query string cannot be empty"
            logger.error(msg)
            raise ValueError(msg)

        if self.debug:
            logger.debug(f"Parsing query: {query}")

        try:
            # Parse and transform to AST
            ast = self.parser.parse(query)

            if self.debug:
                logger.debug(f"Generated AST: {ast}")

            return ast

        except Exception as e:
            error_msg = f"Invalid CQL syntax in query '{query}': {e}"
            logger.error(error_msg)
            raise ValueError(error_msg) from e


def build_grammar(debug: bool, query: str) -> list[Any]:
    """Build an Abstract Syntax Tree from a CQL query.

    This is a compatibility function that maintains the same interface
    as the original PLY-based implementation.

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

        >>> ast = build_grammar(False, "[pos='VERB']")
        >>> ast
        [('pos', '=', 'VERB')]
    """
    parser = CQLParser(debug=debug)
    return parser.parse(query)


# For backward compatibility with old imports
Parser = CQLParser
