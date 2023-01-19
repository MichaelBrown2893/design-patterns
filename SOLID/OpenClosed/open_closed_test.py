"""open_closed_test.py

Unittests for the open_closed.py module"""
import sys
from abc import abstractmethod
from io import StringIO
from unittest.mock import MagicMock, Mock

import pytest

from open_closed import (
    ProductFilter,
    Product,
    Color,
    Size,
    ColorSpecification,
    SizeSpecification,
    BetterFilter,
    print_filtered_products,
    Specification,
)

apple = Product("Apple", Color.GREEN, Size.SMALL)
tree = Product("Tree", Color.GREEN, Size.LARGE)
house = Product("House", Color.BLUE, Size.LARGE)


@pytest.fixture()
def products():
    products = [apple, tree, house]
    return products


# region ProductFilter tests
@pytest.fixture
def prod_filter():
    return ProductFilter()


def test_filter_by_color_filters_by_color(prod_filter, products):
    filtered = list(prod_filter.filter_by_color(products, Color.GREEN))
    assert apple in filtered
    assert tree in filtered
    assert house not in filtered


def test_filter_by_size_filters_by_size(prod_filter, products):
    filtered = list(prod_filter.filter_by_size(products, Size.LARGE))
    assert apple not in filtered
    assert tree in filtered
    assert house in filtered


def test_filter_by_size_and_color(prod_filter, products):
    filtered = list(prod_filter.filter_by_size_and_color(products, Size.LARGE, Color.GREEN))
    assert apple not in filtered
    assert tree in filtered
    assert house not in filtered


# endregion

# region Specification Tests
class MockSpecification(Specification):
    def is_satisfied(self, item: Product) -> bool:
        pass


@pytest.fixture
def mock_spec_true():
    true_mock_spec = MockSpecification()
    true_mock_spec.is_satisfied = MagicMock(return_value=True)
    return true_mock_spec


@pytest.fixture
def mock_spec_false():
    false_mock_spec = MockSpecification()
    false_mock_spec.is_satisfied = MagicMock(return_value=False)
    return false_mock_spec


def test_color_specification_is_satisfied_correct_response():
    spec = ColorSpecification(Color.GREEN)
    assert spec.is_satisfied(apple)
    assert spec.is_satisfied(tree)
    assert not spec.is_satisfied(house)


def test_size_specification_is_satisfied_correct_response():
    spec = SizeSpecification(Size.LARGE)
    assert spec.is_satisfied(tree)
    assert spec.is_satisfied(house)
    assert not spec.is_satisfied(apple)


def test_and_specification_is_satisfied_correct_response(mock_spec_true, mock_spec_false):
    true_true_spec = mock_spec_true & mock_spec_true
    true_false_spec = mock_spec_true & mock_spec_false
    false_false_spec = mock_spec_false & mock_spec_false
    assert true_true_spec.is_satisfied(tree)
    assert not true_false_spec.is_satisfied(tree)
    assert not false_false_spec.is_satisfied(tree)


def test_or_specification_is_satisfied_correct_response(mock_spec_true, mock_spec_false):
    true_false_spec = mock_spec_true | mock_spec_false
    true_true_spec = mock_spec_true | mock_spec_true
    false_false_spec = mock_spec_false | mock_spec_false
    assert true_false_spec.is_satisfied(apple)
    assert true_true_spec.is_satisfied(tree)
    assert not false_false_spec.is_satisfied(house)


def test_xor_specification_is_satisfied_correct_response(mock_spec_true, mock_spec_false):
    true_false_spec = mock_spec_true ^ mock_spec_false
    true_true_spec = mock_spec_true ^ mock_spec_true
    false_false_spec = mock_spec_false ^ mock_spec_false
    assert true_false_spec.is_satisfied(apple)
    assert not true_true_spec.is_satisfied(house)
    assert not false_false_spec.is_satisfied(tree)


# endregion


@pytest.fixture
def return_all_filtered_products(products, mock_spec_true):
    prod_filter = BetterFilter()
    return list(prod_filter.filter(products, mock_spec_true))


def test_filter_returns_correct_items_for_spec(return_all_filtered_products):
    assert apple in return_all_filtered_products
    assert tree in return_all_filtered_products
    assert house in return_all_filtered_products


def test_print_filtered_products_prints_filtered_products(return_all_filtered_products):
    expected_output = (
        "Included (new):\n- Apple is Included\n- Tree is Included\n- House is Included\n\n\n"
    )
    captured_output = StringIO()
    sys.stdout = captured_output
    print_filtered_products("Included", return_all_filtered_products)
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == expected_output
