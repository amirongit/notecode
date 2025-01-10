def max_diff_between_two_elements(arr: list[int]) -> int:
    min_val = arr[0]
    max_dif = 0
    for number in arr:
        max_dif = max(max_dif, number - min_val)
        min_val = min(min_val, number)
    return max_dif
