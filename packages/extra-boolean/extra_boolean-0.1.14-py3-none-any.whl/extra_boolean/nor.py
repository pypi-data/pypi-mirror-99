from .or_ import or_


def nor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if all values are False. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> nor(False, False)               == True
    >>> nor(True, False)                == False
    >>> nor(False, False, False, False) == True
    >>> nor(False, False, True, False)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/nor
  """
  return not or_(a, b, c, d, e, f, g, h)
