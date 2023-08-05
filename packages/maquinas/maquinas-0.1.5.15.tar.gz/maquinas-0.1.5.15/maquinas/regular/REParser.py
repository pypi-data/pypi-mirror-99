#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu, leftrec, nomemo
from tatsu.parsing import leftrec, nomemo  # noqa
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class REBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(REBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class REParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re=None,
        eol_comments_re=None,
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=REBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(REParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    @nomemo
    def _start_(self):  # noqa
        self._union_()
        self._check_eof()

    @tatsumasu()
    @leftrec
    def _union_(self):  # noqa
        with self._choice():
            with self._option():
                self._union_()
                self._token('+')
                self._cut()
                self._concat_()
            with self._option():
                self._concat_()
            self._error('no available options')

    @tatsumasu()
    @leftrec
    def _concat_(self):  # noqa
        with self._choice():
            with self._option():
                self._concat_()
                self._cut()
                self._kleene_()
            with self._option():
                self._kleene_()
            self._error('no available options')

    @tatsumasu()
    @leftrec
    def _kleene_(self):  # noqa
        with self._choice():
            with self._option():
                self._kleene_()
                self._token('*')
            with self._option():
                self._factor_()
            self._error('no available options')

    @tatsumasu()
    def _factor_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('(')
                self._cut()
                self._union_()
                self.name_last_node('@')
                self._token(')')
            with self._option():
                self._basic_()
            self._error('no available options')

    @tatsumasu()
    def _basic_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('epsilon')
            with self._option():
                self._token('empty')
            with self._option():
                self._token('ε')
            with self._option():
                self._token('∅')
            with self._option():
                self._pattern('\\w')
            with self._option():
                self._pattern('[\\$#@.<>\\-\\/#_]')
            with self._option():
                self._pattern('"[^"]+"')
            self._error('no available options')


class RESemantics(object):
    def start(self, ast):  # noqa
        return ast

    def union(self, ast):  # noqa
        return ast

    def concat(self, ast):  # noqa
        return ast

    def kleene(self, ast):  # noqa
        return ast

    def factor(self, ast):  # noqa
        return ast

    def basic(self, ast):  # noqa
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'start'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = REParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, REParser, name='RE')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
