def imply(a, b):
  """Checks if antecedent ⇒ consequent (a ⇒ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> imply(True, True)   == True
    >>> imply(False, True)  == True
    >>> imply(False, False) == True
    >>> imply(True, False)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/imply
  """
  return (not a) or b
