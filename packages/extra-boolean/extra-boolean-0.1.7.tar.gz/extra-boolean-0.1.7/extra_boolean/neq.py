def neq(a, b):
  """Checks if antecedent ⇎ consequent (a ⇎ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> neq(true, false)  == true
    >>> neq(false, true)  == true
    >>> neq(true, true)   == false
    >>> neq(false, false) == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/neq
  """
  return a != b
