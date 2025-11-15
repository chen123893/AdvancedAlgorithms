"""Entity class representing a baby product item."""
class BabyProduct:
    def __init__(self, product_id, name, product_type, price, quantity):
        self.product_id = product_id
        self.name = name
        self.product_type = product_type
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return (f"ID: {self.product_id}, Name: {self.name}, "
                f"Type: {self.product_type}, Price: RM{self.price:.2f}, Qty: {self.quantity}")
