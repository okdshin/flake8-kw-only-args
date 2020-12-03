# flake8-kw-only-args

A [flake8](http://flake8.pycqa.org/en/latest/) plugin that checks for default
arguments like:

```python
def default(key=value):
    ...
```

Positional parameters can unintentionally override these arguments.  Instead
use the safer kw-only argument equivalent:

```python
def kw_only(*, key=value):
    ...
```

## Install

Install with `pip`:

```ShellSession
$ pip install flake8-kw-only-args
```

You can check that `flake8` has picked it up by looking for `flake8-kw-only-args`
in the output of `--version`:

```ShellSession
$ flake8 --version
2.6.2 (pycodestyle: 2.0.0, flake8-kw-only-args: 1.0.0, pyflakes: 1.2.3, mccabe: 0.5.0) CPython 2.7.11+ on Linux
```


## Warnings

This plugin add new flake8 warning:

- `K801`: non-kw-only argument


## Requirements

* Python 3.x (tested on 3.5, 3.6, and 3.7)
* flake8 or pycodestyle


# References

* [PEP 3102 -- Keyword-Only Arguments](https://www.python.org/dev/peps/pep-3102/)


## Licence

BSD license
