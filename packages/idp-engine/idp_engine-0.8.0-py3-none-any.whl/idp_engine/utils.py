# Copyright 2019 Ingmar Dasseville, Pierre Carbonnelle
#
# This file is part of Interactive_Consultant.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Various utilities (in particular, OrderedSet)
"""

from collections import ChainMap, Iterable
from json import JSONEncoder
import time

NEWL = "\n"
indented = "\n  "
BOOL = "Bool"
INT = "Int"
REAL = "Real"
DATE = "Date"
SYMBOL = "Symbol"

RELEVANT = "__relevant"
ARITY = "arity"
INPUT_DOMAIN = "input_domain"
OUTPUT_DOMAIN = "output_domain"
RESERVED_SYMBOLS = [RELEVANT, ARITY, INPUT_DOMAIN, OUTPUT_DOMAIN]

""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder.default  # Save unmodified default.
JSONEncoder.default = _default  # Replace it.


start = time.process_time()


def log(action):
    global start
    print("*** ", action, round(time.process_time()-start, 3))
    start = time.process_time()


class IDPZ3Error(Exception):
    """ raised whenever an error occurs in the conversion from AST to Z3 """
    pass


def unquote(s):
    if s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    return s


def in_list(q, ls):
    if not ls:
        return True  # e.g. for INT, REAL
    if len(ls) == 1:
        return q == ls[0]
    return Or([q == i for i in ls])


def is_number(s):
    if str(s) in ['True', 'False']:
        return False
    try:
        float(eval(str(s if not s.endswith('?') else s[:-1]))) # accepts "2/3" or "3.1415?"
        return True
    except:
        return False


def splitLast(l):
    return l[:-1], l[-1]


def applyTo(sym, arg):
    if len(arg) == 0:
        return sym
    return sym(arg)


def mergeDicts(l):
    # merge a list of dicts (possibly a comprehension
    return dict(ChainMap(*reversed(list(l))))

# OrderedSet  #############################################


class OrderedSet(dict):
    """
    a list of expressions without duplicates (first-in is selected)
    """
    def __init__(self, els=[]):
        assert isinstance(els, Iterable)
        super(OrderedSet, self).__init__(((el.code, el) for el in els))

    def append(self, el):
        if el not in self:
            self[el.code] = el

    def __iter__(self):
        return iter(self.values())  # instead of keys()

    def __contains__(self, expression):
        return super(OrderedSet, self).__contains__(expression.code)

    def extend(self, more):
        for el in more:
            self.append(el)

    # def items(self):
    #     return super(OrderedSet, self).items()

    # def popitem(self):
    #     return super(OrderedSet, self).popitem()

    def __or__(self, other: "OrderedSet") -> "OrderedSet":
        """returns the union of self and other.  Use: `self | other`.

        Returns:
            OrderedSet: the union of self and other
        """
        out = OrderedSet(self) # makes a copy
        out.extend(other)
        return out

    def __and__(self, other: "OrderedSet") -> "OrderedSet":
        """returns the intersection of self and other.  Use: `self & other`.

        Returns:
            OrderedSet: the intersection of self and other
        """
        out = OrderedSet({v for v in self if v in other})
        return out

    def __xor__(self, other: "OrderedSet") -> "OrderedSet":
        """returns the self minus other.  Use: `self ^ other`.

        Returns:
            OrderedSet: self minus other
        """
        out = OrderedSet({v for v in self if v not in other})
        return out
