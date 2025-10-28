from abc import ABC, abstractmethod

class HotDogABC(ABC):
    @abstractmethod
    def __init__(self, bread, sausage, souse, additions) -> None:
        self._bread = bread
        self._sausage = sausage
        self._souse = souse
        self._additions = additions
        self._price = 15

    @abstractmethod
    def display(self) -> None:
        pass

    @abstractmethod
    def get_price(self):
        pass


class BuilderABC(ABC):
    @abstractmethod
    def check_items(self):
        pass

    @abstractmethod
    def produce(self):
        pass


class OrderABC(ABC):
    @abstractmethod
    def add_item(self, item) -> None:
        pass

    @abstractmethod
    def display_order(self):
        pass


class ItemsABC(ABC):
    @abstractmethod
    def check_item(self, bread, sausage, souse, additions):
        pass

    @abstractmethod
    def update_items(self, bread, sausage, souse, additions):
        pass

    @abstractmethod
    def alert(self):
        pass


class SaleABC(ABC):
    @abstractmethod
    def count_sale(self, amount, price):
        pass


class HotDog(HotDogABC):
    def __init__(self, bread, sausage, souse, additions) -> None:
        self._bread = bread
        self._sausage = sausage
        self._souse = souse
        self._additions = additions
        self.__price = 15

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    def display(self) -> None:
        self.count_price()
        print(f"Hot dog: {self._bread}, {self._sausage}, {self._souse}, {self._additions}\nPrice: {self.__price}")

    def count_price(self):
        if len(self._additions) > 1:
            self.__price += 2

    def get_price(self):
        return self.__price

    def get_full(self):
        return f"Hot dog: {self._bread}, {self._sausage}, {self._souse}, {self._additions}\nPrice: {self.__price}"


class Items(ItemsABC):
    def __init__(self) -> None:
        self._ingredients = {
            "bread": {"White": 10, "Black": 9},
            "sausage": {"Regular": 10, "Bavarian": 8},
            "souse": {"Ketchup": 10, "Garlic": 8},
            "additions": {"Pickles": 8, "Onions": 6, "Chilli": 5}
        }
        self._missing_items = []

    def check_item(self, bread, sausage, souse, additions):
        self._missing_items = []

        if self._ingredients["bread"][bread] <= 0:
            self._missing_items.append(bread)
        if self._ingredients["sausage"][sausage] <= 0:
            self._missing_items.append(sausage)
        if self._ingredients["souse"][souse] <= 0:
            self._missing_items.append(souse)
        for i in additions:
            if self._ingredients["additions"][i] <= 0:
                self._missing_items.append(i)
        return self._missing_items

    def update_items(self, bread, sausage, souse, additions):
        self._ingredients["bread"][bread] -= 1
        self._ingredients["sausage"][sausage] -= 1
        self._ingredients["souse"][souse] -= 1
        for i in additions:
            self._ingredients["additions"][i] -= 1

    def alert(self):
        for i, item in self._ingredients.items():
            for j, amount in item.items():
                if amount <= 2:
                    print(f"We are running out of {j}, only {amount} left.")
                    if amount == 0:
                        return True
        return False

    @property
    def ingredients(self):
        return self._ingredients


class Proxy(HotDog):
    def __new__(cls, bread, sausage, souse, additions):
        items = Items()
        result = items.check_item(bread, sausage, souse, additions)
        if len(result) > 0:
            return None
        return super().__new__(cls)


class Builder1(BuilderABC):
    def __init__(self, items: Items) -> None:
        self._items = items
        self._bread = "White"
        self._sausage = "Bavarian"
        self._souse = "Ketchup"
        self._additions = ["Onions"]
        self._missing_items = None

    def check_items(self):
        self._missing_items = self._items.check_item(self._bread, self._sausage, self._souse, self._additions)
        return len(self._missing_items) == 0

    def produce(self):
        if self.check_items():
            self._items.update_items(self._bread, self._sausage, self._souse, self._additions)
            return Proxy(self._bread, self._sausage, self._souse, self._additions)
        else:
            print(f"We don't have enough items for this HotDog\nMissing items: {self._missing_items}")
            return None


class Builder2(BuilderABC):
    def __init__(self, items: Items) -> None:
        self._missing_items = None
        self._items = items
        self.__bread = "Black"
        self.__sausage = "Regular"
        self.__souse = "Garlic"
        self.__additions = ["Pickles"]

    @property
    def bread(self): return self.__bread
    @bread.setter
    def bread(self, bread): self.__bread = bread

    @property
    def sausage(self): return self.__sausage
    @sausage.setter
    def sausage(self, sausage): self.__sausage = sausage

    @property
    def souse(self): return self.__souse
    @souse.setter
    def souse(self, souse): self.__souse = souse

    @property
    def additions(self): return self.__additions
    @additions.setter
    def additions(self, additions): self.__additions = additions

    def check_items(self):
        self._missing_items = self._items.check_item(self.__bread, self.__sausage, self.__souse, self.__additions)
        return len(self._missing_items) == 0

    def produce(self):
        if self.check_items():
            self._items.update_items(self.__bread, self.__sausage, self.__souse, self.__additions)
            return Proxy(self.__bread, self.__sausage, self.__souse, self.__additions)
        else:
            print(f"We don't have enough items for this HotDog\nMissing items: {self._missing_items}")
            return None


