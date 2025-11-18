import time
import matplotlib.pyplot as plt
from baby_product import BabyProduct
from id_utils import generate_random_product_id


def compare_hash_vs_array_performance(hash_table) -> None:
    """Compare search performance between hash table and array data structures."""
    print("\n========== HASH TABLE VS ARRAY PERFORMANCE ==========")

    # Get all products from hash table as array representation
    array_data = hash_table.get_all_products()
    if not array_data:
        print("No data available in hash table. Please insert some records first.")
        return

    # Define test data sizes
    data_sizes = [10, 50, 100, 200, 500, 1000]
    ht_times = []  # Hash table search times
    arr_times = []  # Array search times

    # Prepare test data, copy to get till 1000
    all_products = array_data.copy()
    existing_ids = set(p.product_id for p in all_products)

    # Generate additional products if needed to reach 1000 items
    while len(all_products) < 1000:
        pid = generate_random_product_id(existing_ids)
        all_products.append(BabyProduct(pid, "Sample", "Misc", 50, 10))
        hash_table.insert(all_products[-1])

    # Measure search performance for different data sizes
    for n in data_sizes:
        subset = all_products[:n]  # Take first n products
        test_id = subset[-1].product_id  # Use last product ID as search target

        # Hash Table search performance measurement
        start_ht = time.time()
        for _ in range(100):
            hash_table.search(test_id)
        # Convert to microseconds
        ht_avg = (time.time() - start_ht) / 100 * 1e6
        ht_times.append(ht_avg)

        # Array search performance measurement
        start_arr = time.time()
        for _ in range(100):
            for item in subset:
                if item.product_id == test_id:
                    break
        arr_avg = (time.time() - start_arr) / 100 * 1e6
        arr_times.append(arr_avg)

    # Display table format
    print("\nPerformance Comparison Results")
    print("---------------------------------------------------")
    print(f"{'Data Size':<10}{'Hash Table (µs)':>20}{'Array (µs)':>20}")
    print("---------------------------------------------------")
    for n, ht_t, arr_t in zip(data_sizes, ht_times, arr_times):
        print(f"{n:<10}{ht_t:>20.4f}{arr_t:>20.4f}")
    print("---------------------------------------------------")

    # Create graph
    plt.figure(figsize=(8, 5))
    plt.plot(data_sizes, ht_times, marker='o', label="Hash Table Search (O(1))")
    plt.plot(data_sizes, arr_times, marker='o', label="1D Array Search (O(n))")
    plt.title("Hash Table vs Array Search Performance")
    plt.xlabel("Number of Records")
    plt.ylabel("Average Search Time (µs)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()