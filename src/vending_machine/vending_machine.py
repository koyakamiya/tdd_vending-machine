"""This is vending machine class.  # TODO: refactoring
"""
from enum import Enum, auto

from vending_machine.money import Money
from vending_machine.request import InsertMoneyRequest, Request
from vending_machine.response import Response, ReturnMoneyResponse


class VendingMachineStatus(Enum):
    RETURN_NOTHING = auto()
    RETURN_UNACCEPTABLE_MONEY = auto()


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self):
        self.money_amount: int = 0
        self.unacceptable_money: Money = Money.Y0
        self.acceptable_money_kinds: set[Money] = {
            Money.Y10,
            Money.Y50,
            Money.Y100,
            Money.Y500,
            Money.Y1000,
        }

    def __call__(self, req: Request) -> Response:
        # NOTE: request と response を分ける

        # requestの処理
        if isinstance(req, InsertMoneyRequest):
            self.accumulate_money(req.money)
        else:
            raise NotImplementedError

        # responseの処理
        if isinstance(req, InsertMoneyRequest):
            # TODO: ジュースを返すケースを考える
            status = self.check_status()
            if status == VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY:
                return ReturnMoneyResponse(self.return_money())
            else:
                raise NotImplementedError

    def check_status(self) -> VendingMachineStatus:
        if self.unacceptable_money != Money.Y0:
            return VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY
        return VendingMachineStatus.RETURN_NOTHING

    def accumulate_money(self, money: Money):
        if not isinstance(money, Money):
            raise TypeError("this is not money.")

        if self.check_acceptable_money_kind(money):
            self.money_amount += money.value
        else:
            self.unacceptable_money = money

    def return_money(self) -> Money:
        """Return unacceptable money."""
        money = self.unacceptable_money
        self.unacceptable_money = Money.Y0
        return money

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
        return money in self.acceptable_money_kinds
