import os
import time

import eventlet
eventlet.monkey_patch()

from celery import Celery
from flask import Flask, session, request
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)

CELERY_BROCKER_URL = 'redis://localhost:6379'

app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')


CELERY_BROKER_URL = 'redis://localhost:6379/0'

app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['result_backend'] = CELERY_BROKER_URL

mail = Mail(app)

c = Celery(app.name, broker=CELERY_BROKER_URL)
c.conf.update(app.config)


@c.task
def send_email(address):
    msg = Message('subject',
                  sender=app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[address])
    msg.body = 'body'
    with app.app_context():
        mail.send(msg)


@socketio.on('send')
def on_send():
    addresses = session['addresses']
    for i, address in enumerate(addresses):
        send_email.delay(address)
        emit('progress', [i, len(addresses)])
        time.sleep(1)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['addresses']
        if uploaded_file.filename != '':
            addresses = [x for x in (uploaded_file.read()).decode().split('\n') if x]
            session['addresses'] = addresses
    return """        
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="addresses" id="addresses">
            <input type="submit" value="submit">
        </form>
        
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.structure.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.theme.min.css">
        
        <script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js'></script>
        <script>        
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            socket.emit('send');
            socket.on('progress', function(info){
                var current, total;
                [current, total] = info;
                current = (current + 1) * (100 / total);                
                console.log(current);
                
                $(function(){
                    $('#progressbar').progressbar({
                        value: current
                    })
                })

            })
        </script>
        <div id="progressbar"></div>
    """


if __name__ == "__main__":
    eventlet_socket = eventlet.listen(('127.0.0.1', 5000))
    eventlet.wsgi.server(eventlet_socket, app)
