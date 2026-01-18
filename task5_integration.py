"""
Task 5: Complete Integration with Car Generator (Synchronous Version)
This is the main application that reads from cars.json and processes all cars.
"""

import json
from typing import Dict
from task2_interfaces import ServiceStats
from task4_semaphore import Semaphore


class CarServiceApplication:
    """Main application to process cars from generator."""
    
    def __init__(self):
        """Initialize the application."""
        self.semaphore = Semaphore()
        self.dining_count = 0
        self.not_dining_count = 0
    
    def load_and_process_cars(self, filepath: str = "cars.json") -> None:
        """
        Load cars from JSON file and process them.
        
        Args:
            filepath: Path to the JSON file containing car data
        """
        try:
            with open(filepath, 'r') as f:
                cars_data = json.load(f)
            
            print(f"Loaded {len(cars_data)} cars from {filepath}")
            print("=" * 50)
            
            # Route each car to appropriate station
            for car_data in cars_data:
                car_json = json.dumps(car_data)
                self.semaphore.route_car_from_json(car_json)
                
                # Track dining statistics
                if car_data["isDining"]:
                    self.dining_count += 1
                else:
                    self.not_dining_count += 1
            
            # Serve all cars
            print("\n" + "=" * 50)
            self.semaphore.serve_all_cars()
            
            # Print final statistics
            self.print_statistics()
            
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            print("Please run the generator script first to create cars.json")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{filepath}'")
    
    def print_statistics(self) -> None:
        """Print statistics in the format matching the generator output."""
        stats = ServiceStats().get_stats()
        
        # Build output matching generator format
        output = {
            "ELECTRIC": stats["ELECTRIC"],
            "GAS": stats["GAS"],
            "PEOPLE": stats["PEOPLE"],
            "ROBOTS": stats["ROBOTS"],
            "DINING": self.dining_count,
            "NOT_DINING": self.not_dining_count,
            "CONSUMPTION": stats["CONSUMPTION"]
        }
        
        print("=" * 50)
        print("FINAL STATISTICS:")
        print("=" * 50)
        print(json.dumps(output, indent=4))
        print("=" * 50)
        
        return output
    
    def get_statistics(self) -> Dict:
        """Get the current statistics."""
        stats = ServiceStats().get_stats()
        return {
            "ELECTRIC": stats["ELECTRIC"],
            "GAS": stats["GAS"],
            "PEOPLE": stats["PEOPLE"],
            "ROBOTS": stats["ROBOTS"],
            "DINING": self.dining_count,
            "NOT_DINING": self.not_dining_count,
            "CONSUMPTION": stats["CONSUMPTION"]
        }


def main():
    """Main entry point for the application."""
    print("=" * 50)
    print("CAR SERVICE STATION APPLICATION")
    print("=" * 50)
    print()
    
    # Reset statistics
    ServiceStats().reset()
    
    # Create and run application
    app = CarServiceApplication()
    app.load_and_process_cars("cars.json")
    
    print("\nApplication completed successfully!")


if __name__ == '__main__':
    main()


# ============== TESTS ==============
import unittest
import os
import tempfile


class TestCarServiceApplication(unittest.TestCase):
    """Test suite for complete application integration."""
    
    def setUp(self):
        """Reset stats before each test."""
        ServiceStats().reset()
    
    def test_process_sample_cars(self):
        """Test processing a sample set of cars."""
        # Create temporary JSON file
        sample_data = [
            {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": False, "consumption": 42},
            {"id": 2, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": False, "consumption": 26},
            {"id": 3, "type": "GAS", "passengers": "ROBOTS", "isDining": True, "consumption": 41},
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(sample_data, f)
            temp_file = f.name
        
        try:
            app = CarServiceApplication()
            app.load_and_process_cars(temp_file)
            
            stats = app.get_statistics()
            
            # Verify statistics
            self.assertEqual(stats["ELECTRIC"], 2)
            self.assertEqual(stats["GAS"], 1)
            self.assertEqual(stats["PEOPLE"], 0)  # None dining
            self.assertEqual(stats["ROBOTS"], 1)  # One dining
            self.assertEqual(stats["DINING"], 1)
            self.assertEqual(stats["NOT_DINING"], 2)
            self.assertEqual(stats["CONSUMPTION"]["ELECTRIC"], 68)
            self.assertEqual(stats["CONSUMPTION"]["GAS"], 41)
        finally:
            os.unlink(temp_file)
    
    def test_all_combinations(self):
        """Test all possible car type combinations."""
        sample_data = [
            {"id": 1, "type": "ELECTRIC", "passengers": "PEOPLE", "isDining": True, "consumption": 20},
            {"id": 2, "type": "ELECTRIC", "passengers": "ROBOTS", "isDining": True, "consumption": 25},
            {"id": 3, "type": "GAS", "passengers": "PEOPLE", "isDining": True, "consumption": 30},
            {"id": 4, "type": "GAS", "passengers": "ROBOTS", "isDining": False, "consumption": 35},
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(sample_data, f)
            temp_file = f.name
        
        try:
            app = CarServiceApplication()
            app.load_and_process_cars(temp_file)
            
            stats = app.get_statistics()
            
            self.assertEqual(stats["ELECTRIC"], 2)
            self.assertEqual(stats["GAS"], 2)
            self.assertEqual(stats["PEOPLE"], 2)
            self.assertEqual(stats["ROBOTS"], 1)
            self.assertEqual(stats["DINING"], 3)
            self.assertEqual(stats["NOT_DINING"], 1)
        finally:
            os.unlink(temp_file)
    
    def test_large_batch_processing(self):
        """Test processing a large batch of cars."""
        # Simulate 30 cars like the generator
        sample_data = []
        for i in range(1, 31):
            sample_data.append({
                "id": i,
                "type": "ELECTRIC" if i % 2 == 0 else "GAS",
                "passengers": "PEOPLE" if i % 3 == 0 else "ROBOTS",
                "isDining": i % 2 == 1,
                "consumption": 20 + (i % 30)
            })
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(sample_data, f)
            temp_file = f.name
        
        try:
            app = CarServiceApplication()
            app.load_and_process_cars(temp_file)
            
            stats = app.get_statistics()
            
            # Verify counts add up correctly
            self.assertEqual(stats["ELECTRIC"] + stats["GAS"], 30)
            self.assertEqual(stats["DINING"] + stats["NOT_DINING"], 30)
            
            # Verify consumption is tracked
            total_consumption = (stats["CONSUMPTION"]["ELECTRIC"] + 
                               stats["CONSUMPTION"]["GAS"])
            self.assertGreater(total_consumption, 0)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    # Run main application or tests based on context
    import sys
    if '--test' in sys.argv:
        sys.argv.remove('--test')
        unittest.main()
    else:
        main()
