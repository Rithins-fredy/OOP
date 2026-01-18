# main.py

"""
Main program to demonstrate brewing different types of coffee using a unified interface.
"""
from coffee import Coffee, Espresso, Latte
from instant_coffee import InstantCoffee, ThreeInOne

if __name__ == "__main__":
    # Create one object of each coffee type
    generic_coffee = Coffee()
    espresso = Espresso()
    latte = Latte()
    instant = InstantCoffee()
    three_in_one = ThreeInOne()

    # Put all coffee objects in a list (they are all Brewable)
    coffees = [generic_coffee, espresso, latte, instant, three_in_one]

    # Brew each coffee and print its description
    for coffee in coffees:
        coffee.brew()
        # After brewing, print the coffee description (calls the object's __str__ method)
        print(f"Brewed {coffee}")
        print("-" * 40)
