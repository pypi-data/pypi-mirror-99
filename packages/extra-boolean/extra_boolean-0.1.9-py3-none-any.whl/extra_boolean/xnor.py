from .xor import xor


def xnor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if even no. of values are true. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> xnor(true, true)               == true
    >>> xnor(false, true)              == false
    >>> xnor(true, true, false, false) == true
    >>> xnor(true, true, true, false)  == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/xnor
  """
  return not xor(a, b, c, d, e, f, g, h)
