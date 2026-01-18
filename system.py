# system.py

class StationeryItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price:.2f}"

class Pen(StationeryItem):
    def __init__(self, name: str, color: str, price: float):
        super().__init__(name, price)
        self.color = color

    def write(self):
        print(f"Writing with {self.color} pen.")

class Notebook(StationeryItem):
    def __init__(self, name: str, page_count: int, cover_type: str, size: str, price: float):
        super().__init__(name, price)
        self.page_count = page_count
        self.cover_type = cover_type
        self.size = size
        self.pages_written = 0

    def write_page(self):
        if self.pages_written < self.page_count:
            self.pages_written += 1
            print(f"Written on page {self.pages_written}/{self.page_count}.")
        else:
            print("No more blank pages left!")

class Customer:
    def __init__(self, name: str):
        self.name = name
        self.items = []

    def buy_item(self, item: StationeryItem):
        self.items.append(item)
        print(f"{self.name} bought a {item.name}.")

    def list_items(self):
        print(f"{self.name}'s purchased items:")
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item}")

class Store:
    def __init__(self, name: str):
        self.name = name
        self.inventory = []

    def add_item(self, item: StationeryItem):
        self.inventory.append(item)
        print(f"{item.name} added to store inventory.")

    def sell_item(self, customer: Customer, item_name: str):
        for item in self.inventory:
            if item.name == item_name:
                customer.buy_item(item)
                self.inventory.remove(item)
                print(f"Sold {item_name} to {customer.name}.")
                return
        print(f"{item_name} not found in inventory.")
