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
    assert Cost(0) == 0
    assert not Cost(0) == 1

    assert Cost(1) == Cost(1)
    assert not Cost(1) == Cost(0)

    assert not Cost(1, 1) == 1
    assert Cost(1, 1) == Cost(1, 1)
    assert not Cost(1, 1) == Cost(2, 1)


def test_ne():
    assert not  Cost(0) != 0
    assert  Cost(0) != 1

    assert not  Cost(1) != Cost(1)
    assert  Cost(1) !=  Cost(0)

    assert Cost(1, 1) != 1
    assert not Cost(1, 1) != Cost(1, 1)
    assert Cost(1, 1) != Cost(2, 1)


def test_lt():
    assert Cost(0) < 1
    assert not Cost(2) < 2
    assert not Cost(3) < 2

    assert Cost(0) < Cost(1)
    assert not Cost(2) < Cost(2)
    assert not Cost(3) < Cost(2)

    assert Cost(2, 1) < Cost(3, 1)
    assert not Cost(4, 1) < Cost(4, 1)
    assert not Cost(4, 1) < Cost(3, 1)

    assert Cost(2) < Cost(2, 1)
    assert not Cost(1) < Cost(2, 1)
    assert not Cost(3) < Cost(2, 1)


def test_le():
    assert Cost(0) <= 1
    assert Cost(2) <= 2
    assert not Cost(3) <= 2

    assert Cost(0) <= Cost(1)
    assert Cost(2) <= Cost(2)
    assert not Cost(3) <= Cost(2)

    assert Cost(2, 1) <= Cost(3, 1)
    assert Cost(4, 1) <= Cost(4, 1)
    assert not Cost(4, 1) <= Cost(3, 1)

    assert Cost(2) <= Cost(2, 1)
    assert not Cost(1) <= Cost(2, 1)
    assert not Cost(3) <= Cost(2, 1)


def test_gt():
    assert not Cost(0) > 1
    assert not Cost(2) > 2
    assert Cost(3) > 2

    assert not Cost(0) > Cost(1)
    assert not Cost(2) > Cost(2)
    assert Cost(3) > Cost(2)

    assert not Cost(2, 1) > Cost(3, 1)
    assert not Cost(4, 1) > Cost(4, 1)
    assert Cost(4, 1) > Cost(3, 1)

    assert not Cost(2) > Cost(2, 1)
    assert not Cost(1) > Cost(2, 1)
    assert not Cost(3) > Cost(2, 1)


def test_ge():
    assert not Cost(0) >= 1
    assert Cost(2) >= 2
    assert Cost(3) >= 2

    assert not Cost(0) >= Cost(1)
    assert Cost(2) >= Cost(2)
    assert Cost(3) >= Cost(2)

    assert not Cost(2, 1) >= Cost(3, 1)
    assert Cost(4, 1) >= Cost(4, 1)
    assert Cost(4, 1) >= Cost(3, 1)

    assert not Cost(2) >= Cost(2, 1)
    assert not Cost(1) >= Cost(2, 1)
    assert not Cost(3) >= Cost(2, 1)
