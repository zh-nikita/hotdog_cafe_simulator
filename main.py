from classes import Order, Items, Strategy, Strategy1, Strategy2, Strategy3, Director, NoSale, WithSale


def main():
    order = Order()
    items = Items()
    strategy = Strategy(order, items, Strategy1(order, items), Strategy2(order, items), Strategy3(order, items))
    director = Director(order, items, strategy, NoSale(), WithSale())

    while True:
        option = input("First - Bavarian | Second - Regular | Custom - Custom Hotdog | Finish - Exit\nEnter: ").strip()

        if option == "Custom":
            additions = []
            bread = input("Bread: ")
            sausage = input("Sausage: ")
            souse = input("Souse: ")
            n = int(input("Number of additions: "))
            for _ in range(n):
                additions.append(input("Addition: "))
            director.action(option, bread, sausage, souse, additions)

        elif option == "Finish":
            director.action(option, None, None, None, None)
            break

        else:
            director.action(option, None, None, None, None)


if __name__ == "__main__":
    main()
