# -*- coding: utf-8 -*-
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta


def is_passport_valid(birthday, issued):
    '''
        Задание:
        Нужно написать функцию на Python проверки актуальности паспорта.
        Паспорт выдается в 14 лет и должен быть заменен в 20 и 45 лет, на замену паспорта дается 1 месяц.
        Функция должна принимать две даты - дата рождения и дату выдачи паспорта, возвращать должна True если паспорт действителен, False - есть нет.

        Мой комментарий:
	Для работы скрипта нужен python 2
	Перед началом использования надо сделать sudo pip install python-dateutil (проблема в том, что datetime.timedelta не принимает годы)
        Даты принимаются в формате YYYY-MM-DD
        Исходим из того, что в течение выделенного на замену месяца паспорт является недействительным
    '''
    try:
        date_birthday = dt.strptime(birthday, '%Y-%m-%d')
    except ValueError as e:
        print e
        return

    try:
        date_issued_current_passport = dt.strptime(issued, '%Y-%m-%d')
    except ValueError as e:
        print e
        return

    date_passport_first_issue = date_birthday + relativedelta(years=14)
    date_passport_first_due = date_birthday + relativedelta(years=20)

    date_passport_second_issue = date_passport_first_due + relativedelta(
        months=1)
    date_passport_second_due = date_birthday + relativedelta(years=45)

    date_passport_third_issue = date_passport_second_due + relativedelta(
        months=1)

    return any([
        date_passport_first_issue <= date_issued_current_passport < date_passport_first_due,
        date_passport_second_issue <= date_issued_current_passport < date_passport_second_due,
        date_passport_third_issue <= date_issued_current_passport])


if __name__ == '__main__':
    assert is_passport_valid('1977-05-30', '1991-05-30') == True, 'Чувак получил паспорт ровно в 14 лет'
    assert is_passport_valid('1977-05-30', '1991-05-29') == False, 'Чуваку ещё не исполнилось 14 лет'
    assert is_passport_valid('1977-05-30', '1997-05-29') == True, 'Чуваку вот-вот стукнет 20 лет, пора завтра менять паспорт'
    assert is_passport_valid('1977-05-30', '1997-05-30') == False, 'Чуваку исполнилось 20 лет, пора менять паспорт'
    assert is_passport_valid('1977-05-30', '1997-05-31') == False, 'Чуваку исполнилось 20 лет, но месяц на замену паспорта не прошёл'
    assert is_passport_valid('1977-05-30', '1997-06-30') == True, 'Чуваку исполнилось 20 лет, прошёл месяц на замену паспорта'
    assert is_passport_valid('1977-05-30', '2022-05-29') == True, 'Чуваку вот-вот исполнится 45 лет. Как годы-то летят'
    assert is_passport_valid('1977-05-30', '2022-05-30') == False, 'Чуваку исполнилось 45 лет'
    assert is_passport_valid('1977-05-30', '2022-06-30') == True, 'Чуваку исполнилось 45 лет, месяц на замену паспорта прошёл'
