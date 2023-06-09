from __future__ import annotations

from dataclasses import dataclass

from lark import Lark, UnexpectedCharacters
from lark.parsers.lalr_interactive_parser import InteractiveParser


@dataclass
class CompleteResult:
    pos: int
    prefix: str
    token_options: set[str]


class LarkCompleter:
    def __init__(self, lark: Lark, start: str = None):
        if not lark.options.parser == "lalr":
            raise TypeError("The given Lark instance must be using the LALR(1) parser")
        self.parser = lark
        self.start = start

    def complete(self, text: str) -> CompleteResult:
        interactive = self.parser.parse_interactive(text, self.start)
        lex_stream = interactive.lexer_thread.lex(interactive.parser_state)
        while True:
            try:
                token = next(lex_stream)
            except StopIteration:
                break
            except UnexpectedCharacters as e:
                return self.compute_options_unexpected_char(interactive, text, e)
            interactive.feed_token(token)
        return self.compute_options_no_error(interactive, text)

    def compute_options_unexpected_char(self, interactive: InteractiveParser, text: str,
                                        e: UnexpectedCharacters) -> CompleteResult:
        prefix = text[e.pos_in_stream:]

        return CompleteResult(e.pos_in_stream, prefix, interactive.accepts())

    def compute_options_no_error(self, interactive: InteractiveParser, text: str) -> CompleteResult:
        return CompleteResult(len(text), "", interactive.accepts())
