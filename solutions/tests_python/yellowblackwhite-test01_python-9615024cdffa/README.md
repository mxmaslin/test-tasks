Напишите запрос возвращающий данные из mongo используя aggregation framework и mongoengine.
Ответ запроса должен соответствовать следующему формату:

```
#!json

           [
              {
                "path": "/series/<alias сериала>",
                "title": "<title сериала>",
                "description": "<description сериала>",
                "cover": "<изображение из поля images с ключем ImagesEnum.cover>",
                "quote": "<значение quote.text>",
                "quote_source": "<значение quote.source>",
                "slide": {
                  "background": "<изображение из поля images с ключем ImagesEnum.background>",
                  "foreground": "<изображение из поля images с ключем ImagesEnum.foreground>"
                }
                "seasons": [
                  {
                    "path": "/series/<alias сериала>/<alias сезона>",
                    "title": "<num сезона> сезон",
                    "episodes": [
                      {
                        "path": "/series/<alias сериала>/<alias сезона>/<alias эпизода>",
                        "title": "Эпизод <num сезона>",
                        "files": [
                          {
                            "path": "<path файла>",
                            "label": "<название enum поля QualityEnum>",
                            "quality": "<значения enum поля QualityEnum>"
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
```

Все модели данных есть в файле task.py.
Запуск теста автоматически создаст необходимые записи в базе.
Для запуска проекта используйте docker-compose, в папке проекта выполните команду docker-compose up.

Решение содержится в файле [task.py](https://github.com/mxmaslin/Test-tasks/blob/master/solutions/tests_python/yellowblackwhite-test01_python-9615024cdffa/task.py)
