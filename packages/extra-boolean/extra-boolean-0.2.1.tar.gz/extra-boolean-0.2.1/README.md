[Boolean] data type has two possible truth values to represent logic.<br>
📦 [PyPi](https://pypi.org/project/extra-boolean/),
📰 [Pdoc](https://python3f.github.io/extra-boolean/),
📘 [Wiki](https://github.com/python3f/extra-boolean/wiki).

Here is my implementation of digital logic gates in software. That includes
the basic gates [not_], [and_], [or_], [xor]; their complements [nand], [nor],
[xnor]; and 2 propositional logic (taught in discrete mathematics) gates
[imply], [eq]; and their complements [nimply], [neq]. There is also a
multiplexer, called [select], and a `True` counter, called [count]. [count]
can help you make custom gates, such as an *alternate* concept of **xnor**
which returns `True` only if all inputs are the same (standard [xnor] returns
`True` if even inputs are `True`). All of them can handle upto 8 inputs.

[parse] is influenced by ["boolean"] package, and is quite good at translating
`str` to `bool`. It can also handle double negatives, eg. `not inactive`.
You know the [and_] of 2-inputs, but what of 1-input? What of 0? And what of
the other gates? I answer them here.

> Stability: Experimental.

<br>

```python
from extra_boolean import *


parse("1")
parse("truthy")
parse("not off")
# True

parse("not true")
parse("inactive")
parse("disabled")
# False

imply(True, False)
# False

eq(False, False)
# True

xor(True, True, True)
# True

select(1, True, False, True)
# False           ^

count(True, False, True)
# 2    ^            ^
```

<br>
<br>


## Index

| Name     | Action                                     |
| -------- | ------------------------------------------ |
| [parse]  | Converts string to boolean.                |
| [not_]   | Checks if value is false.                  |
| [and_]   | Checks if all values are true.             |
| [or_]    | Checks if any value is true.               |
| [xor]    | Checks if odd no. of values are true.      |
| [nand]   | Checks if any value is false.              |
| [nor]    | Checks if all values are false.            |
| [xnor]   | Checks if even no. of values are true.     |
| [eq]     | Checks if antecedent ⇔ consequent (a ⇔ b). |
| [neq]    | Checks if antecedent ⇎ consequent (a ⇎ b). |
| [imply]  | Checks if antecedent ⇒ consequent (a ⇒ b). |
| [nimply] | Checks if antecedent ⇏ consequent (a ⇏ b). |
| [select] | Checks if ith value is true.               |
| [count]  | Counts no. of true values.                 |

<br>
<br>


## References

- [How to Build Your Very First Python Package](https://www.freecodecamp.org/news/build-your-first-python-package/)
- [Test Python package publishing with the Test Python Package Index](https://test.pypi.org)
- [How to use setup.py to install dependencies only?](https://stackoverflow.com/q/30797124/1413259)
- [install_requires vs requirements files](https://packaging.python.org/discussions/install-requires-vs-requirements/)
- [What does the “-U” option stand for in pip install -U](https://stackoverflow.com/a/12435220/1413259)
- [Getting Started With Testing in Python](https://realpython.com/python-testing/)
- [Import parent directory for brief tests](https://stackoverflow.com/a/11452413/1413259)
- [pytest: Most useful command-line options](https://docs.pytest.org/en/reorganize-docs/new-docs/user/commandlineuseful.html)
- [How to do relative imports in Python?](https://stackoverflow.com/a/7541369/1413259)
- [How do I use a keyword as a variable name?](https://stackoverflow.com/q/37968516/1413259)
- [pdoc: Auto-generate API documentation for Python projects](https://pdoc3.github.io/pdoc/)
- [Docstrings in Python](https://www.datacamp.com/community/tutorials/docstrings-python)
- [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [Twine is asking for my password each time : how to use the .pypirc](https://stackoverflow.com/a/57936053/1413259)
- [TravisCI: Building Pull Requests](https://docs.travis-ci.com/user/pull-requests/)
- [TravisCI: Building a Python Project](https://docs.travis-ci.com/user/languages/python/)
- [Creating a clean gh-pages branch](https://gist.github.com/ramnathv/2227408)
- [How to show only next line after the matched one?](https://stackoverflow.com/a/14310555/1413259)
- [How To Check If a Directory Exists In a Shell Script](https://www.cyberciti.biz/faq/howto-check-if-a-directory-exists-in-a-bash-shellscript/)
- [How do I trim leading and trailing whitespace from each line of some output?](https://unix.stackexchange.com/a/102229/166668)
- [Bash if..else Statement](https://linuxize.com/post/bash-if-else-statement/)

<br>
<br>

[![](https://img.youtube.com/vi/6mMK6iSZsAs/maxresdefault.jpg)](https://www.youtube.com/watch?v=6mMK6iSZsAs)

[Boolean]: https://realpython.com/python-boolean/#the-python-boolean-type
["boolean"]: https://www.npmjs.com/package/boolean
[parse]: https://github.com/python3f/extra-boolean/wiki/parse
[xor]: https://github.com/python3f/extra-boolean/wiki/xor
[not_]: https://github.com/python3f/extra-boolean/wiki/not_
[and_]: https://github.com/python3f/extra-boolean/wiki/and_
[or_]: https://github.com/python3f/extra-boolean/wiki/or_
[nand]: https://github.com/python3f/extra-boolean/wiki/nand
[nor]: https://github.com/python3f/extra-boolean/wiki/nor
[xnor]: https://github.com/python3f/extra-boolean/wiki/xnor
[eq]: https://github.com/python3f/extra-boolean/wiki/eq
[imply]: https://github.com/python3f/extra-boolean/wiki/imply
[nimply]: https://github.com/python3f/extra-boolean/wiki/nimply
[select]: https://github.com/python3f/extra-boolean/wiki/select
[count]: https://github.com/python3f/extra-boolean/wiki/count
[neq]: https://github.com/python3f/extra-boolean/wiki/neq
