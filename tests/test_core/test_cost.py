from pyminion.core import Cost


def test_init():
    c1 = Cost(1)
    assert c1.money == 1
    assert c1.potions == 0

    c2 = Cost(3, 1)
    assert c2.money == 3
    assert c2.potions == 1


def test_str():
    c1 = Cost(0)
    assert str(c1) == "$0"

    c2 = Cost(5)
    assert str(c2) == "$5"

    c3 = Cost(0, 1)
    assert str(c3) == "p1"

    c4 = Cost(2, 1)
    assert str(c4) == "$2 p1"


def test_eq():
    c1 = Cost(0)
    c2 = Cost(1)
    c3 = Cost(1)
    c4 = Cost(1, 1)
    c5 = Cost(1, 1)
    c6 = Cost(2, 1)

    assert c1 == 0
    assert not c1 == 1

    assert c2 == c3
    assert not c2 == c1

    assert not c4 == 1
    assert c4 == c5
    assert not c5 == c6


def test_ne():
    c1 = Cost(0)
    c2 = Cost(1)
    c3 = Cost(1)
    c4 = Cost(1, 1)
    c5 = Cost(1, 1)
    c6 = Cost(2, 1)

    assert not c1 != 0
    assert c1 != 1

    assert not c2 != c3
    assert c2 != c1

    assert c4 != 1
    assert not c4 != c5
    assert c5 != c6
