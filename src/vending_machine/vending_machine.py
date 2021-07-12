"""This is vending machine class.  # TODO: refactoring
"""
from collections import defaultdict
from enum import Enum, auto

from vending_machine.juice import Juice

# from vending_machine.juice_supplier import JuiceSupplier
from vending_machine.money import Money
from vending_machine.request import InsertMoneyRequest, RefundRequest, Request, SupplyJuiceRequest
from vending_machine.response import EmptyResponse, RefundResponse, Response, ReturnMoneyResponse


class VendingMachineStatus(Enum):
    """[summary]"""

    RETURN_NOTHING = auto()
    RETURN_UNACCEPTABLE_MONEY = auto()
    EMPTY_STOCK = auto()
    INSUFFICIENT_AMOUNT = auto()
    RETURN_JUICE_AND_REFUND = auto()


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    # def __init__(self, juice_supplier: JuiceSupplier):
    def __init__(self):
        """[summary]"""
        self.money_list: list[Money] = []
        self.unacceptable_money: Money = Money.Y0
        self.acceptable_money_kinds: set[Money] = {
            Money.Y10,
            Money.Y50,
            Money.Y100,
            Money.Y500,
            Money.Y1000,
        }

        self.stock: defaultdict[str, int] = defaultdict(int)
        # self.juice_supplier = juice_supplier

    def __call__(self, req: Request) -> Response:
        """[summary]

        Args:
            req (Request): [description]

        Raises:
            NotImplementedError: [description]
            NotImplementedError: [description]
            NotImplementedError: [description]

        Returns:
            Response: [description]
        """
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
            # TODO: 在庫の最大数チェック
            return EmptyResponse()

        raise NotImplementedError

    @property
    def money_amount(self) -> int:
        """[summary]

        Returns:
            int: [description]
        """
        return sum([_.value for _ in self.money_list])

    def check_status(self) -> VendingMachineStatus:
        """[summary]

        Returns:
            VendingMachineStatus: [description]
        """
        # TODO: Rename func name. This is only used at InsertMoneyRequest.
        if self.unacceptable_money != Money.Y0:
            return VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY
        return VendingMachineStatus.RETURN_NOTHING

    def is_available(self, juice: Juice) -> VendingMachineStatus:
        """[summary]

        Args:
            juice (Juice): [description]

        Returns:
            VendingMachineStatus: [description]
        """
        if self.stock[juice.name] == 0:
            return VendingMachineStatus.EMPTY_STOCK

        if self.money_amount < juice.price:
            return VendingMachineStatus.INSUFFICIENT_AMOUNT

        return VendingMachineStatus.RETURN_JUICE_AND_REFUND

    def accumulate_money(self, money: Money):
        """[summary]

        Args:
            money (Money): [description]

        Raises:
            TypeError: [description]
        """
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
        """[summary]

        Returns:
            list[Money]: [description]
        """
        refunds = self.money_list
        self.money_list = []
        return refunds

    def buy(self, juice_name: str) -> Juice:
        """[summary]

        Args:
            juice_name (str): [description]

        Returns:
            Juice: [description]
        """
        self.stock[juice_name] -= 1
        # TODO: money_listを減らす 6/23
        return self.juice_supplier[juice_name]

    def check_acceptable_money_kind(self, money: Money):
        """[summary]

        Args:
            money (Money): [description]

        Returns:
            [type]: [description]
        """
        return money in self.acceptable_money_kinds

    def supply_juice(self, juice: Juice, qty: int):
        """[summary]

        Args:
            juice (Juice): [description]
            qty (int): [description]
        """
        self.stock[juice.name] += qty
