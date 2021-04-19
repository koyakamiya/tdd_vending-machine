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
        refund_value = self.money_amount
        self.money_amount = 0

        refunds = []
        # Memo: 異常系！
        for cur_money_member in sorted(Money.members())[::-1]:
            if refund_value >= cur_money_member:
                n_money = refund_value // cur_money_member
                refund_value -= cur_money_member * n_money
                refunds += [Money(cur_money_member)] * n_money

        return refunds