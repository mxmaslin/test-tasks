# -*- coding: utf-8 -*-
import os
from operator import itemgetter


def closest(p, c, n):
    # выбираем из p и n, кто ближе к c
    try:
        ptup = p, teams[c] - teams[p]
    except KeyError:
        ptup = c, teams[c]

    try:
        ntup = n, teams[n] - teams[c]
    except KeyError:
        ntup = c, teams[c]

    return min([ptup, ntup], key=itemgetter(1))[0]


for root, dirs, files in os.walk(os.path.join('Wargaming Forge Task', 'task_1_data')):
    if not files:
        continue

    users = dict()

    # получаем словарь с парами user_id:user_rating
    with open(os.path.join(root, files[0])) as f_players:
        for line in f_players:
            print(line)
            user_id, user_rating = line.split()
            users[user_id] = user_rating

    teams = dict()

    # получаем словарь с парами team_id:team_rating
    with open(os.path.join(root, files[1])) as f_teams:
        for line in f_teams:
            print(line)
            team_id, *user_ids = line.split()
            teams[team_id] = sum(map(lambda x: int(users[x]), user_ids))

    # ищем подходящую пару
    teams_sorted = sorted(teams, key=teams.__getitem__)

    for p, c, n in zip([None]+teams_sorted[:-1],
                       teams_sorted,
                       teams_sorted[1:]+[None]):
        t2 = closest(p, c, n)

        test_name = root.split('/')[-1]

        print(c, t2)

        with open(os.path.join('Username_task_1_team_pairs',
                               '{}_pairs.txt'.format(test_name)), 'a') as f_result:
            if c != t2:
                f_result.write('{} {}\n'.format(c, t2))
            else:
                f_result.write(c)
