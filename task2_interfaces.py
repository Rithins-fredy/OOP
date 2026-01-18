"""
Task 2: Dineable and Refuelable Interfaces with Implementations
This module provides interface segregation for dining and refueling services.
"""

from abc import ABC, abstractmethod


class Dineable(ABC):
    """Abstract interface for dining services."""
    
    @abstractmethod
    def serve_dinner(self, car_id: int) -> None:
        """Serve dinner to passengers in the car."""
        pass


class Refuelable(ABC):
    """Abstract interface for refueling services."""
    
    @abstractmethod
    def refuel(self, car_id: int) -> None:
        """Refuel the car."""
        pass


# Global statistics tracker (shared across all instances)
class ServiceStats:
    """Singleton to track statistics across all service stations."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reset()
        return cls._instance
    
    def reset(self):
        """Reset all statistics."""
        self.people_count = 0
        self.robots_count = 0
        self.electric_count = 0
        self.gas_count = 0
        self.electric_consumption = 0
        self.gas_consumption = 0
    
    def get_stats(self):
        """Get current statistics."""
        return {
            "ELECTRIC": self.electric_count,
            "GAS": self.gas_count,
            "PEOPLE": self.people_count,
            "ROBOTS": self.robots_count,
            "CONSUMPTION": {
                "ELECTRIC": self.electric_consumption,
                "GAS": self.gas_consumption
            }
        }


class PeopleDinner(Dineable):
    """Dining service for people."""
    
    def __init__(self):
        self.stats = ServiceStats()
    
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to people in car {car_id}")
        self.stats.people_count += 1


class RobotDinner(Dineable):
    """Dining service for robots."""
    
    def __init__(self):
        self.stats = ServiceStats()
    
    def serve_dinner(self, car_id: int) -> None:
        print(f"Serving dinner to robots in car {car_id}")
        self.stats.robots_count += 1


class ElectricStation(Refuelable):
    """Refueling service for electric cars."""
    
    def __init__(self):
        self.stats = ServiceStats()
    
    def refuel(self, car_id: int, consumption: int = 0) -> None:
        print(f"Refueling electric car {car_id}")
        self.stats.electric_count += 1
        self.stats.electric_consumption += consumption


class GasStation(Refuelable):
    """Refueling service for gas cars."""
    
    def __init__(self):
        self.stats = ServiceStats()
    
    def refuel(self, car_id: int, consumption: int = 0) -> None:
        print(f"Refueling gas car {car_id}")
        self.stats.gas_count += 1
        self.stats.gas_consumption += consumption


# ============== TESTS ==============
import unittest


class TestDineableAndRefuelable(unittest.TestCase):
    """Test suite for Dineable and Refuelable implementations."""
    
    def setUp(self):
        """Reset stats before each test."""
        ServiceStats().reset()
    
    def test_people_dinner_service(self):
        """Test PeopleDinner service."""
        dinner = PeopleDinner()
        dinner.serve_dinner(1)
        dinner.serve_dinner(2)
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["PEOPLE"], 2)
    
    def test_robot_dinner_service(self):
        """Test RobotDinner service."""
        dinner = RobotDinner()
        dinner.serve_dinner(1)
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["ROBOTS"], 1)
    
    def test_electric_station_service(self):
        """Test ElectricStation service."""
        station = ElectricStation()
        station.refuel(1, consumption=25)
        station.refuel(2, consumption=30)
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["ELECTRIC"], 2)
        self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 55)
    
    def test_gas_station_service(self):
        """Test GasStation service."""
        station = GasStation()
        station.refuel(1, consumption=40)
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["GAS"], 1)
        self.assertEqual(stats["CONSUMPTION"]["GAS"], 40)
    
    def test_multiple_stations_share_stats(self):
        """Test that multiple instances share statistics."""
        electric1 = ElectricStation()
        electric2 = ElectricStation()
        
        electric1.refuel(1, consumption=20)
        electric2.refuel(2, consumption=30)
        
        stats = ServiceStats().get_stats()
        # Should count as one electric station tracking both
        self.assertEqual(stats["ELECTRIC"], 2)
        self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 50)
    
    def test_no_dining_scenario(self):
        """Test cars that don't dine."""
        electric = ElectricStation()
        electric.refuel(1, consumption=25)
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["ELECTRIC"], 1)
        self.assertEqual(stats["PEOPLE"], 0)
        self.assertEqual(stats["ROBOTS"], 0)


if __name__ == '__main__':
    unittest.main()
