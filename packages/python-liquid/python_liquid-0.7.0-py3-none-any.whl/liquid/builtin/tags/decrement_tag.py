"""Tag and node definition for the built-in "decrement" tag."""

import sys
from typing import TextIO

from liquid import ast
from liquid.context import Context
from liquid.lex import tokenize_identifier
from liquid.stream import TokenStream
from liquid.tag import Tag

from liquid.parse import expect
from liquid.parse import parse_unchained_identifier

from liquid.token import Token
from liquid.token import TOKEN_TAG
from liquid.token import TOKEN_EXPRESSION

TAG_DECREMENT = sys.intern("decrement")


class DecrementNode(ast.Node):
    """Parse tree node for the built-in "decrement" tag."""

    __slots__ = ("tok", "identifier")

    def __init__(self, tok: Token, identifier: str):
        self.tok = tok
        self.identifier = identifier

    def __str__(self) -> str:
        return f"{self.identifier} -= 1"

    def render_to_output(self, context: Context, buffer: TextIO):
        buffer.write(str(context.decrement(self.identifier)))


class DecrementTag(Tag):
    """The built-in "decrement" tag."""

    name = TAG_DECREMENT
    block = False

    def parse(self, stream: TokenStream) -> DecrementNode:
        expect(stream, TOKEN_TAG, value=TAG_DECREMENT)
        tok = stream.current
        stream.next_token()

        expect(stream, TOKEN_EXPRESSION)
        tokens = TokenStream(tokenize_identifier(stream.current.value))
        ident = parse_unchained_identifier(tokens)

        return DecrementNode(tok=tok, identifier=str(ident))
