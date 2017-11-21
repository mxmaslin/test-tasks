# Начало работы

Выполните в папке проекта в консоли команды:

```
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
```

В результате создадутся

- группы с требуемыми правами
- админ
- пользователи для каждой из групп
- экземпляры Предложения, Анкеты клиента, Заявки в кредитную организацию.

Всё это будет доступно через админку http://{ip}:{port}/admin/, логин: admin, пароль: qwer1234.

# Как делать запросы к API

Для запросов к API проще всего использовать httpie

# PartnerAPI

## Получение списка всех анкет

    http --auth {superuser, partner, bank}:qwer1234 GET http://127.0.0.1:8000/loans/partner_api/questionnaires/

## Получение определённой анкеты

    http --auth {superuser, partner, bank}:qwer1234 GET http://127.0.0.1:8000/loans/partner_api/questionnaires/{id}/

## Поиск среди анкет по одному из критериев (name, phone, passport)

    http --auth {superuser, partner, bank}:qwer1234 GET http://127.0.0.1:8000/loans/partner_api/questionnaires/?search={name,phone,passport}

## Получение отсортированного списка анкет по одному из критериев (created, modified, birthday, score)

    http --auth {superuser, partner, bank}:qwer1234 GET http://127.0.0.1:8000/loans/partner_api/questionnaires/?ordering={created,modified,birthday,score} 

## Создание анкеты

    http --auth {superuser, partner, bank}:qwer1234 POST http://127.0.0.1:8000/loans/partner_api/questionnaires/ <<< '{"name": "Давид Соломонович", "birthday": "1957-06-21", "passport": "abc123", "phone": "130-19-32", "score": 5}'

## Изменение анкеты

    http --auth superuser:qwer1234 PUT http://127.0.0.1:8000/loans/partner_api/questionnaires/ <<< '{"name": "Исаак Моисеевич", "birthday": "1977-05-30", "passport": "cba981", "phone": "425-58-12", "score": 11}'

## Удаление анкеты

    http --auth superuser:qwer1234 DELETE http://127.0.0.1:8000/loans/partner_api/questionnaires/{id}/

## Отправка заявки в кредитную организацию

    http --auth {superuser, partner, bank}:qwer1234 POST http://127.0.0.1:8000/loans/partner_api/make_submission/ <<< '{"application": 1, "questionnaire": 1, "status": 1, "created": "2017-11-10T18:23:16.913526Z", "submitted": "2017-11-10T18:23:16.913526Z"}'

# BankAPI

## Получение списка всех заявок

    http --auth bank:qwer1234 GET http://127.0.0.1:8000/loans/bank_api/submissions/

## Получение отфильтрованного списка заявок по критерию status:
    
    http --auth bank:qwer1234 GET http://127.0.0.1:8000/loans/bank_api/submissions/?status={0,1,2}

## Поиск среди заявок по одному из критериев (application, questionnaire):
    
    http --auth bank:qwer1234 GET http://127.0.0.1:8000/loans/bank_api/submissions/?search={application data,questionnaire data}

## Получение отсортированного списка анкет по одному из критериев (created, submitted):

    http --auth bank:qwer1234 GET http://127.0.0.1:8000/loans/bank_api/submissions/?ordering={created, submitted}

## Получение определённой заявки

    http --auth bank:qwer1234 GET http://127.0.0.1:8000/loans/bank_api/submissions/{id}/

## Создание заявки

    http --auth {superuser, partner, bank}:qwer1234 POST http://127.0.0.1:8000/loans/bank_api/submissions/ <<< '{"application": 1, "questionnaire": 1, "status": 2}'

## Изменение заявки

    http --auth superuser:qwer1234 PUT http://127.0.0.1:8000/loans/bank_api/submissions/ <<< '{"application": 1, "questionnaire": 1, "status": 1}'

## Удаление заявки

    http --auth superuser:qwer1234 DELETE http://127.0.0.1:8000/loans/bank_api/submissions/{id}/