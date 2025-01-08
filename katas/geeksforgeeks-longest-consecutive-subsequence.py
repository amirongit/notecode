def low_iq(arr: list[int]) -> int:
    if len(arr) == 0:
        return 0

    sorted_arr = sorted(set(arr))
    highest_seq = 1

    former = sorted_arr.pop(0)
    seq = 1
    while len(sorted_arr) > 0:
        if (latter := sorted_arr.pop(0)) == former + 1:
            seq += 1
            former = latter
        else:
            highest_seq = max(seq, highest_seq)
            seq = 1

    return highest_seq


def retard(arr: list[int]) -> int:
    if len(arr) == 0:
        return 0

    table = {item: ((item - 1) in arr, (item + 1) in arr) for item in arr}
    middle_numbers = dict(filter(lambda i: i[1][0] and i[1][1], table.items()))
    edge_numbers = dict(filter(lambda i: (i[1][0] or i[1][1]) and not (i[1][0] and i[1][1]), table.items()))

    if len(middle_numbers) > 0:
        highest_seq = 3

        while len(edge_numbers) > 0:
            edge_numbers.pop(edge := next(iter(edge_numbers.keys())))
            seq = 1

            if (higher := edge + 1) in middle_numbers:
                seq += 1
                while higher in middle_numbers:
                    higher += 1
                    seq += 1
            elif (lower := edge - 1) in middle_numbers:
                seq += 1
                while lower in middle_numbers:
                    lower -= 1
                    seq += 1

            highest_seq = max(seq, highest_seq)

        return highest_seq
    else:
        return 2 if len(edge_numbers) > 0 else 1


def longestConsecutive(arr: list[int]) -> int:
    arr_set = set(arr)
    highest_seq = 0

    for number in arr:
        if number - 1 not in arr_set:
            seq = 1
            latter = number + 1
            while latter in arr_set:
                arr_set.remove(latter)
                seq += 1
                latter += 1

            highest_seq = max(seq, highest_seq)

    return highest_seq
