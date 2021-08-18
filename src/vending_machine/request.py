"""[summary]
"""
from dataclasses import dataclass

from vending_machine.juice import Juice
from vending_machine.money import Money


@dataclass
class Request:
    """[summary]"""

    pass


@dataclass
class InsertMoneyRequest(Request):
    """[summary]

    Args:
        Request ([type]): [description]
    """

    money: Money


@dataclass
class RefundRequest(Request):
    """[summary]

    Args:
        Request ([type]): [description]
    """

    pass


@dataclass
class SupplyJuiceRequest(Request):
    """[summary]

    Args:
        Request ([type]): [description]
    """

    juice: Juice
    qty: int


@dataclass
class BuyRequest(Request):
    """[summary]

    Args:
        Request ([type]): [description]
    """

    juice_name: str
