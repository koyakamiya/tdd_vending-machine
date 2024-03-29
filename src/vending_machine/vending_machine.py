"""This is vending machine class.  # TODO: refactoring
"""
from collections import defaultdict
from enum import Enum, auto
from typing import Optional, Tuple

from vending_machine.juice import Juice
from vending_machine.juice_supplier import JuiceSupplier
from vending_machine.money import Money
from vending_machine.request import BuyRequest, InsertMoneyRequest, RefundRequest, Request, SupplyJuiceRequest
from vending_machine.response import BuyResponse, RefundResponse, Response, ReturnMoneyResponse


class VendingMachineStatus(Enum):
    """[summary]"""

    RETURN_NOTHING = auto()
    RETURN_UNACCEPTABLE_MONEY = auto()
    EMPTY_STOCK = auto()
    INSUFFICIENT_AMOUNT = auto()
    IS_AVAILABLE_JUICE = auto()


class BuyError(RuntimeError):
    """[summary]

    Args:
        RuntimeError ([type]): [description]
    """

    pass


class VendingMachine:
    """This is vending machine class.  # TODO: refactoring"""

    def __init__(self, juice_supplier: JuiceSupplier):
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
        self.juice_supplier = juice_supplier

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
        self._hundle_request(req)
        return self._get_response(req)

    def _hundle_request(self, req):
        if isinstance(req, InsertMoneyRequest):
            self.accumulate_money(req.money)
        elif isinstance(req, RefundRequest):
            pass
        elif isinstance(req, SupplyJuiceRequest):
            self.supply_juice(req.juice, req.qty)
        elif isinstance(req, BuyRequest):
            pass
        else:
            raise NotImplementedError

    def _get_response(self, req):
        if isinstance(req, InsertMoneyRequest):
            # TODO: ジュースを返すケースを考える
            status = self.check_status()
            if status == VendingMachineStatus.RETURN_UNACCEPTABLE_MONEY:
                return ReturnMoneyResponse(self.return_money())
            elif status == VendingMachineStatus.RETURN_NOTHING:
                return Response()
            else:
                raise NotImplementedError
        if isinstance(req, RefundRequest):
            return RefundResponse(self.refund())
        if isinstance(req, SupplyJuiceRequest):
            # TODO: 在庫の最大数チェック
            return Response()
        if isinstance(req, BuyRequest):
            try:
                juice, refunds = self.buy(req.juice_name)
                return BuyResponse(juice, refunds)
            except BuyError:
                return BuyResponse(None, None)

        raise NotImplementedError

    @property
    def money_amount(self) -> int:
        """[summary]

        Returns:
            int: [description]
        """
        return sum([_.value for _ in self.money_list])

    @property
    def available_drinks(self) -> set[str]:
        """[summary]

        Returns:
            set[str]: [description]
        """
        return {
            juice_name
            for juice_name in self.stock
            if self.is_available(self.juice_supplier(juice_name)) == VendingMachineStatus.IS_AVAILABLE_JUICE
        }

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

        return VendingMachineStatus.IS_AVAILABLE_JUICE

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

    def buy(self, juice_name: str) -> Tuple[Juice, Optional[list[Money]]]:
        """[summary]

        Args:
            juice_name (str): [description]

        Raises:
            BuyError: [description]
            BuyError: [description]

        Returns:
            Juice: [description]
        """
        # check
        if self.stock.get(juice_name, 0) <= 0:
            raise BuyError

        if self.money_amount < self.juice_supplier(juice_name).price:
            raise BuyError

        bought_juice = self.__buy(juice_name)
        min_juice_price = min([v for v in self.juice_supplier.name2price.values()])
        if min_juice_price <= self.money_amount:
            return bought_juice, None

        refunds, self.money_list = self.money_list, []
        return bought_juice, refunds

    def __buy(self, juice_name: str) -> Juice:
        """[summary]

        Args:
            juice_name (str): [description]

        Returns:
            Juice: [description]
        """

        def _allocate_coin(money_remain: int) -> Tuple[Money, int]:
            for money in sorted(Money.members())[::-1]:
                if money_remain >= money:
                    return Money(money), money_remain - money
            raise NotImplementedError

        self.stock[juice_name] -= 1

        juice = self.juice_supplier(juice_name)
        money_remain = self.money_amount - juice.price
        coins_remain = []
        while money_remain > 0:
            coin, money_remain = _allocate_coin(money_remain)
            coins_remain.append(coin)

        self.money_list = coins_remain

        return juice

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
