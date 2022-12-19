Имеется файл events.log вида:

    [2018-04-11 03:13:57] ОК

    [2018-04-11 03:14:04] OK

    [2018-04-11 03:14:05] NOK
   
    [2018-04-11 03:14:06] NOK
    
    [2018-04-11 03:14:08] NOK

    [2018-04-11 03:14:09] OK

    ...

Напишите на вашем любимом скриптовом языке программирования (Ruby/Perl/PHP/Python/Groovy/..) программу, которая считывает файл и выводит число событий NOK за каждую минуту.

Особенность моей реализации заключается в следующем:
- файл читается построчно
- число NOK за каждую минуту принтится сразу (в минуту `n` было `m` NOK-событий), не дожидаясь, когда чтение файла будет завершено

[**Решение**](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/nok_counter/nok_counter.py "Realtime cчётчик событий определённого типа за интервал времени")