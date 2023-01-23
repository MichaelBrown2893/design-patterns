"""liskov_substitution_test.py

unittests for liskov_substitution.py"""
import pytest

from liskov_substitution import Order


# region Order tests

@pytest.fixture
def order():
    return Order()

def test_add_item_adds_item(order):
    assert not order.items
    assert not order.quantities
    assert not order.prices
    name = "Name"
    price = 1
    qty = 1
    order.add_item(name, qty, price)
    assert name in order.items
    assert qty in order.quantities
    assert price in order.prices


def test_total_price_returns_correct_price(order):
    price_1 = 1
    price_2 = 2
    price_3 = 3
    qty_1 = 3
    qty_2 = 2
    qty_3 = 1
    order.add_item("", qty_1, price_1)
    order.add_item("", qty_2, price_2)
    order.add_item("", qty_3, price_3)


# endregion
