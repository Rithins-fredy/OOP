# main.py

from system import Store, Notebook, Pen, Customer

store = Store("Campus Stationery")

notebook1 = Notebook("Oxford Notebook", 120, "hard", "A5", 5.99)
pen1 = Pen("Parker Pen", "blue", 2.49)

store.add_item(notebook1)
store.add_item(pen1)

customer = Customer("Alice")

store.sell_item(customer, "Oxford Notebook")
store.sell_item(customer, "Parker Pen")

customer.list_items()

# Simulate writing
notebook1.write_page()
pen1.write()
