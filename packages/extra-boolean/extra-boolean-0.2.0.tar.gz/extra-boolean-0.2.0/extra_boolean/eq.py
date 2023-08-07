def eq(a, b):
  """Checks if antecedent ⇔ consequent (a ⇔ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> eq(True, True)   == True
    >>> eq(False, False) == True
    >>> eq(True, False)  == False
    >>> eq(False, True)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/eq
  """
  return a == b
