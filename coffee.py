# coffee.py

"""
Defines the Coffee base class and two subclasses: Espresso and Latte.
All these are brewable (brewed coffee drinks).
"""
from brewable import Brewable

class Coffee(Brewable):
    """Base class for brewed coffee drinks."""
    def brew(self):
        # Generic brewing process for a basic coffee
        print("Brewing a basic coffee...")
        # (In a real scenario, this might involve steps like grinding beans, pouring hot water, etc.)
        # For simplicity, we'll just print a message.

    def __str__(self):
        return "a cup of generic coffee"

class Espresso(Coffee):
    """Espresso coffee, subclass of Coffee."""
    def brew(self):
        # Specific brewing process for Espresso
        print("Pulling a shot of espresso...")
        # (Espresso is brewed by forcing hot water under pressure through finely ground coffee.)

    def __str__(self):
        return "a small, strong espresso"

class Latte(Coffee):
    """Latte coffee, subclass of Coffee."""
    def brew(self):
        # Specific brewing process for Latte
        print("Brewing an espresso and adding steamed milk for a latte...")
        # (A latte is made with espresso and hot milk.)

    def __str__(self):
        return "a creamy latte coffee"
