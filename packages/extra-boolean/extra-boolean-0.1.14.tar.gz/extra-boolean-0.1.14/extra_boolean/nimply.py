from .imply import imply


def nimply(a, b):
  """Checks if antecedent ⇏ consequent (a ⇏ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> nimply(True, False)  == True
    >>> nimply(True, True)   == False
    >>> nimply(False, True)  == False
    >>> nimply(False, False) == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/nimply
  """
  return not imply(a, b)