class CustomBuilder(BuilderABC):
    def __init__(self, bread, sausage, souse, additions, items: Items) -> None:
        self._missing_items = None
        self._items = items
        self._bread = bread
        self._sausage = sausage
        self._souse = souse
        self._additions = additions

    def check_each(self):
        check = True
        if self._bread not in self._items.ingredients["bread"]:
            print("We don't have such bread"); check = False
        if self._sausage not in self._items.ingredients["sausage"]:
            print("We don't have such sausage"); check = False
        if self._souse not in self._items.ingredients["souse"]:
            print("We don't have such souse"); check = False
        for i in self._additions:
            if i not in self._items.ingredients["additions"]:
                print(f"We don't have such addition {i}"); check = False
        return check

    def check_items(self):
        self._missing_items = self._items.check_item(self._bread, self._sausage, self._souse, self._additions)
        return len(self._missing_items) == 0

    def produce(self):
        if self.check_each() and self.check_items():
            self._items.update_items(self._bread, self._sausage, self._souse, self._additions)
            return Proxy(self._bread, self._sausage, self._souse, self._additions)
        elif not self.check_items():
            print(f"We don't have enough items for this HotDog\nMissing items: {self._missing_items}")
        return None


class Order(OrderABC):
    def __init__(self) -> None:
        self._current_order = []

    def add_item(self, hotdog) -> None:
        if hotdog:
            self._current_order.append(hotdog)
            self.display_order()

    def display_order(self):
        for idx, i in enumerate(self._current_order, start=1):
            print(f"------\n{idx}")
            i.display()

    def save_order(self):
        with open("file2.txt", "w") as file:
            for i in self._current_order:
                file.write(f"Hot dog: {i.get_full()}\n")

    def reset(self): self._current_order = []
    def get_order(self): return self._current_order
    def get_price(self): return sum(i.get_price() for i in self._current_order)


class NoSale(SaleABC):
    def count_sale(self, amount, price): return 0


class WithSale(SaleABC):
    def count_sale(self, amount, price):
        return price * 0.05 if 3 <= amount < 5 else price * 0.1


class Sale:
    def __init__(self, no_sale: NoSale, with_sale: WithSale) -> None:
        self._no_sale = no_sale
        self._with_sale = with_sale
        self._strategy = self._no_sale

    def choose_strategy(self, order):
        self._strategy = self._with_sale if len(order.get_order()) >= 3 else self._no_sale

    def apply_sale(self, order):
        self.choose_strategy(order)
        amount = len(order.get_order())
        price = sum(i.get_price() for i in order.get_order())
        return self._strategy.count_sale(amount, price)


class Context:
    def __init__(self):
        self._items = Items()
        self._order = Order()
        self._sale = Sale(NoSale(), WithSale())
        self._state = None

    def change_state(self, state):
        self._state = state
        self._state.context = self

    def process_state(self):
        return self._state.process(self._items, self._order)


class State(ABC):
    def __init__(self):
        self.__context = None

    @property
    def context(self): return self.__context
    @context.setter
    def context(self, context): self.__context = context

    @abstractmethod
    def process(self, items: Items, order: Order):
        pass


class MenuMode(State):
    def get_option(self):
        option = int(input("1 - First hotdog\n2 - Second hotdog\n3 - Custom hotdog\n4 - Finish order\n5 - Start over\nEnter: "))
        return option if 0 < option < 6 else self.get_option()

    def process(self, items, order):
        while True:
            if items.alert():
                self.context.change_state(NoItems())
                return
            user_option = self.get_option()
            if user_option == 1:
                order.add_item(Builder1(items).produce())
            elif user_option == 2:
                order.add_item(Builder2(items).produce())
            elif user_option == 3:
                self.custom_hotdog(items, order)
            elif user_option == 4:
                self.context.change_state(Finish())
                return
            elif user_option == 5:
                order.reset()

    def custom_hotdog(self, items, order):
        additions = []
        bread = input("What is the bread: ")
        sausage = input("What is the sausage: ")
        souse = input("What is the souse: ")
        amount = int(input("How many additions you want(1-3): "))
        for i in range(amount):
            additions.append(input("Enter: "))
        hotdog = CustomBuilder(bread, sausage, souse, additions, items).produce()
        if hotdog:
            order.add_item(hotdog)


class NoItems(State):
    def get_option(self):
        option = int(input("1 - Order custom hotdog\n2 - Finish your order\nEnter: "))
        return option if 0 < option < 3 else self.get_option()

    def process(self, items, order):
        while True:
            option = self.get_option()
            if option == 1:
                self.custom_hotdog(items, order)
            elif option == 2:
                self.context.change_state(Finish())
                self.context.process_state()
                return

    def custom_hotdog(self, items, order):
        additions = []
        bread = input("What is the bread: ")
        sausage = input("What is the sausage: ")
        souse = input("What is the souse: ")
        amount = int(input("How many additions you want(1-3): "))
        for i in range(amount):
            additions.append(input("Enter: "))
        hotdog = CustomBuilder(bread, sausage, souse, additions, items).produce()
        if hotdog:
            order.add_item(hotdog)


class Finish(State):
    def process(self, items, order):
        order.save_order()
        order.display_order()
        sale = Sale(NoSale(), WithSale())
        discount = sale.apply_sale(order)
        price = order.get_price() - discount
        print(f"\n\nYour final price is {price} with a sale of {discount}.")
        return False


class Director:
    def __init__(self):
        self._context = Context()

    def main(self):
        self._context.change_state(MenuMode())
        while True:
            result = self._context.process_state()
            if result is False:
                return
