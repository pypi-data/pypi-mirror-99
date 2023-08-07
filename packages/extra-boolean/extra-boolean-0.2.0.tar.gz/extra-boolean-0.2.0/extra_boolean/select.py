def select(i, a=False, b=False, c=False, d=False, e=False, f=False, g=False, h=False):
  """Checks if ith value is True. `📘`_

  - i: index
  - a: 1st boolean
  - b: 2nd boolean
  - ...

  Example:
    >>> select(0, True, False)              == True
    >>> select(1, True, False)              == False
    >>> select(1, True, True, False, False) == True
    >>> select(2, True, True, False, False) == False

  .. _📘:
    https://github.com/python3f/extra-boolean/wiki/select
  """
  if i == 0: return a
  elif i == 1: return b
  elif i == 2: return c
  elif i == 3: return d
  elif i == 4: return e
  elif i == 5: return f
  elif i == 6: return g
  elif i == 7: return h
  return False
