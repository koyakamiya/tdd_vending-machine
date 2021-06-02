from dataclasses import dataclass

from vending_machine.juice import Juice
from vending_machine.money import Money


@dataclass
class Request:
    pass


@dataclass
class InsertMoneyRequest(Request):
    money: Money


@dataclass
class RefundRequest(Request):
    pass


@dataclass
class SupplyJuiceRequest(Request):
    juice: Juice
    qty: int
