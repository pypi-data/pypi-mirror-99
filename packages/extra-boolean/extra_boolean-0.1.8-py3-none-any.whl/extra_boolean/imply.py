def imply(a, b):
  """Checks if antecedent ⇒ consequent (a ⇒ b). `📘`_

  - a: antecedent
  - b: consequent

  Example:
    >>> imply(true, true)   == true
    >>> imply(false, true)  == true
    >>> imply(false, false) == true
    >>> imply(true, false)  == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/imply
  """
  return (not a) or b
