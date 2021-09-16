from collections import defaultdict

import pytest

from vending_machine.juice import Juice
from vending_machine.juice_supplier import JuiceSupplier
from vending_machine.money import Money
from vending_machine.request import BuyRequest, InsertMoneyRequest, RefundRequest, SupplyJuiceRequest
from vending_machine.response import BuyResponse, RefundResponse, Response, ReturnMoneyResponse
from vending_machine.vending_machine import BuyError, VendingMachine, VendingMachineStatus


@pytest.fixture
def vending_machine_with_cola() -> VendingMachine:
    return VendingMachine(JuiceSupplier({"cola": 120}))


@pytest.fixture
def vending_machine_with_cola_redbull_water() -> VendingMachine:
    return VendingMachine(JuiceSupplier({"cola": 120, "redbull": 200, "water": 100}))


def test_insert_money_into_vending_machine(vending_machine_with_cola: VendingMachine):
    req = InsertMoneyRequest(money=Money.Y1)
    res: Response = vending_machine_with_cola(req)

    assert isinstance(res, ReturnMoneyResponse)
    assert res.money == Money.Y1


def test_get_money_amount(vending_machine_with_cola: VendingMachine):
    reqs = []
    reqs.append(InsertMoneyRequest(money=Money.Y100))
    reqs.append(InsertMoneyRequest(money=Money.Y10))
    reqs.append(InsertMoneyRequest(money=Money.Y10))

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    assert vending_machine_with_cola.money_amount == 120


