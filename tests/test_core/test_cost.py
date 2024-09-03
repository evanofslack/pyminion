from pyminion.core import Cost
import pytest


def test_init():
    c1 = Cost(1)
    assert c1.money == 1
    assert c1.potions == 0

    c2 = Cost(3, 1)
    assert c2.money == 3
    assert c2.potions == 1

    c3 = Cost()
    assert c3.money == 0
    assert c3.potions == 0

    with pytest.raises(AssertionError):
        Cost(-1)

    with pytest.raises(AssertionError):
        Cost(1, 2)


def test_repr():
    c1 = Cost(0)
    assert repr(c1) == "Cost(0, 0)"

    c2 = Cost(2, 1)
    assert repr(c2) == "Cost(2, 1)"


def test_format():
    c1 = Cost(3)
    assert f"{c1:>3}" == " $3"

    c2 = Cost(6, 1)
    assert f"{c2:<8}" == "$6P     "


def test_hash():
    c1 = Cost(3)
    c2 = Cost(3)
    assert hash(c1) == hash(c2)

    c3 = Cost(2, 1)
    c4 = Cost(2, 1)
    assert hash(c3) == hash(c4)


def test_str():
    c1 = Cost(0)
    assert str(c1) == "$0"

    c2 = Cost(5)
    assert str(c2) == "$5"

    c3 = Cost(0, 1)
    assert str(c3) == "P"

    c4 = Cost(2, 1)
    assert str(c4) == "$2P"


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
    assert Cost(1) < Cost(2, 1)
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
    assert Cost(1) <= Cost(2, 1)
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


def test_add():
    c1 = Cost(0) + 3
    assert c1.money == 3 and c1.potions == 0

    c2 = Cost(4, 1) + 2
    assert c2.money == 6 and c2.potions == 1

    c3 = Cost(4, 1) + -2
    assert c3.money == 2 and c3.potions == 1

    c4 = Cost(4, 1) + -5
    assert c4.money == 0 and c4.potions == 1

    c5 = 2 + Cost(4, 1)
    assert c5.money == 6 and c5.potions == 1


def test_sub():
    c1 = Cost(3) - 1
    assert c1.money == 2 and c1.potions == 0

    c2 = Cost(4, 1) - 2
    assert c2.money == 2 and c2.potions == 1

    c3 = Cost(2, 1) - 8
    assert c3.money == 0 and c3.potions == 1

    c4 = Cost(3) - -3
    assert c4.money == 6 and c4.potions == 0


def test_examples():
    # examples from https://wiki.dominionstrategy.com/index.php/Alchemy

    # $3 < $3P

    assert Cost(3) < Cost(3, 1)
    assert Cost(3, 1) > Cost(3)

    # comparisons with no potions in cost

    for m in range(5):
        assert Cost(m) < 5
        assert not Cost(m, 1) < 5
        assert 5 > Cost(m)
        assert not 5 > Cost(m, 1)
        assert Cost(m) <= 5
        assert not Cost(m, 1) <= 5
        assert 5 >= Cost(m)
        assert not 5 >= Cost(m, 1)

    assert not Cost(5) < 5
    assert not Cost(5, 1) < 5
    assert not 5 > Cost(5)
    assert not 5 > Cost(5, 1)
    assert Cost(5) <= 5
    assert not Cost(5, 1) <= 5
    assert 5 >= Cost(5)
    assert not 5 >= Cost(5, 1)

    # comparisons with potions in cost

    for m in range(4):
        assert Cost(m) < Cost(4, 1)
        assert Cost(m, 1) < Cost(4, 1)
        assert Cost(4, 1) > Cost(m)
        assert Cost(4, 1) > Cost(m, 1)
        assert Cost(m) <= Cost(4, 1)
        assert Cost(m, 1) <= Cost(4, 1)
        assert Cost(4, 1) >= Cost(m)
        assert Cost(4, 1) >= Cost(m, 1)

    assert Cost(4) < Cost(4, 1)
    assert not Cost(4, 1) < Cost(4, 1)
    assert Cost(4, 1) > Cost(4)
    assert not Cost(4, 1) > Cost(4, 1)
    assert Cost(4) <= Cost(4, 1)
    assert Cost(4, 1) <= Cost(4, 1)
    assert Cost(4, 1) >= Cost(4)
    assert Cost(4, 1) >= Cost(4, 1)

    assert not Cost(5) < Cost(4, 1)
    assert not Cost(5, 1) < Cost(4, 1)
    assert not Cost(4, 1) > Cost(5)
    assert not Cost(4, 1) > Cost(5, 1)
    assert not Cost(5) <= Cost(4, 1)
    assert not Cost(5, 1) <= Cost(4, 1)
    assert not Cost(4, 1) >= Cost(5)
    assert not Cost(4, 1) >= Cost(5, 1)

    # range comparisons

    assert not 3 <= Cost(2) <= 6
    assert not 3 <= Cost(2, 1) <= 6
    for m in range(3, 7):
        assert 3 <= Cost(m) <= 6
        assert not 3 <= Cost(m, 1) <= 6
    assert not 3 <= Cost(7) <= 6
    assert not 3 <= Cost(7, 1) <= 6
