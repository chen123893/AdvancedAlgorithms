import csv

def export_to_csv(hash_table, filename: str = "baby_products.csv") -> None:
    products_exist = False
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Table Index", "Product IDs"])
        for i, bucket in enumerate(hash_table.table):
            if bucket:
                products_exist = True
                product_ids = ", ".join(p.product_id for p in bucket)
                writer.writerow([i, product_ids])
    if products_exist:
        print(f"\nExported all product IDs (grouped by table index) to '{filename}' successfully!")
    else:
        print("No products in the hash table to export.")
