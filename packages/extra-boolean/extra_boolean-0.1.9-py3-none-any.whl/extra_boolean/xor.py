def xor(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if odd no. of values are true. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> xor(true, false)             == true
    >>> xor(true, true)              == false
    >>> xor(true, true, true, false) == true
    >>> xor(true, true, true, true)  == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/xor
  """
  return a != b != c != d != e != f != g != h
