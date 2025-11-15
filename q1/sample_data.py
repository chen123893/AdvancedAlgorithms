from baby_product import BabyProduct
from id_utils import generate_random_product_id
import random

def generate_sample_data(ht, count: int = 30) -> None:
    product_catalog = {
        "Diapering": ["Baby Diaper", "Diaper Cream", "Baby Wipes"],
        "Feeding": ["Baby Milk", "Feeding Bottle", "Baby Spoon Set"],
        "Bathing": ["Baby Shampoo", "Baby Soap", "Baby Lotion"],
        "Clothing": ["Baby Romper", "Baby Blanket", "Baby Bib"],
        "Healthcare": ["Baby Thermometer", "Baby Oil", "Baby Powder"]
    }

    used_ids = set()
    all_products = [(ptype, name) for ptype, names in product_catalog.items() for name in names]

    for _ in range(count):
        product_type, name = random.choice(all_products)
        price = round(random.uniform(10, 150), 2)
        quantity = random.randint(10, 100)
        product_id = generate_random_product_id(used_ids)
        product = BabyProduct(product_id, name, product_type, price, quantity)
        ht.insert(product)

    print(f"\n{count} sample baby products inserted successfully!\n")
