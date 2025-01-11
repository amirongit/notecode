def maximum_difference_group(arr: list[int], k: int) -> int:
    sorted_arr = sorted(arr)
    return max(
        abs(sum(sorted_arr[:k]) - sum(sorted_arr[k:])),
        abs(sum(sorted_arr[:-k]) - sum(sorted_arr[-k:]))
    )
