from .xor import xor


def xnor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if even no. of values are True. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> xnor(True, True)               == True
    >>> xnor(False, True)              == False
    >>> xnor(True, True, False, False) == True
    >>> xnor(True, True, True, False)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/xnor
  """
  return not xor(a, b, c, d, e, f, g, h)
