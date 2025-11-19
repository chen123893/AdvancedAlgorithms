from baby_product import BabyProduct
from hash_table import HashTable
from id_utils import generate_random_product_id
from sample_data import generate_sample_data
from exporter import export_to_csv
from performance import compare_hash_vs_array_performance

def inventory_system() -> None:
    ht = HashTable(size=100)
    generate_sample_data(ht, count=30)
    #keep track used id
    used_ids = set(p.product_id for p in ht.get_all_products())

    while True:
        print("\n====== Baby Product Inventory ======")
        print("1. Insert Product (Auto Random ID)")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. Display All ID")
        print("6. Display All With Details")
        print("7. Compare Hash Table vs Array Performance (Graph)")
        print("8. Export to CSV")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            name = input("Enter Product Name: ")
            product_type = input("Enter Product Type: ")
            try:
                price = float(input("Enter Price: "))
                qty = int(input("Enter Quantity: "))
            except ValueError:
                print("Invalid numeric value for price or quantity.")
                continue
            product_id = generate_random_product_id(used_ids)
            product = BabyProduct(product_id, name, product_type, price, qty)
            ht.insert(product)
            used_ids.add(product_id)
            print(f"Product inserted successfully! Assigned ID: {product_id}")

        elif choice == "2":
            pid = input("Enter Product ID to search (e.g. P12345678): ").strip()#remove spacing
            result = ht.search(pid)
            print("Product Found:" if result else "Product not found.")
            if result:
                print(result)

        elif choice == "3":
            pid = input("Enter Product ID to edit (e.g. P12345678): ").strip()
            product = ht.search(pid)
            if product:
                print("Editing:", product)
                new_name = input("Enter new name (leave blank to keep current): ")
                new_type = input("Enter new type (leave blank to keep current): ")
                new_price = input("Enter new price (leave blank to keep current): ")
                new_qty = input("Enter new quantity (leave blank to keep current): ")
                try:
                    price_val = float(new_price) if new_price else None
                    qty_val = int(new_qty) if new_qty else None
                except ValueError:
                    print("Invalid numeric value for price or quantity.")
                    continue
                ht.edit(
                    pid,
                    name=new_name or None,
                    product_type=new_type or None,
                    price=price_val,
                    quantity=qty_val,
                )
            else:
                print("Product not found.")

        elif choice == "4":
            pid = input("Enter Product ID to delete (e.g. P12345678): ").strip()
            if ht.delete(pid):
                used_ids.discard(pid)
                print("Product deleted successfully!")
            else:
                print("Product not found.")

        elif choice == "5":
            ht.display_id()

        elif choice == "6":
            ht.display_items()

        elif choice == "7":
            compare_hash_vs_array_performance(ht)

        elif choice == "8":
            export_to_csv(ht)

        elif choice == "9":
            print("Exiting Inventory System...")
            break

        else:
            print("Invalid choice. Try again.")



if __name__ == "__main__":
    inventory_system()
