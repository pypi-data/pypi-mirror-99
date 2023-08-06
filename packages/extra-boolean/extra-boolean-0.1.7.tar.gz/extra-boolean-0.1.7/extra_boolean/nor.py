from .or import or


def nor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if all values are false. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> nor(false, false)               == true
    >>> nor(true, false)                == false
    >>> nor(false, false, false, false) == true
    >>> nor(false, false, true, false)  == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/nor
  """
  return not or(a, b, c, d, e, f, g, h)
