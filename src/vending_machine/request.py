from dataclasses import dataclass

from vending_machine.money import Money


@dataclass
class Request:
    pass


@dataclass
class InsertMoneyRequest(Request):
    money: Money
