"""This is vending machine class.  # TODO: refactoring
"""
from vending_machine.money import Money


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self):
        self.money_amount: int = 0

    def insert_money(self, money: Money):
        if not isinstance(money, Money):
            raise TypeError("this is not money.")

        self.money_amount += money.value

    def return_refund(self) -> list[Money]:
        refund = self.money_amount
        self.money_amount = 0
        return refund
