from typing import Optional, List
"""Hash table using separate chaining (array of lists)."""

class HashTable:
    def __init__(self, size: int = 100):
        self.size = size
        self.table: List[list] = [[] for _ in range(size)]

    def hash_function(self, key: str) -> int:
        # e.g. 'P12345678'; ignores the 'P' and uses the numeric portion
        numeric_key = int(key[1:])
        return numeric_key % self.size

    def insert(self, product) -> None:
        index = self.hash_function(product.product_id)
        for item in self.table[index]:
            # if got duplicate, replace to new one
            if item.product_id == product.product_id:
                item.name = product.name
                item.product_type = product.product_type
                item.price = product.price
                item.quantity = product.quantity
                return
        # add new product
        self.table[index].append(product)

    def search(self, product_id: str):
        index = self.hash_function(product_id)
        for item in self.table[index]:
            if item.product_id == product_id:
                return item
        return None

    def edit(self, product_id: str, name=None, product_type=None, price=None,
             quantity=None) -> bool:
        product = self.search(product_id)
        if product:
            if name:
                product.name = name
            if product_type:
                product.product_type = product_type
            if price is not None:
                product.price = price
            if quantity is not None:
                product.quantity = quantity
            print("Product updated successfully!")
            return True
        else:
            print("Product not found.")
            return False

    def delete(self, product_id: str) -> bool:
        index = self.hash_function(product_id)
        bucket = self.table[index]
        for i, item in enumerate(bucket):
            if item.product_id == product_id:
                del bucket[i]
                return True
        return False

    def display_id(self) -> None:
        print("\n===== PRODUCT IDS IN HASH TABLE =====")
        for i, bucket in enumerate(self.table):
            print(f"Bucket {i}: ", end="")
            if not bucket:
                print("[]")
            else:
                print(", ".join(item.product_id for item in bucket))

    def display_items(self) -> None:
        print("\n===== INVENTORY RECORDS =====")
        for i, bucket in enumerate(self.table):
            print(f"Bucket {i}: ", end="")
            if not bucket:
                print("[]")
            else:
                print(", ".join(str(item) for item in bucket))

    def get_all_products(self):
        products = []
        for bucket in self.table:
            products.extend(bucket)
        return products
