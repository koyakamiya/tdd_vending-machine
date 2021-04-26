from typing import Final

from vending_machine.money import Money


def test_cannot_create_2_yen():
    assert "Y2" not in dir(Money)


def test_cannot_create_0_yen():
    assert "Y0" not in dir(Money)


def test_create_japanese_valid_money():
    JAPANESE_MONEY_KIND: Final[list[str]] = [
        "Y1",
        "Y5",
        "Y10",
        "Y50",
        "Y100",
        "Y500",
        "Y1000",
        "Y2000",
        "Y5000",
        "Y10000",
    ]

    def _test_money_kind():
        """Test format of Money members."""
        assert set([f"Y{_}" for _ in Money.members()]) == set(JAPANESE_MONEY_KIND)

    def _test_money_value():
        """Test value of Money members."""
        for money, money_kind in zip(Money.members(), JAPANESE_MONEY_KIND):
            assert int(money_kind.lstrip("Y")) == getattr(Money, f"Y{money}")

    _test_money_kind()
    _test_money_value()


def test_create_1_yen():
    assert Money.Y1 == 1


def test_create_5_yen():
    assert Money.Y5 == 5


def test_create_10_yen():
    assert Money.Y10 == 10


def test_create_50_yen():
    assert Money.Y50 == 50


def test_create_100_yen():
    assert Money.Y100 == 100


def test_create_500_yen():
    assert Money.Y500 == 500


def test_create_1000_yen():
    assert Money.Y1000 == 1000


def test_create_2000_yen():
    assert Money.Y2000 == 2000


def test_create_5000_yen():
    assert Money.Y5000 == 5000


def test_create_10000_yen():
    assert Money.Y10000 == 10000
