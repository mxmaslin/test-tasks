from itertools import chain


src_a1 = ({k: v} for k, v in zip(['a', 'b', 'c'], [0, 1, 2]))
src_b1 = ({k: v} for k, v in zip(['d', 'c'], [1, 2]))
src_c1 = ({k: v} for k, v in zip(['c'], [2]))

src_a2 = ({k: v} for k, v in zip(['a', 'b', 'c'], [2, 1, 0]))
src_b2 = ({k: v} for k, v in zip(['a', 'c'], [2, 1]))
src_c2 = ({k: v} for k, v in zip(['c'], [2]))


def gen_sum(src_a, src_b, src_c):
    result = dict()
    for d in chain(src_a, src_b, src_c):
        k, v = zip(*d.items())
        k, v = k[0], v[0]
        cur_val = result.get(k, 0)
        result[k] = cur_val + v
    return result


if __name__ == '__main__':
    assert gen_sum(src_a1, src_b1, src_c1) == {'a': 0, 'b': 1, 'c': 6, 'd': 1}
    assert gen_sum(src_a2, src_b2, src_c2) == {'a': 4, 'b': 1, 'c': 3}
