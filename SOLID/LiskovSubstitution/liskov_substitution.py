"""liskov_substitution.py

includes the content from the Liskov substitution lecture

exercise from arjancodes: https://www.youtube.com/watch?v=pTB30aXS77U
If you have objects in a program you should be able to replace them with instances
of their subtypes or subclasses without altering the correctness of the program
"""
from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name: str, quantity: int, price: int) -> None:
        """Adds an item to the order

        :param name: Name of the item
        :param quantity: Quantity of the item
        :param price: Price of the item
        """
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] + self.prices[i]
        return total


class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self._security_code = security_code

    def pay(self, order):
        print("Processing debit payment type")
        print(f"Verifying security code: {self._security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def __init__(self, security_code):
        self._security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self._security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):
    def __init__(self, email):
        self._email = email

    def pay(self, order):
        print("Processing paypal payment type")
        print(f"Verifying email address: {self._email}")
        order.status = "paid"


if __name__ == "__main__":
    new_order = Order()
    new_order.add_item("Keyboard", 1, 150)
    new_order.add_item("Mouse", 1, 100)
    new_order.add_item("Monitor", 1, 450)

    print(new_order.total_price())
    processor = PaypalPaymentProcessor("test@email.com")
    processor.pay(new_order)