# -*- coding: utf-8 -*-
import csv
import sys

from faker import Faker

args = sys.argv

try:
    num_persons = args[1]
except IndexError:
    print('Требуется целочисленный аргумент при запуске скрипта')
    exit()

wrong_num = 'Аргументом должно быть положительное целое число'

try:
    num_persons = int(num_persons)
except ValueError:
    print(wrong_num)
    exit()

if num_persons < 1:
    print(wrong_num)
    exit()

fake = Faker('ru_RU')

with open('persons.csv', 'w') as f:
    header = ['family', 'name', 'patronymic', 'diploma_id']
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    wr.writerow(header)

    for _ in range(num_persons):
        person = fake.name().split()[-3:]
        wr.writerow([unicode(x).encode('utf-8') for x in person])
