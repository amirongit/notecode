def longest_consecutive_subsequence(arr: list[int]) -> int:
    longest_seq = 1
    for potential_beginner in arr:
        if potential_beginner - 1 not in arr:
            new_seq = 1
            next_ = potential_beginner + 1
            while next_ in arr:
                new_seq += 1
                next_ += 1
            longest_seq = max(new_seq, longest_seq)
    return longest_seq
