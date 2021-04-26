"""This is vending machine class.  # TODO: refactoring
"""
from vending_machine.money import Money


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self):
        self.money_amount: int = 0
        self.acceptable_monies: set[Money] = {
            Money.Y10,
            Money.Y50,
            Money.Y100,
            Money.Y500,
            Money.Y1000,
        }

    def insert_money(self, money: Money):
        if not isinstance(money, Money):
            raise TypeError("this is not money.")

        self.money_amount += money.value

    def refund(self) -> list[Money]:
        refund_value = self.money_amount
        self.money_amount = 0

        refunds = []
        # Memo: Step1 の状況には未対応
        for cur_money_member in sorted(Money.members())[::-1]:
            if refund_value >= cur_money_member:
                n_money = refund_value // cur_money_member
                refund_value -= cur_money_member * n_money
                refunds += [Money(cur_money_member)] * n_money

        return refunds

    def check_acceptable_money_kind(self, money: Money):
        return money in self.acceptable_monies
