def neq(a, b):
  """Checks if antecedent ⇎ consequent (a ⇎ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> neq(True, False)  == True
    >>> neq(False, True)  == True
    >>> neq(True, True)   == False
    >>> neq(False, False) == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/neq
  """
  return a != b
