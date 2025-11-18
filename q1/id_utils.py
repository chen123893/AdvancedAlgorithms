import random

def generate_random_product_id(existing_ids: set) -> str:
    """Generate a unique product ID of the form 'P########'"""
    while True:
        random_digits = random.randint(10000000, 99999999)
        product_id = f"P{random_digits}"
        if product_id not in existing_ids:
            existing_ids.add(product_id)
            return product_id
