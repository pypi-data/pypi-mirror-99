def or_(a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if any value is True. `📘`_

  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> or_(True, False)                == True
    >>> or_(False, False)               == False
    >>> or_(False, True, False, True)   == True
    >>> or_(False, False, False, False) == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/or
  """
  return a or b or c or d or e or f or g or h
