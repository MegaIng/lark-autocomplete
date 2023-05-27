#!/usr/bin/env python3
from __future__ import annotations
"""
Simple program for playing with LarkCompleter within an interactive IPython environment
Coded May 2023 by David McNab at https://github.com/davidmcnabnz
Public domain, hope you find this useful, no warranty yada yada
"""
import sys, os, pathlib
import traceback
try:
    from IPython import embed
except ImportError:
    print("Failed to import IPython. Try 'pip install IPython' then try again")
    sys.exit(1)


from lark import Lark
from lark.indenter import PythonIndenter

from lark_autocomplete import LarkCompleter

THIS_FILE = pathlib.PosixPath(__file__).absolute()
THIS_STEM = THIS_FILE.as_posix().rsplit(".",1)[0]
GRAMMAR_PATH = THIS_STEM + ".lark"


class AutoCompleteTest:
    """
    For creating and launching an interactive IPython environment for
    playing around with Lark grammars and the helpful LarkCompleter object
    written by https://github.com/MegaIng
    """
    def __init__(self):
        try:
            self.reload()
        except:
            traceback.print_exc()
            print("Fix your grammar - something's up")

    def reload(self):
        self.parser = Lark.open(
            GRAMMAR_PATH,
            #rel_to=PROG_FILE,
            parser='lalr',
            #transformer=self.parserTransformer,
        )
        self.completer = LarkCompleter(self.parser)
        return self.parser, self.completer.complete

    def run(self):
        p = self.parser
        c = self.completer.complete
        r = self.reload
        print("Interactive IPython test environment.")
        print("Parser object is 'p', completer.complete() method is 'c'")
        print("Try the commands:")
        print("  c('')")
        print("  c('foo')")
        print("  c('foo b')")
        print("etc")
        print()
        print("ALSO - if you edit your grammar, you can reload it here by typing:")
        print("p, c = r()")
        print()
        print("Note - each of these calls to completer method 'c' returns a CompleteResult object")
        print("whose attribute 'token_options' is a set of legal token names which are legal in")
        print("the context of the entered line")
        embed()


def main():
    completerTest = AutoCompleteTest()
    completerTest.run()


if __name__ == '__main__':
    main()

