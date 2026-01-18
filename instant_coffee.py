# instant_coffee.py

"""
Defines the InstantCoffee base class and a subclass ThreeInOne.
These represent instant coffee drinks (dissolvable powders).
"""
from brewable import Brewable

class InstantCoffee(Brewable):
    """Base class for instant coffee drinks (made with soluble powder)."""
    def brew(self):
        # Generic brewing process for instant coffee
        print("Stirring instant coffee powder into hot water...")
        # (Instant coffee is made by dissolving coffee powder in hot water.)

    def __str__(self):
        return "a cup of instant coffee"

class ThreeInOne(InstantCoffee):
    """3-in-1 instant coffee (coffee, sugar, and creamer all-in-one)."""
    def brew(self):
        # Specific brewing process for 3-in-1 coffee
        print("Mixing a 3-in-1 coffee packet with hot water...")
        # (3-in-1 packets contain coffee, sugar, and creamer together.)

    def __str__(self):
        return "a cup of 3-in-1 instant coffee"
