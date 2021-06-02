"""This is vending machine class.  # TODO: refactoring
"""
from collections import defaultdict
from enum import Enum, auto

from vending_machine.juice import Juice
from vending_machine.money import Money
from vending_machine.request import InsertMoneyRequest, RefundRequest, Request, SupplyJuiceRequest
from vending_machine.response import EmptyResponse, RefundResponse, Response, ReturnMoneyResponse


class VendingMachineStatus(Enum):
    RETURN_NOTHING = auto()
    RETURN_UNACCEPTABLE_MONEY = auto()


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self):
        self.money_list: list[Money] = []
        self.unacceptable_money: Money = Money.Y0
        self.acceptable_money_kinds: set[Money] = {
            Money.Y10,
            Money.Y50,
            Money.Y100,
            Money.Y500,
            Money.Y1000,
        }

        self.stock = defaultdict(int)

    def __call__(self, req: Request) -> Response:
        # NOTE: request と response を分ける

        # requestの処理
        if isinstance(req, InsertMoneyRequest):
            self.accumulate_money(req.money)
        elif isinstance(req, RefundRequest):
            pass
        elif isinstance(req, SupplyJuiceRequest):
            self.supply_juice(req.juice, req.qty)
        else:
            raise NotImplementedError

        # responseの処理
        if isinstance(req, InsertMoneyRequest):
            # TODO: ジュースを返すケースを考える
            status = self.check_status()
            if status == VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY:
                return ReturnMoneyResponse(self.return_money())
            elif status == VendingMachineStatus.RETURN_NOTHING:
                return EmptyResponse()
            else:
                raise NotImplementedError
        if isinstance(req, RefundRequest):
            return RefundResponse(self.refund())
        if isinstance(req, SupplyJuiceRequest):
            return EmptyResponse()

        raise NotImplementedError

    @property
    def money_amount(self) -> int:
        return sum([_.value for _ in self.money_list])

    def check_status(self) -> VendingMachineStatus:
        if self.unacceptable_money != Money.Y0:
            return VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY
        return VendingMachineStatus.RETURN_NOTHING

    def accumulate_money(self, money: Money):
        if not isinstance(money, Money):
            raise TypeError("this is not money.")

        if self.check_acceptable_money_kind(money):
            self.money_list.append(money)
        else:
            self.unacceptable_money = money

    def return_money(self) -> Money:
        """Return unacceptable money."""
        money = self.unacceptable_money
        self.unacceptable_money = Money.Y0
        return money

    def refund(self) -> list[Money]:
        refunds = self.money_list
        self.money_list = []
        return refunds

    def check_acceptable_money_kind(self, money: Money):
        return money in self.acceptable_money_kinds

    def supply_juice(self, juice: Juice, qty: int):
        self.stock[juice.name] += qty
