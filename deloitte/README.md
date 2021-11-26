# Task 1

Implement some action for the user after timeout.

Features: sending messages to specific user via websockets. 

[Solution](expire/app.py)

# Task 2

Implement asynchronous email sending with progress display.

Start celery: `celery -A app.c worker -PE eventlet -c 1000`

[Solution](display_progress/app.py)