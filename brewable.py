# brewable.py

"""
Abstract base class for all brewable coffee types.
Defines the interface (methods) that all coffee types must implement.
"""
from abc import ABC, abstractmethod

class Brewable(ABC):
    @abstractmethod
    def brew(self):
        """Abstract method to brew the coffee. Each subclass should implement this."""
        pass

    @abstractmethod
    def __str__(self):
        """Abstract method to describe the coffee as a string."""
        pass
