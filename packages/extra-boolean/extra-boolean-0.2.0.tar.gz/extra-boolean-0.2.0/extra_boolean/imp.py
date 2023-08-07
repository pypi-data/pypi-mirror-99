from .imply import imply


def imp(a, b):
  """Checks if antecedent ⇒ consequent (a ⇒ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> imp(True, True)   == True
    >>> imp(False, True)  == True
    >>> imp(False, False) == True
    >>> imp(True, False)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/imp
  """
  return imply(a, b)
