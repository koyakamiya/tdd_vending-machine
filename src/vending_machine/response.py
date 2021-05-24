from dataclasses import dataclass

from vending_machine.money import Money


@dataclass
class Response:
    pass


@dataclass
class ReturnMoneyResponse(Response):
    money: Money
