Необходимо:
1. Написать скрипт на Python который загружает в БД (sqlite3) данные по каждому твиту из файла [three_minutes_tweets.json.txt](https://raw.githubusercontent.com/mxmaslin/Test-tasks/master/tests_python/tweets_sentiment/three_minutes_tweets.json.txt) в таблицу tweet (name, tweet_text, country_code, display_url, lang, created_at, location)
2. Добавить новую колонку tweet_sentiment
3. Подумать как можно провести нормализацию данной таблицы, создать и применить SQL скрипт
для нормализации
4.  Написать скрипт на Python для подсчета среднего sentiment (Эмоциональной окраски сообщения) на основе [AFINN-111.txt](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/tweets_sentiment/AFINN-111.txt) и обновить tweet_sentiment колонку, если слова нет в файле предполагать что sentiment = 0
AFINN ReadMe:
AFINN is a list of English words rated for valence with an integer between minus five (negative) and plus five (positive). The words have been manually labeled by Finn Årup Nielsen in 2009-2011. The file is tab-separated.
5. Написать 1 SQL скрипт, который выводит наиболее и наименее счастливую страну, локацию и пользователя

[**Решение**](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/tweets_sentiment/calculate.py "Определение эмоциональной окраски твитов")

Для работы скрипта необходимы
- библиотека [peewee](http://docs.peewee-orm.com/en/latest/)
- файл [models.py](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/tweets_sentiment/models.py)
- файл [three_minutes_tweets.json.txt](https://raw.githubusercontent.com/mxmaslin/Test-tasks/master/tests_python/tweets_sentiment/three_minutes_tweets.json.txt)
- файл [AFINN-111.txt](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/tweets_sentiment/AFINN-111.txt)
