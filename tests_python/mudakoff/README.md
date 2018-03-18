Написать веб-приложение, которое будет отслеживать публикации в группе МДК (https://vk.com/mudakoff) и строить графики изменения количества лайков, комментариев и репостов в реальном времени.

**Решение** содержится в файле [plot.py](https://github.com/mxmaslin/Test-tasks/blob/master/tests_python/mudakoff/plot.py)

Для работы скрипта необходимы
- библиотека [vk-api](https://github.com/python273/vk_api)
- библиотека [bokeh](https://bokeh.pydata.org/en/latest/)

Запуск скрипта:

    bokeh serve
    python plot.py
    
Для просмотра данных откройте файл plot.html (создастся после запуска скрипта).
