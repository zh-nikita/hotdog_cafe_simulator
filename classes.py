from abc import ABC, abstractmethod


#Abstract classes
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
    def add_item(self, item: HotDog) -> None:
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



#Main classes
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
        if len(self._missing_items) > 0:
            return False
        else:
            return True

    def produce(self):
        if self.check_items():
            self._items.update_items(self._bread, self._sausage, self._souse, self._additions)
            return HotDog(self._bread, self._sausage, self._souse, self._additions)
        else:
            print(f"We dont have enough items for this HotDog\nMissing items: {self._missing_items}")
            return None

class Builder2(BuilderABC):
    def __init__(self, items: Items) -> None:
        self._missing_items = None
        self._items = items
        self._bread = "Black"
        self._sausage = "Regular"
        self._souse = "Garlic"
        self._additions = ["Pickles"]

    def check_items(self):
        self._missing_items = self._items.check_item(self._bread, self._sausage, self._souse, self._additions)
        if len(self._missing_items) > 0:
            return False
        else:
            return True

    def produce(self):
        if self.check_items():
            self._items.update_items(self._bread, self._sausage, self._souse, self._additions)
            return HotDog(self._bread, self._sausage, self._souse, self._additions)
        else:
            print(f"We dont have enough items for this HotDog\nMissing items: {self._missing_items}")
            return None


class CustomBuilder(BuilderABC):
    def __init__(self, bread, sausage, souse, additions, items: Items) -> None:
        self._missing_items = None
        self._items = items
        self._bread = bread
        self._sausage = sausage
        self._souse = souse
        self._additions = additions

    def check_items(self):
        if self._bread not in self._items.ingredients["bread"]:
            print("We dont have such bread")
            return False
        if self._sausage not in self._items.ingredients["sausage"]:
            print("We dont have such sausage")
            return False
        if self._souse not in self._items.ingredients["souse"]:
            print("We dont have such souse")
            return False
        for i in self._additions:
            if i not in self._items.ingredients["additions"]:
                print(f"We dont have such addition {i}")
                return False

        self._missing_items = self._items.check_item(self._bread, self._sausage, self._souse, self._additions)
        if len(self._missing_items) > 0:
            return False
        else:
            return True

    def produce(self):
        if self.check_items():
            self._items.update_items(self._bread, self._sausage, self._souse, self._additions)
            return HotDog(self._bread, self._sausage, self._souse, self._additions)
        else:
            print(f"We dont have enough items for this HotDog\nMissing items: {self._missing_items}")
            return None


class Order(OrderABC):
    def __init__(self) -> None:
        self._current_order = []

    def add_item(self, hotdog) -> None:
        if hotdog:
            self._current_order.append(hotdog)
            self.display_order()

    def display_order(self):
        for i in self._current_order:
            i.display()

    def save_order(self):
        with open("file1.txt", "a") as file:
            for i in self._current_order:
                file.write(f"Hot dog: {i.get_full()}\n")

    def reset(self):
        self._current_order = []

    def get_order(self):
        return self._current_order

    def get_price(self):
        price = 0
        for i in self._current_order:
            price += i.get_price()
        return price


class Items(ItemsABC):
    def __init__(self) -> None:
        self._ingredients = {"bread" : {"White" : 10, "Black" : 9},
                             "sausage" : {"Regular" : 10, "Bavarian" : 8},
                             "souse" : {"Ketchup" : 10, "Garlic" : 8},
                             "additions" : {"Pickles" : 8, "Onions" : 6, "Chilli" : 5}
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

    @property
    def ingredients(self):
        return self._ingredients


class NoSale(SaleABC):
    def __init__(self) -> None:
        self._sale = None

    def count_sale(self, amount, price):
        self._sale = 0
        return self._sale


class WithSale(SaleABC):
    def __init__(self) -> None:
        self._sale = None

    def count_sale(self, amount, price):
        if 5 > amount >= 3:
            self._sale = price * 0.05
        else:
            self._sale = price * 0.1
        return self._sale


class Sale:
    def __init__(self, no_sale: NoSale, with_sale: WithSale) -> None:
        self._sale = None
        self._no_sale = no_sale
        self._with_sale = with_sale
        self._strategy = self._no_sale

    def choose_strategy(self, order):
        if len(order.get_order()) >=3:
            self._strategy = self._with_sale
        else:
            self._strategy = self._no_sale

    def apply_sale(self, order):
        self.choose_strategy(order)
        amount = len(order.get_order())
        price = 0
        for i in order.get_order():
            price += i.get_price()
        self._sale = self._strategy.count_sale(amount, price)
        return self._sale

class Strategy1:
    def __init__(self, order: Order, items: Items) -> None:
        self._order = order
        self._items = items

    def produce_hotdog(self):
        hotdog = Builder1(items).produce()
        order.add_item(hotdog)

class Strategy2:
    def __init__(self, order: Order, items: Items) -> None:
        self._order = order
        self._items = items

    def produce_hotdog(self):
        hotdog = Builder2(items).produce()
        order.add_item(hotdog)

class Strategy3:
    def __init__(self, order: Order, items: Items) -> None:
        self._order = order
        self._items = items

    def produce_hotdog(self, bread, sausage, souse, additions):
        hotdog = CustomBuilder(bread, sausage, souse, additions, self._items).produce()
        self._order.add_item(hotdog)

class Strategy:
    def __init__(self, order: Order, items: Items, strategy1: Strategy1, strategy2: Strategy2, strategy3: Strategy3) -> None:
        self._order = order
        self._items = items
        self._strategy1 = strategy1
        self._strategy2 = strategy2
        self._strategy3 = strategy3
        self._strategy = None

    def choose_strategy(self, option):
        if option == "First":
            self._strategy = self._strategy1
        elif option == "Second":
            self._strategy = self._strategy2
        elif option == "Custom":
            self._strategy = self._strategy3

    def produce_hotdog(self, bread, sausage, souse, additions):
        if self._strategy == self._strategy3:
            self._strategy.produce_hotdog(bread, sausage, souse, additions)
        else:
            self._strategy.produce_hotdog()

class Director:
    def __init__(self, order: Order, items: Items, strategy: Strategy, no_sale: NoSale, with_sale: WithSale) -> None:
        self._order = order
        self._items = items
        self._strategy = strategy
        self._no_sale = no_sale
        self._with_sale = with_sale

    def action(self, option, bread, sausage, souse, additions):
        if option == "First" or option == "Custom" or option == "Second":
            self._strategy.choose_strategy(option)
            self._strategy.produce_hotdog(bread, sausage, souse, additions)
            self._items.alert()
            self._order.save_order()
        elif option == "Finish":
            self.finish_order()
            self._order.save_order()
        else:
            print("Invalid option.")

    def finish_order(self):
        sale = Sale(self._no_sale, self._with_sale).apply_sale(self._order)
        price = order.get_price() - sale
        print(f"Your total price is {price} with applied sale {sale}")
