**Задание**

Приведено здесь: https://gist.github.com/tm-minty/c39f9ab2de1c70ca9d4d559505678234

Данные в csv: police-department-calls-for-service.csv

**Проверка**

1. `pip install -r requirements.txt`
2. `python upload_to_db.py`
3. Налейте боольшую кружку вашего любимого горячего напитка.
4. `export FLASK_APP=api.py`
5. `python api.py`
6. Откройте в браузере URL http://127.0.0.1:5000/crimes?page=1&date_from=2008-11-05&date_to=2022-11-05