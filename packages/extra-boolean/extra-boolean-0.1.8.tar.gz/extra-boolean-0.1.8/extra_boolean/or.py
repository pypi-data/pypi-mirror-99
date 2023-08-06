def or(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if any value is true. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> or(true, false)                == true
    >>> or(false, false)               == false
    >>> or(false, true, false, true)   == true
    >>> or(false, false, false, false) == false

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/or
  """
  return a or b or c or d or e or f or g or h
