"""Money class for Japanese coins and bills.

TODO: refactoring
"""
from enum import IntEnum


class Money(IntEnum):
    """Money class for Japanese coins and bills."""

    Y0 = 0
    Y1 = 1
    Y5 = 5
    Y10 = 10
    Y50 = 50
    Y100 = 100
    Y500 = 500
    Y1000 = 1000
    Y2000 = 2000
    Y5000 = 5000
    Y10000 = 10000

    @staticmethod
    def members() -> list[int]:
        """[summary]

        Returns:
            list[int]: [description]
        """
        return [_.value for _ in Money.__members__.values()]
