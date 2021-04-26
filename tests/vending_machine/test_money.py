from typing import Final

from vending_machine.money import Money


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