def test_refund(vending_machine_with_cola: VendingMachine):
    reqs = [InsertMoneyRequest(money=Money.Y10) for _ in range(6)]
    expected_refunds = [Money.Y10 for _ in range(6)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    res: Response = vending_machine_with_cola(RefundRequest())

    assert isinstance(res, RefundResponse)
    assert res.refunds == expected_refunds
    assert vending_machine_with_cola.money_amount == 0


@pytest.mark.parametrize("money, is_available", [(Money.Y10, True), (Money.Y1, False)])
def test_is_acceptable_money_kind(money, is_available, vending_machine_with_cola: VendingMachine):
    assert vending_machine_with_cola.check_acceptable_money_kind(money) is is_available


def test_check_stock(vending_machine_with_cola: VendingMachine):
    req = SupplyJuiceRequest(juice=Juice("cola", 120), qty=5)

    _: Response = vending_machine_with_cola(req)
    stock: defaultdict[str, int] = vending_machine_with_cola.stock

    assert len(stock) == 1
    assert "cola" in stock.keys()
    assert stock["cola"] == 5
    assert vending_machine_with_cola.juice_supplier.name2price["cola"] == 120


def test_is_available(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [SupplyJuiceRequest(juice=juice, qty=5), InsertMoneyRequest(money=Money.Y500)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    vending_machine_with_cola.is_available(juice) == VendingMachineStatus.IS_AVAILABLE_JUICE


def test_is_not_available_by_empty_stock(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [InsertMoneyRequest(money=Money.Y500)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    vending_machine_with_cola.is_available(juice) == VendingMachineStatus.EMPTY_STOCK


def test_is_not_available_by_insufficient_amount(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [SupplyJuiceRequest(juice=juice, qty=5), InsertMoneyRequest(money=Money.Y100)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    vending_machine_with_cola.is_available(juice) == VendingMachineStatus.INSUFFICIENT_AMOUNT


def test_buy_cola(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [SupplyJuiceRequest(juice=juice, qty=5), InsertMoneyRequest(money=Money.Y500)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    stock = vending_machine_with_cola.stock["cola"]
    amount = vending_machine_with_cola.money_amount
    expected_money_list = [
        Money(100),
        Money(100),
        Money(100),
        Money(50),
        Money(10),
        Money(10),
        Money(10),
    ]

    vending_machine_with_cola.buy("cola")

    assert vending_machine_with_cola.stock["cola"] == stock - 1
    assert vending_machine_with_cola.money_amount == amount - 120
    for money, expected_money in zip(vending_machine_with_cola.money_list, expected_money_list):
        assert money.value == expected_money.value


def test_cannot_buy_cola_for_empty_stock(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [SupplyJuiceRequest(juice=juice, qty=0), InsertMoneyRequest(money=Money.Y500)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    with pytest.raises(BuyError):
        vending_machine_with_cola.buy("cola")


def test_cannot_buy_cola_for_no_money(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [SupplyJuiceRequest(juice=juice, qty=5), InsertMoneyRequest(money=Money.Y100)]

    for req in reqs:
        _: Response = vending_machine_with_cola(req)

    with pytest.raises(BuyError):
        vending_machine_with_cola.buy("cola")


def test_send_buy_request(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    reqs = [
        SupplyJuiceRequest(juice=juice, qty=5),
        InsertMoneyRequest(money=Money.Y100),
        InsertMoneyRequest(money=Money.Y100),
        BuyRequest(juice_name=juice.name),
    ]
    expected_juice = juice
    expected_refunds = [
        Money(50),
        Money(10),
        Money(10),
        Money(10),
    ]

    for req in reqs[:3]:
        _: Response = vending_machine_with_cola(req)
    buy_response: Response = vending_machine_with_cola(reqs[3])

    assert isinstance(buy_response, BuyResponse)
    assert buy_response.juice == expected_juice
    assert buy_response.refunds == expected_refunds


def test_send_buy_request_when_no_refund(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    another_juice = Juice("kirin_beer", 200)
    reqs = [
        SupplyJuiceRequest(juice=juice, qty=5),
        SupplyJuiceRequest(juice=another_juice, qty=5),
        InsertMoneyRequest(money=Money.Y100),
        InsertMoneyRequest(money=Money.Y100),
        InsertMoneyRequest(money=Money.Y10),
        InsertMoneyRequest(money=Money.Y10),
        InsertMoneyRequest(money=Money.Y10),
        InsertMoneyRequest(money=Money.Y10),
        BuyRequest(juice_name=juice.name),
    ]
    expected_juice = juice
    expected_refunds = None

    for req in reqs[:-1]:
        _: Response = vending_machine_with_cola(req)
    buy_response: Response = vending_machine_with_cola(reqs[-1])

    assert isinstance(buy_response, BuyResponse)
    assert buy_response.juice == expected_juice
    assert buy_response.refunds == expected_refunds


def test_send_buy_request_when_lack_money(vending_machine_with_cola: VendingMachine):
    juice = Juice("cola", 120)
    another_juice = Juice("kirin_beer", 200)
    reqs = [
        SupplyJuiceRequest(juice=juice, qty=5),
        SupplyJuiceRequest(juice=another_juice, qty=5),
        InsertMoneyRequest(money=Money.Y100),
        BuyRequest(juice_name=juice.name),
    ]
    expected_juice = None
    expected_refunds = None

    for req in reqs[:-1]:
        _: Response = vending_machine_with_cola(req)
    buy_response: Response = vending_machine_with_cola(reqs[-1])

    assert isinstance(buy_response, BuyResponse)
    assert buy_response.juice == expected_juice
    assert buy_response.refunds == expected_refunds


def test_check_menu_vending_machine_redbull_and_water(vending_machine_with_cola_redbull_water: VendingMachine):
    cola = Juice("cola", 120)
    redbull = Juice("redbull", 200)
    water = Juice("water", 100)

    expected_menu = defaultdict(int, {"cola": 5, "redbull": 5, "water": 5})

    reqs = [
        SupplyJuiceRequest(juice=cola, qty=5),
        SupplyJuiceRequest(juice=redbull, qty=5),
        SupplyJuiceRequest(juice=water, qty=5),
    ]

    for req in reqs:
        _: Response = vending_machine_with_cola_redbull_water(req)

    assert vending_machine_with_cola_redbull_water.stock == expected_menu


def test_check_available_drinks_by_money(vending_machine_with_cola_redbull_water: VendingMachine):
    cola = Juice("cola", 120)
    redbull = Juice("redbull", 200)
    water = Juice("water", 100)

    expected_available_drinks = {"water"}

    reqs = [
        SupplyJuiceRequest(juice=cola, qty=5),
        SupplyJuiceRequest(juice=redbull, qty=5),
        SupplyJuiceRequest(juice=water, qty=5),
        InsertMoneyRequest(money=Money.Y100),
    ]

    for req in reqs:
        _: Response = vending_machine_with_cola_redbull_water(req)

    assert vending_machine_with_cola_redbull_water.available_drinks == expected_available_drinks


def test_check_available_drinks_by_empty_stock(vending_machine_with_cola_redbull_water: VendingMachine):
    cola = Juice("cola", 120)
    redbull = Juice("redbull", 200)
    water = Juice("water", 100)

    expected_available_drinks = {"cola", "redbull"}

    reqs = [
        SupplyJuiceRequest(juice=cola, qty=5),
        SupplyJuiceRequest(juice=redbull, qty=5),
        SupplyJuiceRequest(juice=water, qty=5),
        InsertMoneyRequest(money=Money.Y1000),
        BuyRequest(juice_name=water.name),
        BuyRequest(juice_name=water.name),
        BuyRequest(juice_name=water.name),
        BuyRequest(juice_name=water.name),
        BuyRequest(juice_name=water.name),
    ]

    for req in reqs:
        _: Response = vending_machine_with_cola_redbull_water(req)

    assert vending_machine_with_cola_redbull_water.available_drinks == expected_available_drinks
