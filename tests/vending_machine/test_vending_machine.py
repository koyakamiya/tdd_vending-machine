from collections import defaultdict

import pytest

from vending_machine.juice_supplier import JuiceSupplier
from vending_machine.money import Money
from vending_machine.request import InsertMoneyRequest, RefundRequest, SupplyJuiceRequest
from vending_machine.response import EmptyResponse, RefundResponse, ReturnMoneyResponse
from vending_machine.vending_machine import VendingMachine, VendingMachineStatus


@pytest.fixture
def vending_machine() -> VendingMachine:
    return VendingMachine()


def test_insert_money_into_vending_machine(vending_machine: VendingMachine):
    req = InsertMoneyRequest(money=Money.Y1)
    res: ReturnMoneyResponse = vending_machine(req)

    assert res.money == Money.Y1


def test_get_money_amount(vending_machine: VendingMachine):
    reqs = []
    reqs.append(InsertMoneyRequest(money=Money.Y100))
    reqs.append(InsertMoneyRequest(money=Money.Y10))
    reqs.append(InsertMoneyRequest(money=Money.Y10))

    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    assert vending_machine.money_amount == 120


def test_refund(vending_machine: VendingMachine):
    reqs = [InsertMoneyRequest(money=Money.Y10) for _ in range(6)]

    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    res: RefundResponse = vending_machine(RefundRequest())

    expected_refunds = [Money.Y10 for _ in range(6)]
    assert res.refunds == expected_refunds
    assert vending_machine.money_amount == 0


@pytest.mark.parametrize("money, is_available", [(Money.Y10, True), (Money.Y1, False)])
def test_is_acceptable_money_kind(money, is_available, vending_machine: VendingMachine):
    assert vending_machine.check_acceptable_money_kind(money) is is_available


def test_check_stock(vending_machine: VendingMachine):
    # NOTE: ここからリファクタ
    js = JuiceSupplier({"cola": 120})
    req = SupplyJuiceRequest(juice=js("cola"), qty=5)

    _: EmptyResponse = vending_machine(req)
    stock: defaultdict[str, int] = vending_machine.stock

    assert len(stock) == 1
    assert "cola" in stock.keys()
    assert stock["cola"] == 5
    assert js.name2price["cola"] == 120


def test_is_available(vending_machine: VendingMachine):
    js = JuiceSupplier({"cola": 120})
    reqs = [SupplyJuiceRequest(juice=js("cola"), qty=5), InsertMoneyRequest(money=Money.Y500)]
    # おかねいれる
    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    vending_machine.is_available(js("cola")) == VendingMachineStatus.RETURN_JUICE_AND_REFUND


def test_is_not_available_by_empty_stock(vending_machine: VendingMachine):
    js = JuiceSupplier({"cola": 120})
    reqs = [InsertMoneyRequest(money=Money.Y500)]
    # おかねいれる
    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    vending_machine.is_available(js("cola")) == VendingMachineStatus.EMPTY_STOCK


def test_is_not_available_by_insufficient_amount(vending_machine: VendingMachine):
    js = JuiceSupplier({"cola": 120})
    reqs = [SupplyJuiceRequest(juice=js("cola"), qty=5), InsertMoneyRequest(money=Money.Y100)]
    # おかねいれる
    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    vending_machine.is_available(js("cola")) == VendingMachineStatus.INSUFFICIENT_AMOUNT


def test_is_available2(vending_machine: VendingMachine):
    js = JuiceSupplier({"cola": 120})
    reqs = [SupplyJuiceRequest(juice=js("cola"), qty=5), InsertMoneyRequest(money=Money.Y500)]

    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    stock = vending_machine.stock["cola"]
    amount = vending_machine.money_amount

    vending_machine.buy("cola")

    assert vending_machine.stock["cola"] == stock - 1
    assert vending_machine.money_amount == amount - 120
