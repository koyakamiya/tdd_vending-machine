"""This is vending machine class.  # TODO: refactoring
"""
from vending_machine.money import Money


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self):
        pass

    def insert_money(self, money: Money):
        if not isinstance(money, Money):
            raise TypeError("this is not money.")
