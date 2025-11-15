from threading import Thread
import time
from statistics import mean
from typing import List, Tuple
import matplotlib.pyplot as plt


# 1. FACTORIAL FUNCTION
def compute_factorial(n: int) -> int:
    """Compute factorial in a simple loop."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


# 2. MULTITHREAD TEST
def run_factorials_multithread(numbers: List[int], rounds: int = 10) -> Tuple[List[int], float]:
    """Run factorials using threads and measure total time per round."""
    times = []

    for _ in range(rounds):
        threads = []
        start_times = []
        end_times = []

        # Work done inside each thread
        def worker(num: int):
            start = time.time_ns()
            compute_factorial(num)
            end = time.time_ns()
            start_times.append(start)
            end_times.append(end)

        # Create one thread per number
        for num in numbers:
            t = Thread(target=worker, args=(num,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total_ns = max(end_times) - min(start_times)
        times.append(total_ns)

    return times, mean(times)


# 3. SINGLE-THREAD TEST
def run_factorials_singlethread(numbers: List[int], rounds: int = 10) -> Tuple[List[int], float]:
    """Run factorials in sequence (no threads) and measure time."""
    times = []

    for _ in range(rounds):
        start = time.time_ns()
        for num in numbers:
            compute_factorial(num)
        end = time.time_ns()
        times.append(end - start)

    return times, mean(times)


# 4. GRAPH PLOTTING
def plot_results(mt_times_ns: List[int], st_times_ns: List[int]) -> None:
    """Create graphs for round-by-round time and average time."""
    # Convert nanoseconds → milliseconds
    mt_ms = [t / 1e6 for t in mt_times_ns]
    st_ms = [t / 1e6 for t in st_times_ns]
    rounds = list(range(1, len(mt_ms) + 1))

    # -------- Graph 1: Line graph (time per round) --------
    plt.figure(figsize=(8, 5))
    plt.plot(rounds, mt_ms, marker="o", label="Multithread")
    plt.plot(rounds, st_ms, marker="s", label="Single-thread")
    plt.title("Execution Time Per Round")
    plt.xlabel("Round")
    plt.ylabel("Time (ms)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig("q3_times_per_round.png", dpi=300)

    # -------- Graph 2: Bar chart (average time) --------
    plt.figure(figsize=(6, 5))
    plt.bar(["Multithread", "Single-thread"], [mean(mt_ms), mean(st_ms)])
    plt.title("Average Execution Time")
    plt.ylabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("q3_average_times.png", dpi=300)

    plt.show()


# 5. MAIN EXPERIMENT
def main():

    factorial_numbers = [50, 100, 200]
    rounds = 10

    print("QUESTION 3 – CONCURRENT PROCESS TEST")
    print("Numbers:", factorial_numbers)
    print("Rounds :", rounds)
    print("=" * 40)

    # --- Multithread run ---
    mt_times, mt_avg = run_factorials_multithread(factorial_numbers, rounds)
    print("\n[Multithreading] Times per round (ns)")
    for i, t in enumerate(mt_times, 1):
        print(f"Round {i:02d}: {t:,}")
    print(f"Average: {mt_avg:,.0f} ns")

    # --- Single-thread run ---
    st_times, st_avg = run_factorials_singlethread(factorial_numbers, rounds)
    print("\n[Single-thread] Times per round (ns)")
    for i, t in enumerate(st_times, 1):
        print(f"Round {i:02d}: {t:,}")
    print(f"Average: {st_avg:,.0f} ns")

    # --- Summary ---
    print("\n[Summary]")
    speedup = (mt_avg/st_avg)*100 if mt_avg > 0 else 0
    print(f"Avg Multi-thread : {mt_avg:,.0f} ns")
    print(f"Avg Single-thread: {st_avg:,.0f} ns")
    print(f"Speedup %: {speedup:.2f}%")

    # Create graphs
    plot_results(mt_times, st_times)


# 6. RUN PROGRAM
if __name__ == "__main__":
    main()
