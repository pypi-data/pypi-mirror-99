import re


def parse(s):
  """Converts string to boolean. `📘`_

  - s: a string

  Example:
    >>> parse("1")        == True
    >>> parse("truthy")   == True
    >>> parse("not off")  == True
    >>> parse("not True") == False
    >>> parse("inactive") == False
    >>> parse("disabled") == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/parse
  """
  rfal  = "(negati|never|refus|wrong|fal|off)|\\b(f|n|0)\\b"
  rneg = "\\b(nay|nah|no|dis|un|in)"
  f = re.search(rfal, s) is not None
  n = len(re.findall(rneg, s))%2 == 1
  return f == n
