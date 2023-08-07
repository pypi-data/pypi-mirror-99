from .eq import eq


def eqv(a, b):
  """Checks if antecedent ⇔ consequent (a ⇔ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> eqv(True, True)   == True
    >>> eqv(False, False) == True
    >>> eqv(True, False)  == False
    >>> eqv(False, True)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/eqv
  """
  return eq(a, b)
