# -*- coding: utf-8 -*-
import ast
import attr
import pycodestyle
import tokenize
from collections import namedtuple
from functools import partial

__version__ = "1.0.0"


class KwOnlyArgsChecker(object):
    name = "flake8-kw-only-args"
    version = __version__
    visitor = attr.ib(init=False, default=attr.Factory(lambda: KwOnlyArgVisitor))

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    def run(self):
        try:
            self.lines = get_lines(self.filename)
        except IOError:
            yield
        noqa = get_noqa_lines(self.lines)

        visitor = KwOnlyArgVisitor(
            filename=self.filename,
            lines=self.lines,
        )
        visitor.visit(self.tree)
        for e in visitor.errors:
            if pycodestyle.noqa(self.lines[e.lineno - 1]):
                continue

            yield self.adapt_error(e)

    @classmethod
    def adapt_error(cls, e):
        """Adapts the extended error namedtuple to be compatible with Flake8."""
        return e._replace(message=e.message.format(*e.vars))[:4]


# TODO: simplify
error = namedtuple("error", "lineno col message type vars")
Error = partial(partial, error, type=KwOnlyArgsChecker, vars=())
K801 = Error(
    message="K801 positional parameters can accidentally set default kwargs; "
            "instead use kw-only args: def foo(*, key=value)."
)


def get_lines(filename):
    if filename in ("stdin", "-", None):
        return pycodestyle.stdin_get_value().splitlines(True)
    else:
        return pycodestyle.readlines(filename)


@attr.s
class KwOnlyArgVisitor(ast.NodeVisitor):
    filename = attr.ib()
    lines = attr.ib()
    errors = attr.ib(default=attr.Factory(list))

    def visit_AsyncFunctionDef(self, node):
        self.check_for_defaults(node)

    def visit_FunctionDef(self, node):
        self.check_for_defaults(node)

    def check_for_defaults(self, node):
        assert isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
        if node.args.defaults:
            self.errors.append(
                K801(
                    node.lineno,
                    node.col_offset
                )
            )


def get_noqa_lines(code):
    tokens = tokenize.generate_tokens(lambda L=iter(code): next(L))
    noqa = [
        x[2][0]
        for x in tokens
        if (
            x[0] == tokenize.COMMENT and
            (
                x[1].endswith("noqa") or
                (
                    isinstance(x[0], str) and x[0].endswith("noqa")
                )
            )
        )]
    return noqa
