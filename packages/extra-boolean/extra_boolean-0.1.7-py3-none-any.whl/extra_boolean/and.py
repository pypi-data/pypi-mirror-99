def and(a=True, b=True, c=True, d=True, e=True, f=True, g=True, h=True):
  """Checks if all values are true. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> and(true, true)              == true
    >>> and(true, false)             == false
    >>> and(true, true, true, true)  == true
    >>> and(true, false, true, true) == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/and
  """
  return a and b and c and d and e and f and g and h
