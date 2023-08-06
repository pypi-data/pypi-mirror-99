"""Pseudo tag and node definition for template literals."""

from typing import TextIO

from liquid.ast import Node
from liquid.context import Context
from liquid.stream import TokenStream
from liquid.tag import Tag

from liquid.token import Token
from liquid.token import TOKEN_LITERAL


class LiteralNode(Node):
    """Parse tree node for template literals."""

    __slots__ = ("tok",)

    def __init__(self, tok: Token):
        self.tok = tok

    def __str__(self) -> str:
        return self.tok.value

    def __repr__(self) -> str:  # pragma: no cover
        return f"LiteralNode(tok={self.tok})"

    def render_to_output(self, context: Context, buffer: TextIO):
        buffer.write(self.tok.value)


class Literal(Tag):
    """Pseudo "tag" for template literals."""

    name = TOKEN_LITERAL

    def parse(self, stream: TokenStream) -> LiteralNode:
        return LiteralNode(stream.current)
