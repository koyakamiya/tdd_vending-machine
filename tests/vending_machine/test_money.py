from vending_machine.money import Money


def test_cannot_create_2_yen():
    assert "Y2" not in dir(Money)


def test_cannot_create_0_yen():
    assert "Y0" not in dir(Money)


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
