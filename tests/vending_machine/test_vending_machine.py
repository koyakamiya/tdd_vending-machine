import pytest

from vending_machine.juice_supplier import JuiceSupplier
from vending_machine.money import Money
from vending_machine.request import InsertMoneyRequest, RefundRequest, SupplyJuiceRequest
from vending_machine.response import EmptyResponse, RefundResponse, ReturnMoneyResponse
from vending_machine.vending_machine import VendingMachine


@pytest.fixture
def vending_machine() -> VendingMachine:
    return VendingMachine()


def test_insert_money_into_vending_machine(vending_machine: VendingMachine):
    req = InsertMoneyRequest(money=Money.Y1)
    res: ReturnMoneyResponse = vending_machine(req)

    assert res.money == Money.Y1


def test_count_money_amount(vending_machine: VendingMachine):
    req = InsertMoneyRequest(money=Money.Y100)
    _: EmptyResponse = vending_machine(req)
    assert vending_machine.money_amount == 100


def test_count_total_money_amount(vending_machine: VendingMachine):
    reqs = []
    reqs.append(InsertMoneyRequest(money=Money.Y100))
    reqs.append(InsertMoneyRequest(money=Money.Y10))
    reqs.append(InsertMoneyRequest(money=Money.Y10))

    for req in reqs:
        _: EmptyResponse = vending_machine(req)

    assert vending_machine.money_amount == 120


def test_refund(vending_machine: VendingMachine):
    reqs = [InsertMoneyRequest(money=Money.Y10) for _ in range(6)]
    reqs.append(RefundRequest())

    for i, req in enumerate(reqs):
        if i < len(reqs) - 1:
            _: EmptyResponse = vending_machine(req)
        else:
            res: RefundResponse = vending_machine(req)

    expected_refunds = [Money.Y10 for _ in range(6)]
    assert res.refunds == expected_refunds
    assert vending_machine.money_amount == 0


def test_is_acceptable_money_kind(vending_machine: VendingMachine):
    assert vending_machine.check_acceptable_money_kind(Money.Y10) is True


def test_is_not_acceptable_money_kind(vending_machine: VendingMachine):
    assert vending_machine.check_acceptable_money_kind(Money.Y1) is False


def test_check_stock(vending_machine: VendingMachine):
    js = JuiceSupplier({"cola": 120})
    req = SupplyJuiceRequest(juice=js("cola"), qty=5)

    _: EmptyResponse = vending_machine(req)
    stock: dict[str, int] = vending_machine.stock

    assert len(stock) == 1
    assert "cola" in stock.keys()
    assert stock["cola"] == 5
    assert js.name2price["cola"] == 120
