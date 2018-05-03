# -*- coding: utf-8 -*-


def same(l):
    return all(x == l[0] for x in l)


def count_noks(file):
    nok_counter = 0
    nok_times = []
    nok_test = []
    with open(file) as f:
        for line in f:
            if len(line) > 1:
                splitted = line.split()
                time = '{} {}'.format(splitted[0][1:], splitted[1][:-1])[:-3]
                event = splitted[-1]
                if event == 'NOK':
                    nok_times.append(time)
                    if same(nok_times):
                        nok_counter += 1
                    else:
                        print(nok_times[0], nok_counter)
                        nok_test.append((nok_times[0], nok_counter))
                        nok_counter = 1
                        nok_times = [time]
    if len(nok_times) >= 1:
        print(time, nok_counter)
        nok_test.append((time, nok_counter))
    return nok_test


if __name__ == '__main__':
    print(count_noks('events.log'))
