"""open_closed.py

Module for work done in design principles udemy course for open closed"""
# pylint: disable=too-few-public-methods

from __future__ import annotations

from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from typing import Generator, Collection


class Color(Enum):
    """Color product feature"""

    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    """Size product feature"""

    SMALL = 1
    MEDIUM = 2
    LARGE = 3


@dataclass
class Product:
    """Class representing an item found in a store"""

    name: str
    color: Color
    size: Size

    def __init__(self, name: str, color: Color, size: Size) -> None:
        self.name = name
        self.color = color
        self.size = size


# OCP = open for extension, closed for modification
# after writing and testing a class you should not modify it you should extend it
# New filter requirements require the ProductFilter to be modified which is an unsalable approach
# State Space Explosion - As the number of state variables in the system increases,
# the size of the system state space grows exponentially


class ProductFilter:
    """Class responsible for filtering a list of products"""

    @staticmethod
    def filter_by_color(items: Collection[Product], color: Color) -> Generator[Product, None, None]:
        """Filters a list of items by a given color

        :param items: List of items to filter
        :param color: Color to filter by
        :returns: Generator containing items of the given color
        """
        for item in items:
            if item.color is color:
                yield item

    @staticmethod
    def filter_by_size(items: Collection[Product], size: Size) -> Generator[Product, None, None]:
        """Filters a list of items by a given size

        :param items: List of items to filter
        :param size: Color to filter by
        :returns: Generator containing items of the given size
        """
        for item in items:
            if item.size is size:
                yield item

    @staticmethod
    def filter_by_size_and_color(items, size, color) -> Generator[Product, None, None]:
        """Filters a list of items by a given color and size

        :param items: List of items to filter
        :param size: Color to filter by
        :param color: Color to filter by
        :returns: Generator containing items of the given color and size
        """
        for item in items:
            if item.color is color and item.size is size:
                yield item


# Specification Pattern
# Filter and Specification are closed for modification but open for extension
# As new filter requirements arise new subclasses can be created to satisfy those requirements


class Specification(ABC):
    """Base class for an item specification"""

    @abstractmethod
    def is_satisfied(self, item: Product) -> bool:
        """Checks if the item meets the specification

        :param item: Item to check
        :returns: If the given item meets the specification
        """

    def __and__(self, other: Specification) -> AndSpecification:
        return AndSpecification(self, other)

    def __or__(self, other: Specification) -> OrSpecification:
        return OrSpecification(self, other)

    def __xor__(self, other: Specification) -> XorSpecification:
        return XorSpecification(self, other)


class ColorSpecification(Specification):
    """Specification for filtering by a color"""

    def __init__(self, color: Color) -> None:
        self.color = color

    def is_satisfied(self, item: Product) -> bool:
        """Checks if a product meets the specification

        :param item: Product to check
        :return: If the product meets the specification
        """
        return item.color is self.color


class SizeSpecification(Specification):
    """Specification for filtering by size"""

    def __init__(self, size: Size) -> None:
        self.size = size

    def is_satisfied(self, item) -> bool:
        """Checks if a product meets the specification

        :param item: Product to check
        :return: If the product meets the specification
        """
        return item.size is self.size


# This is a combinator
class AndSpecification(Specification):
    """Specification combining multiple specifications with an AND operator"""

    def __init__(self, *args: Specification) -> None:
        self._specs = args

    def is_satisfied(self, item: Product) -> bool:
        """Checks if a product meets all the specifications

        :param item: Product to check
        :return: If the product meets all given specifications
        """
        return all(map(lambda spec: spec.is_satisfied(item), self._specs))


class OrSpecification(Specification):
    """Specification combining multiple specifications with an OR operator"""

    def __init__(self, *args: Specification) -> None:
        self._specs = args

    def is_satisfied(self, item: Product) -> bool:
        """Checks if a product meets the specification

        :param item: Product to check
        :return: If the product meets any of the specifications
        """
        return any(map(lambda spec: spec.is_satisfied(item), self._specs))


class XorSpecification(Specification):
    """Specification combining multiple specifications with an XOR operator"""

    def __init__(self, *args: Specification) -> None:
        self._specs = args

    def is_satisfied(self, item: Product) -> bool:
        """Checks if a product meets only one of the specifications

        :param item: Product to check
        :return: If the product meets only one of the specifications
        """
        satisfied = map(lambda spec: spec.is_satisfied(item), self._specs)
        return any(satisfied) and not any(satisfied)


class Filter(ABC):
    """Class responsible for filtering a list of products given a specification"""

    @abstractmethod
    def filter(
        self, items: Collection[Product], spec: Specification
    ) -> Generator[Product, None, None]:
        """Filters a collection of Products given a specification

        :param items: Collection of products to filter
        :param spec: Specification to filter by
        :returns: A generator containing Products that met the specification
        """


class BetterFilter(Filter):
    """Class that handles filtering based on a given specification"""

    def filter(
        self, items: Collection[Product], spec: Specification
    ) -> Generator[Product, None, None]:
        """Filters a collection of Products given a specification

        :param items: Collection of Products to filter
        :param spec: Specification to filter by
        :returns: A generator containing Products that met the specification
        """
        for item in items:
            if spec.is_satisfied(item):
                yield item


def print_filtered_products(title: str, filtered_items: Generator) -> None:
    """Prints filtered items to the console

    :param title: title of the results
    :param filtered_items: Generator of filtered items
    """
    print(f"{title} (new):")
    for item in filtered_items:
        print(f"- {item.name} is {title}")
    print("\n")


if __name__ == "__main__":
    apple = Product("Apple", Color.GREEN, Size.SMALL)
    tree = Product("Tree", Color.GREEN, Size.LARGE)
    house = Product("House", Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    pf = ProductFilter()
    print("Green products (old):")
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f"- {p.name} is green")
    print("\n")

    bf = BetterFilter()

    green = ColorSpecification(Color.GREEN)
    filtered_green = bf.filter(products, green)
    print_filtered_products("Green", filtered_green)

    large = SizeSpecification(Size.LARGE)
    filtered_large = bf.filter(products, large)
    print_filtered_products("Large", filtered_large)

    large_and_green = AndSpecification(large, green)
    filtered_large_and_green = bf.filter(products, large_and_green)
    print_filtered_products("Large and Green", filtered_large_and_green)

    blue = ColorSpecification(Color.BLUE)
    large_and_blue = large & blue
    filtered_large_and_blue = bf.filter(products, large_and_blue)
    print_filtered_products("Large and Blue", filtered_large_and_blue)

    large_or_green = OrSpecification(large, green)
    filtered_large_or_green = bf.filter(products, large_or_green)
    print_filtered_products("Large or Green", filtered_large_or_green)

    large_or_blue = large | blue
    filtered_large_or_blue = bf.filter(products, large_or_blue)
    print_filtered_products("Large or Blue", filtered_large_or_blue)

    large_xor_green = XorSpecification(large, green)
    filtered_large_xor_green = bf.filter(products, large_xor_green)
    print_filtered_products("Large xor Green", filtered_large_xor_green)

    large_xor_blue = large ^ blue
    filtered_large_xor_blue = bf.filter(products, large_xor_blue)
    print_filtered_products("Large xor Blue", filtered_large_xor_blue)
