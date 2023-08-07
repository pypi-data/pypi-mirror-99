def and_(a=True, b=True, c=True, d=True, e=True, f=True, g=True, h=True):
  """Checks if all values are True. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> and_(True, True)              == True
    >>> and_(True, False)             == False
    >>> and_(True, True, True, True)  == True
    >>> and_(True, False, True, True) == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/and
  """
  return a and b and c and d and e and f and g and h
