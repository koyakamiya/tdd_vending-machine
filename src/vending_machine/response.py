"""[summary]
"""
from dataclasses import dataclass
from typing import Optional

from vending_machine.juice import Juice
from vending_machine.money import Money


@dataclass
class Response:
    """[summary]"""

    pass


@dataclass
class ReturnMoneyResponse(Response):
    """[summary]

    Args:
        Response ([type]): [description]
    """

    money: Money


@dataclass
class RefundResponse(Response):
    """[summary]

    Args:
        Response ([type]): [description]
    """

    refunds: list[Money]


@dataclass
class BuyResponse(Response):
    """[summary]

    Args:
        Response ([type]): [description]
    """

    juice: Optional[Juice]
    refunds: Optional[list[Money]]
