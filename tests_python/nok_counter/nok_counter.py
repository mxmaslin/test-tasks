# -*- coding: utf-8 -*-
from collections import Counter


def same(l):
    return all(x == l[0] for x in l)


def lookahead(iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, True
        last = val
    yield last, False


def count_noks(file):
    nok_times = []
    c = Counter()
    with open(file) as f:
        for line, has_more in lookahead(f):
            if len(line) < 2:
                continue
            time, event = line.rsplit(None, 1)
            time = time[1:-4]
            if event == 'NOK':
                c.update({time})
                nok_times.append(time)
                if not same(nok_times):
                    print(nok_times[0], c[nok_times[0]])
                    nok_times = [time]
            if not has_more:
                print(nok_times[0], c[nok_times[0]])
    return c


if __name__ == '__main__':
    assert count_noks('logs/events1.log') == Counter({'2018-04-11 03:13': 1})
    assert count_noks('logs/events2.log') == Counter({'2018-04-11 03:15': 1})
    assert count_noks('logs/events3.log') == Counter({'2018-04-11 03:13': 1, '2018-04-11 03:15': 1})
    assert count_noks('logs/events4.log') == Counter({'2018-04-11 03:13': 2, '2018-04-11 03:15': 1})
    assert count_noks('logs/events5.log') == Counter(
        {'2018-04-11 03:13': 1, '2018-04-11 03:14': 1, '2018-04-11 03:16': 1})
    assert count_noks('logs/events6.log') == Counter(
        {'2018-04-11 03:13': 2, '2018-04-11 03:14': 1, '2018-04-11 03:16': 1})
    assert count_noks('logs/events7.log') == Counter(
        {'2018-04-11 03:13': 1, '2018-04-11 03:14': 2, '2018-04-11 03:16': 1})
    assert count_noks('logs/events9.log') == Counter({'2018-04-11 03:16': 1})
    assert count_noks('logs/events10.log') == Counter(
        {'2018-04-11 03:13': 1, '2018-04-11 03:14': 2, '2018-04-11 03:16': 2})
    assert count_noks('logs/events11.log') == Counter(
        {'2018-04-11 03:13': 2, '2018-04-11 03:14': 1, '2018-04-11 03:16': 2})
