# Задание

Есть js-библиотека [fingerprint2](https://github.com/Valve/fingerprintjs2).
Надо захватывать фингерпринт и делать запрос к своей мини-базе. База данных с одной таблицей. В таблице есть нескольких контактов в любом удобном формате которая будет содержать: фингерпринт, имя, телефон, e-mail.

При заходе на страницу где установлен скрипт - получать фингерпринт, делать запрос к апи для проверки существования фингерпринта.

Если такой есть - выводить приветствие с именем, если такого нет - выводить "Привет, гость!" при этом в базу записывать фингерпринт.

Стэк для реализации:
1. HTML + JS
2. Python (для реализации API допускается использовать Flask), SQLAlchemy

## Инструкции по развертыванию

1. `npm install`
2. `npm run build`
3. `python app.py`
4. Откройте `index.html` в браузере. Отобразится надпись "Привет, незнакомец".
5. Перезагрузите страницу. Отобразится надпись "Привет, {ip-адрес}".
6. Дополнительно: удалите из БД все записи. Скопируйте fingerprint (выводится в консоли). Присвойте его переменной `my_fingerprint` в файле `populate_db.py`. Запустите `populate_db.py`. Откройте `index.html` в браузере. Отобразится надпись "Привет, {имя фамилия}".  
  
