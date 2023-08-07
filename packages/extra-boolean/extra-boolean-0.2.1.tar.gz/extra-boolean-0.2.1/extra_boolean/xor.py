def xor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if odd no. of values are True. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> xor(True, False)             == True
    >>> xor(True, True)              == False
    >>> xor(True, True, True, False) == True
    >>> xor(True, True, True, True)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/xor
  """
  return ((a != b) != (c != d)) != ((e != f) != (g != h))
