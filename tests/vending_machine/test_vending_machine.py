import pytest

from vending_machine.money import Money
from vending_machine.vending_machine import VendingMachine


@pytest.fixture
def vending_machine():
    return VendingMachine()


def test_insert_money_into_vending_machine(vending_machine):
    money = Money.Y1
    vending_machine.insert_money(money)


def test_cannot_insert_int_into_vending_machine(vending_machine):
    not_money = 0
    with pytest.raises(TypeError):
        vending_machine.insert_money(not_money)


def test_count_money_amount(vending_machine):
    vending_machine.insert_money(Money.Y100)
    assert vending_machine.money_amount == 100


def test_count_total_money_amount(vending_machine):
    vending_machine.insert_money(Money.Y100)
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)
    assert vending_machine.money_amount == 120


def test_refund(vending_machine):
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)
    vending_machine.insert_money(Money.Y10)

    expected_refunds = [Money.Y50, Money.Y10]
    assert vending_machine.refund() == expected_refunds
    assert vending_machine.money_amount == 0


def test_is_acceptable_money_kind(vending_machine):
    assert vending_machine.check_acceptable_money_kind(Money.Y10) is True


def test_is_not_acceptable_money_kind(vending_machine):
    assert vending_machine.check_acceptable_money_kind(Money.Y1) is False
