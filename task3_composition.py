"""
Task 3: CarStation with Composition, IoC and Dependency Injection
This module combines Queue, Dineable, and Refuelable using dependency injection.
"""

from typing import Optional
from task1_queues import Queue, ArrayQueue
from task2_interfaces import Dineable, Refuelable


class Car:
    """Represents a car with properties."""
    
    def __init__(self, car_id: int, car_type: str, passengers: str, 
                 is_dining: bool, consumption: int):
        self.id = car_id
        self.type = car_type
        self.passengers = passengers
        self.is_dining = is_dining
        self.consumption = consumption
    
    def __repr__(self):
        return (f"Car(id={self.id}, type={self.type}, passengers={self.passengers}, "
                f"is_dining={self.is_dining}, consumption={self.consumption})")


class CarStation:
    """
    Car service station that composes dining, refueling, and queue services.
    Uses Dependency Injection for flexibility.
    """
    
    def __init__(self, 
                 dining_service: Optional[Dineable],
                 refueling_service: Refuelable,
                 queue: Queue[Car]):
        """
        Initialize CarStation with injected dependencies.
        
        Args:
            dining_service: Optional dining service (can be None if no dining)
            refueling_service: Refueling service (required)
            queue: Queue implementation to hold cars
        """
        self.dining_service = dining_service
        self.refueling_service = refueling_service
        self.queue = queue
    
    def add_car(self, car: Car) -> None:
        """Add a car to the station's queue."""
        self.queue.enqueue(car)
    
    def serve_cars(self) -> None:
        """
        Serve all cars in the queue.
        For each car: serve dinner (if needed), refuel, then dequeue.
        """
        while not self.queue.is_empty():
            car = self.queue.dequeue()
            if car is None:
                break
            
            # Serve dinner if car wants dining and we have dining service
            if car.is_dining and self.dining_service is not None:
                self.dining_service.serve_dinner(car.id)
            
            # Refuel the car
            self.refueling_service.refuel(car.id, car.consumption)
            
            print(f"Car {car.id} serviced and departed")


# ============== TESTS ==============
import unittest
from task2_interfaces import (PeopleDinner, RobotDinner, 
                               ElectricStation, GasStation, ServiceStats)


class TestCarStation(unittest.TestCase):
    """Test suite for CarStation composition."""
    
    def setUp(self):
        """Reset stats before each test."""
        ServiceStats().reset()
    
    def test_add_car_to_queue(self):
        """Test adding cars to the station queue."""
        queue = ArrayQueue()
        station = CarStation(
            dining_service=PeopleDinner(),
            refueling_service=ElectricStation(),
            queue=queue
        )
        
        car1 = Car(1, "ELECTRIC", "PEOPLE", True, 25)
        car2 = Car(2, "ELECTRIC", "PEOPLE", False, 30)
        
        station.add_car(car1)
        station.add_car(car2)
        
        self.assertEqual(station.queue.size(), 2)
    
    def test_serve_cars_with_dining(self):
        """Test serving cars that want to dine."""
        queue = ArrayQueue()
        station = CarStation(
            dining_service=PeopleDinner(),
            refueling_service=ElectricStation(),
            queue=queue
        )
        
        car = Car(1, "ELECTRIC", "PEOPLE", True, 25)
        station.add_car(car)
        station.serve_cars()
        
        self.assertTrue(station.queue.is_empty())
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["PEOPLE"], 1)
        self.assertEqual(stats["ELECTRIC"], 1)
    
    def test_serve_cars_without_dining(self):
        """Test serving cars that don't want to dine."""
        queue = ArrayQueue()
        station = CarStation(
            dining_service=None,
            refueling_service=GasStation(),
            queue=queue
        )
        
        car = Car(1, "GAS", "PEOPLE", False, 40)
        station.add_car(car)
        station.serve_cars()
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["GAS"], 1)
        self.assertEqual(stats["PEOPLE"], 0)  # No dining service
    
    def test_multiple_cars_served_in_order(self):
        """Test that multiple cars are served in FIFO order."""
        queue = ArrayQueue()
        station = CarStation(
            dining_service=RobotDinner(),
            refueling_service=ElectricStation(),
            queue=queue
        )
        
        car1 = Car(1, "ELECTRIC", "ROBOTS", True, 20)
        car2 = Car(2, "ELECTRIC", "ROBOTS", True, 30)
        car3 = Car(3, "ELECTRIC", "ROBOTS", False, 25)
        
        station.add_car(car1)
        station.add_car(car2)
        station.add_car(car3)
        
        station.serve_cars()
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["ROBOTS"], 2)  # Only 2 dined
        self.assertEqual(stats["ELECTRIC"], 3)  # All 3 refueled
        self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 75)
    
    def test_mixed_dining_preferences(self):
        """Test station with mixed dining preferences."""
        queue = ArrayQueue()
        station = CarStation(
            dining_service=PeopleDinner(),
            refueling_service=GasStation(),
            queue=queue
        )
        
        cars = [
            Car(1, "GAS", "PEOPLE", True, 30),
            Car(2, "GAS", "PEOPLE", False, 35),
            Car(3, "GAS", "PEOPLE", True, 40),
        ]
        
        for car in cars:
            station.add_car(car)
        
        station.serve_cars()
        
        stats = ServiceStats().get_stats()
        self.assertEqual(stats["PEOPLE"], 2)  # 2 dined
        self.assertEqual(stats["GAS"], 3)  # All 3 refueled
        self.assertEqual(stats["CONSUMPTION"]["GAS"], 105)


if __name__ == '__main__':
    unittest.main()
