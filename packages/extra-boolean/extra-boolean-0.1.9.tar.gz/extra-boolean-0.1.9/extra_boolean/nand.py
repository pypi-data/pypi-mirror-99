from .and_ import and_


def nand(a=True, b=True, c=True, d=True, e=True, f=True, g=True, h=True):
  """Checks if any value is false. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> nand(true, false)             == true
    >>> nand(true, true)              == false
    >>> nand(true, true, false, true) == true
    >>> nand(true, true, true, true)  == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/nand
  """
  return not and_(a, b, c, d, e, f, g, h)
