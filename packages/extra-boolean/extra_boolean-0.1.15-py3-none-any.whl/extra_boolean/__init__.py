"""Boolean data type has two possible truth values to represent logic."""

# PARSE
from .parse import parse

# NOT, EQ, NEQ, IMPLY, NIMPLY (FIXED)
from .not_ import not_
from .eq import eq
from .neq import neq
from .imply import imply
from .nimply import nimply

# # AND, OR, XOR, NAND, NOR, XNOR (VARIABLE)
from .and_ import and_
from .or_ import or_
from .xor import xor
from .nand import nand
from .nor import nor
from .xnor import xnor

# # COUNT, SELECT (VARIABLE)
from .count import count
from .select import select
