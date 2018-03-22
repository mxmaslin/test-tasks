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

wrong_num = 'Аргументом должно быть целое число больше нуля'

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
    header = ['Фамилия', 'Имя', 'Отчество', 'Номер диплома']
    wr = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    wr.writerow(header)

    num_digits = len(str(num_persons))

    for i in range(1, num_persons + 1):
        person = fake.name().split()[-3:]
        num_digits_i = len(str(i))
        padding = '0' * (num_digits - num_digits_i)
        diploma = str(i) if num_digits == i else padding + str(i)
        person.append(diploma)
        wr.writerow([unicode(x).encode('utf-8') for x in person])




