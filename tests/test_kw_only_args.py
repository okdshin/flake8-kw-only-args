# -*- coding: utf-8 -*-
import ast
import unittest

from ddt import ddt, data, unpack

from flake8_kw_only_args import KwOnlyArgsChecker, KwOnlyArgVisitor


def check_code_for_non_kw_only_args(code):
    tree = ast.parse(code)
    code = [line + "\n" for line in code.split("\n")]
    visitor = KwOnlyArgVisitor(None, code)
    visitor.visit(tree)
    return [error for error in visitor.errors]


@ddt
class TestFlake8KwOnlyArgs(unittest.TestCase):
    @unpack
    @data(
        ("def positional(arg): ...", 0),
        ("def varargs(*args): ...", 0),
        ("def kwargs(**kwargs): ...", 0),
        ("def default(default=None): ...", 1),
        ("def positional_and_default(arg, default=None): ...", 1),
        ("def varargs_and_default(*args, default=None): ...", 0),
        ("def positional_and_varargs_and_default(arg, *args, default=None): ...", 0),
        ("def kwonlyargs(*, default=None): ...", 0),
        ("def positional_and_kwonlyargs(arg, *, default=None): ...", 0),
        ("def varargs_and_kwonlyargs(*args, default=None): ...", 0),
        ("def positional_and_varargs_and_kwonlyargs(arg, *args, default=None): ...", 0),
    )

    def test_kw_only_args(self, code, errors):
        result = check_code_for_non_kw_only_args(code)
        self.assertEqual(len(result), errors)

    def test_file_not_found(self):
        checker = KwOnlyArgsChecker(None, "foo")
        next(checker.run())


if __name__ == "__main__":
    unittest.main()
