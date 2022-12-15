def max_ones(int_list):
    str_list = ''.join(map(str, int_list)).split('0')
    if len(int_list) < 3 or len(str_list) == 1:
        return sum(int_list)
    calculated_max_ones = 0
    for i in range(0, len(str_list) - 1):
        first, second = str_list[i], str_list[i + 1]
        first = len(first) if first else 0
        second = len(second) if second else 0
        pair_sum = first + second
        if pair_sum > calculated_max_ones:
            calculated_max_ones = pair_sum
    return calculated_max_ones


if __name__ == '__main__':
    assert max_ones([0, 0]) == 0
    assert max_ones([1, 0]) == 1
    assert max_ones([1, 1]) == 2
    assert max_ones([1, 0, 1, 0]) == 2
    assert max_ones([0, 1, 0, 1]) == 2
    assert max_ones([1, 1, 1, 1, 1]) == 5
    assert max_ones([0, 0, 0, 0, 0]) == 0
    assert max_ones([1, 0, 0, 1, 0]) == 1
    assert max_ones([0, 1, 1, 0, 1]) == 3
    assert max_ones([1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]) == 6
    assert max_ones([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0]) == 1
    assert max_ones([1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1]) == 5
    assert max_ones([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0]) == 2
