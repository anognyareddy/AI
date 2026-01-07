import time
import statistics


def bubble_sort(arr):
    """In-place bubble sort"""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def insertion_sort(arr):
    """In-place insertion sort"""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def time_sort(sort_fn, data, trials=5):
    """Time sort_fn over copies of data for `trials` runs. Returns list of seconds."""
    times = []
    for _ in range(trials):
        data_copy = data.copy()
        t0 = time.perf_counter()
        sort_fn(data_copy)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return times


def verify_sorted(sorted_list, reference):
    if sorted_list != reference:
        raise RuntimeError("Sort implementation produced incorrect result")


def parse_input_list(s):
    # Accept numbers separated by spaces and/or commas
    if not s.strip():
        return []
    parts = s.replace(",", " ").split()
    return [int(p) for p in parts]


def format_list_preview(lst, limit=20):
    if len(lst) <= limit:
        return str(lst)
    return f"{lst[:limit]} ... (total {len(lst)} items)"


if __name__ == "__main__":
    try:
        raw = input("Enter integers separated by spaces or commas: ")
        data = parse_input_list(raw)
    except ValueError:
        print("Invalid input. Please enter only integers separated by spaces or commas.")
        raise SystemExit(1)

    if not data:
        print("No numbers provided. Exiting.")
        raise SystemExit(0)

    reference = sorted(data)

    # Run several trials to reduce noise
    trials = 5
    times_b = time_sort(bubble_sort, data, trials=trials)
    times_i = time_sort(insertion_sort, data, trials=trials)

    sorted_bubble = bubble_sort(data.copy())
    sorted_insertion = insertion_sort(data.copy())

    # correctness checks
    verify_sorted(sorted_bubble, reference)
    verify_sorted(sorted_insertion, reference)

    def stats(times):
        return statistics.mean(times), statistics.stdev(times) if len(times) > 1 else 0.0

    mean_b, stdev_b = stats(times_b)
    mean_i, stdev_i = stats(times_i)

    print()
    print(f"Original (preview): {format_list_preview(data)}")
    print(f"Sorted (reference, preview): {format_list_preview(reference)}")
    print()
    print(f"Bubble sort:    mean={mean_b:.6f}s  stdev={stdev_b:.6f}s  (over {trials} runs)")
    print(f"Insertion sort: mean={mean_i:.6f}s  stdev={stdev_i:.6f}s  (over {trials} runs)")

