def low_iq(arr: list[int]) -> int:
    max_diff: int = 0
    for fidx, fnum in enumerate(arr):
        for snum in arr[fidx + 1:]:
            max_diff = max(snum - fnum, max_diff)

    return max_diff


def maxDiff(arr: list[int]) -> int:
    if len(arr) < 2:
        return 0

    min_val = arr[0]
    max_diff = 0

    for num in arr[1:]:
        max_diff = max(max_diff, num - min_val)
        min_val = min(min_val, num)

    return max_diff
