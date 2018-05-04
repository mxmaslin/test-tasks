# -*- coding: utf-8 -*-

def same(l):
    return all(x == l[0] for x in l)


def count_noks(file):
    '''
    Этот код работает правильно, но пованивает, я скоро перепишу его
    '''
    nok_counter = 0
    nok_times = []
    nok_test = []
    with open(file) as f:
        for line in f:
            if len(line) < 2:
                continue
            time, event = line.rsplit(None, 1)
            time = time[1:-4]
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
    print(count_noks('logs/events.log'))
    # assert count_noks('logs/events.log') == [('2018-04-11 03:13', 1), ('2018-04-11 03:14', 4), ('2018-04-11 03:15', 1)]

