from .and_ import and_


def nand(a=True, b=True, c=True, d=True, e=True, f=True, g=True, h=True):
  """Checks if any value is False. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> nand(True, False)             == True
    >>> nand(True, True)              == False
    >>> nand(True, True, False, True) == True
    >>> nand(True, True, True, True)  == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/nand
  """
  return not and_(a, b, c, d, e, f, g, h)
