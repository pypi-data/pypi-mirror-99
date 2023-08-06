"""This module handles lists"""

import itertools

from typing import Any
from typing import List
from typing import Sequence
from typing import TypeVar

Unique = TypeVar("Unique")  # Generic type


# https://stackoverflow.com/a/25464724/500942
class Uniques(list):
    """A list of unique items

    Uniqueness is checked when appending to the list
    """

    def __init__(self, items=None):
        super().__init__([])
        self.extend(items or [])

    def predicate(self, _: Unique) -> bool:
        """Subclasses can exclude items which return False"""
        # pylint: disable=no-self-use
        return True

    def convert(self, item: Any) -> Unique:
        return item

    def append(self, item: Sequence) -> bool:
        if item in self:
            return False
        if not self.predicate(item):
            return False
        super().append(self.convert(item))
        return True

    def extend(self, items: Sequence) -> bool:
        result = False
        for item in items or []:
            if self.append(item):
                result = True
        return result


class UniquelyTrues(Uniques):
    """A unique list of items all being true-ish"""

    def predicate(self, item: Unique) -> bool:
        return bool(item)


def de_duplicate(items: List) -> List:
    """Remove any duplicate item, preserving order

    >>> assert de_duplicate([1, 9, 2, 8, 1, 7, 2]) == [1, 9, 2, 8, 7]
    """
    return list(Uniques(items))


def flatten(list_of_lists: List[List]) -> List:
    """Reduce a lists of lists to a list, comprehensively

    >>> assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to Alex Martelli at
        https://stackoverflow.com/a/952952/500942
    """
    return [item for list_ in list_of_lists for item in list_]


def flatten_(list_of_lists: List[List]) -> List:
    """Reduce a lists of lists to a list, functionally

    >>> assert flatten_([[1, 2], [3, 4]]) == [1, 2, 3, 4]

    Thanks to CTT at
        https://stackoverflow.com/a/716482/500942
    """
    return list(itertools.chain.from_iterable(list_of_lists))


def as_list(item):
    """Make item a list from types which can index, have items, or can pop"""
    # pylint: disable=pointless-statement
    try:
        item.index
        return list(item)
    except AttributeError:
        try:
            return list(item.items())
        except AttributeError:
            try:
                item.pop
                return list(item)
            except AttributeError:
                raise TypeError(f"Cannot make a list from {item!r}")
