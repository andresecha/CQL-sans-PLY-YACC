"""Lexer for tokenizing CQL queries using PLY (Python Lex-Yacc)."""

import copy
import logging
from typing import Any

import ply.lex as lex

logger = logging.getLogger(__name__)


class Lexer:
    """Lexer that tokenizes CQL query strings.

    This lexer uses PLY (Python Lex-Yacc) to tokenize CQL queries into
    meaningful tokens that can be processed by the parser.

    Attributes:
        tokens: Tuple of valid token names.
        lexer: The PLY lexer instance (created during tokenization).

    Examples:
        >>> lexer = Lexer()
        >>> lexer.tokenize("[lemma='test']")
        >>> tok = lexer.token()
        >>> tok.type
        'LSQBRACK'
    """

    tokens = (
        "RANGE",
        "DISTANCE",
        "RPAREN",
        "LPAREN",
        "OR",
        "RSQBRACK",
        "LSQBRACK",
        "EQUAL",
        "AND",
        "QUOTE",
        "LEMMA",
        "POS",
        "MORPH",
        "NUMBER",
        "WORD",
        "NOTEQUAL",
        "INTERROGATIVE",
        "PLUS",
        "VALUE",
        "ASTERISK",
    )

    # Token rules
    t_OR = r"\|"
    t_LSQBRACK = r"\["
    t_RSQBRACK = r"\]"
    t_EQUAL = r"\="
    t_NOTEQUAL = r"\!="
    t_AND = r"&"
    t_INTERROGATIVE = r"\?"
    t_PLUS = r"\+"
    t_ASTERISK = r"\*"
    t_ignore = " \t"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"

    def t_DISTANCE(self, t: Any) -> Any:
        r"""\[\s*\]\{[0-9]*\s*,\s*[0-9]+\}"""
        range_str = t.value.split("]")[-1][1:-1].split(",")
        try:
            t.value = (int(range_str[0].strip()), int(range_str[1].strip()))
        except ValueError:
            # If first value is empty, default to 0
            t.value = (0, int(range_str[1].strip()))
        return t

    def t_RANGE(self, t: Any) -> Any:
        r"""\{[0-9]*\s*,\s*[0-9]+\}"""
        numbers = t.value[1:-1].split(",")
        try:
            t.value = (int(numbers[0].strip()), int(numbers[1].strip()))
        except ValueError:
            # If first value is empty, default to 0
            t.value = (0, int(numbers[1].strip()))
        return t

    def t_LEMMA(self, t: Any) -> Any:
        r"""lemma"""
        return t

    def t_POS(self, t: Any) -> Any:
        r"""pos"""
        return t

    def t_MORPH(self, t: Any) -> Any:
        r"""morph"""
        return t

    def t_WORD(self, t: Any) -> Any:
        r"""word"""
        return t

    def t_VALUE(self, t: Any) -> Any:
        r"""'[^']+'"""
        # Remove quotes from value
        t.value = t.value[1:-1]
        return t

    def t_error(self, t: Any) -> None:
        """Handle lexing errors.

        Args:
            t: The problematic token.
        """
        logger.error(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
        t.lexer.skip(1)

    def tokenize(self, query: str, debug: bool = False) -> None:
        """Tokenize a CQL query string.

        Args:
            query: The CQL query string to tokenize.
            debug: If True, prints all tokens for debugging.

        Raises:
            ValueError: If the query string is empty.

        Examples:
            >>> lexer = Lexer()
            >>> lexer.tokenize("[lemma='test']")
        """
        if not query:
            msg = "Query string cannot be empty"
            raise ValueError(msg)

        self.lexer = lex.lex(module=self)
        self.lexer.input(query)

        if debug:
            logger.debug(f"Tokenizing query: {query}")
            debug_lexer = copy.deepcopy(self.lexer)
            while True:
                tok = debug_lexer.token()
                if not tok:
                    break
                logger.debug(f"Token: {tok}")

    def token(self) -> Any:
        """Get the next token from the lexer.

        Returns:
            The next token, or None if no more tokens are available.

        Examples:
            >>> lexer = Lexer()
            >>> lexer.tokenize("[lemma='test']")
            >>> tok = lexer.token()
            >>> tok.type
            'LSQBRACK'
        """
        if not hasattr(self, "lexer"):
            msg = "Lexer not initialized. Call tokenize() first."
            raise RuntimeError(msg)
        return self.lexer.token()
