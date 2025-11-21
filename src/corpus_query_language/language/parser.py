"""Parser for building Abstract Syntax Trees from CQL queries using PLY."""

import logging
from typing import Any

import ply.yacc as yacc

from corpus_query_language.language.lexer import Lexer

logger = logging.getLogger(__name__)


class Parser(Lexer):
    """Parser that builds an Abstract Syntax Tree from tokenized CQL queries.

    This parser uses PLY (Python Lex-Yacc) to parse CQL queries and generate
    an Abstract Syntax Tree (AST) that can be executed by the query engine.

    Attributes:
        tokens: Inherited from Lexer class.
        lexer: The lexer instance used for tokenization.
        parser: The PLY parser instance.
        ast: The generated Abstract Syntax Tree.

    Examples:
        >>> from corpus_query_language.language.lexer import Lexer
        >>> lexer = Lexer()
        >>> lexer.tokenize("[lemma='test']")
        >>> parser = Parser(lexer, debug=False)
        >>> isinstance(parser.ast, list)
        True
    """

    tokens = Lexer.tokens

    def p_or_queries(self, p: Any) -> None:
        """Parse OR queries with alternatives.

        Grammar:
            queries : LPAREN query OR query RPAREN
            queries : queries LPAREN query OR query RPAREN

        Args:
            p: The parser production.
        """
        if len(p) == 6:
            p[0] = [("or", p[2], p[4])]
        else:
            p[0] = p[1] + [("or", p[3], p[5])]

    def p_queries(self, p: Any) -> None:
        """Parse a sequence of queries.

        Grammar:
            queries : query
            queries : queries query
            queries : queries DISTANCE query

        Args:
            p: The parser production.
        """
        if len(p) == 2:
            p[0] = [p[1]]  # Single query
        elif len(p) == 3:
            p[0] = p[1] + [p[2]]  # Append the new query to the list
        else:
            p[0] = p[1] + [("distance", p[2])] + [p[3]]

    def p_query(self, p: Any) -> None:
        """Parse a single query.

        Grammar:
            query : bracketed_query

        Args:
            p: The parser production.
        """
        p[0] = p[1]

    def p_bracketed_query(self, p: Any) -> None:
        """Parse a bracketed query.

        Grammar:
            bracketed_query : LSQBRACK query_content RSQBRACK

        Args:
            p: The parser production.
        """
        p[0] = p[2]

    def p_ling_equality(self, p: Any) -> None:
        """Parse linguistic equality/inequality expressions.

        Grammar:
            query_atom : LEMMA EQUAL VALUE
            query_atom : POS EQUAL VALUE
            query_atom : MORPH EQUAL VALUE
            query_atom : WORD EQUAL VALUE
            query_atom : LEMMA NOTEQUAL VALUE
            query_atom : POS NOTEQUAL VALUE
            query_atom : MORPH NOTEQUAL VALUE
            query_atom : WORD NOTEQUAL VALUE

        Args:
            p: The parser production.
        """
        annotation_type = p[1]
        operator = p[2]
        value = p[3]

        if operator == "=":
            p[0] = (annotation_type, "=", value)
        else:  # operator == "!="
            p[0] = (annotation_type, "!=", value)

    def p_subquery_and_subquery(self, p: Any) -> None:
        """Parse AND combinations of query atoms.

        Grammar:
            query_content : query_atom
            query_content : query_atom AND query_atom
            query_content : query_atom AND query_atom AND query_atom
            query_content : query_atom AND query_atom AND query_atom AND query_atom

        Args:
            p: The parser production.
        """
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = ("and", p[1], p[3])
        elif len(p) == 6:
            p[0] = ("and", p[1], p[3], p[5])
        elif len(p) == 8:
            p[0] = ("and", p[1], p[3], p[5], p[7])

    def p_one_or_zero(self, p: Any) -> None:
        """Parse optional (zero or one) query operator.

        Grammar:
            queries : queries query INTERROGATIVE

        Args:
            p: The parser production.
        """
        p[0] = p[1] + [("?", p[2])]

    def p_error(self, p: Any) -> None:
        """Handle parsing errors.

        Args:
            p: The problematic token, or None if at end of input.
        """
        if p:
            error_msg = f"Syntax error at '{p.value}' (line {p.lineno}, position {p.lexpos})"
            logger.error(error_msg)
        else:
            error_msg = "Syntax error: unexpected end of input"
            logger.error(error_msg)

    def __init__(self, lexer: Lexer, debug: bool = False) -> None:
        """Initialize the parser.

        Args:
            lexer: The lexer instance to use for tokenization.
            debug: If True, enables debug mode for the parser.

        Examples:
            >>> from corpus_query_language.language.lexer import Lexer
            >>> lexer = Lexer()
            >>> lexer.tokenize("[lemma='test']")
            >>> parser = Parser(lexer, debug=False)
        """
        self.lexer = lexer
        self.parser = yacc.yacc(module=self, start="queries", debug=debug)
        self.ast = self.parser.parse(lexer=self.lexer, tracking=True, debug=debug)

        if debug:
            logger.debug(f"Generated AST: {self.ast}")
