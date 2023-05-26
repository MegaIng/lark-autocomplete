from __future__ import annotations

from lark import Lark
from lark.indenter import PythonIndenter

from lark_autocomplete import LarkCompleter

GRAMMAR = """
start: cmd
cmd: FOO BAR foobar_arg?
foobar_arg: BAZ
  | BAM

FOO: "foo"
BAR: "bar"
BAZ: "baz"
BAM: "bam"
"""

# parser = Lark(GRAMMAR, parser="lalr")
parser = Lark.open_from_package("lark", "python.lark", ["grammars"], parser="lalr", postlex=PythonIndenter(),
                                start="single_input")

completer = LarkCompleter(parser)

print(completer.complete("def n ("))
