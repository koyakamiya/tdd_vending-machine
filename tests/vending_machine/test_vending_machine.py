import pytest

from vending_machine.money import Money
from vending_machine.vending_machine import VendingMachine


def test_insert_money_into_vending_machine():
    vending_machine = VendingMachine()
    money = Money.Y1
    vending_machine.insert_money(money)


def test_cannot_insert_int_into_vending_machine():
    vending_machine = VendingMachine()
    not_money = 0
    with pytest.raises(TypeError):
        vending_machine.insert_money(not_money)


def test_count_money_amount():
    vending_machine = VendingMachine()
    vending_machine.insert_money(Money.Y100)
    assert vending_machine.money_amount == 100
