import eventlet

import redis

from datetime import timedelta
from flask import Flask, session, request
from flask_socketio import SocketIO, emit

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)

r = redis.Redis.from_url('redis://localhost:6379')


@socketio.on('expiration check')
def on_expiration_check():
    user = session.get('user')
    if not user:
        return
    if not r.get(user):
        emit('expired', f'{user} session expired')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form.get('user')
        session['user'] = user
        r.setex(user, timedelta(seconds=5), value=user)

    return """        
        <form method="post">
            <input type="text" name="user" id="user">
            <input type="submit" value="login">
        </form>

        <script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.3/socket.io.min.js'></script>
        <script>
            var socket = io.connect('http://' + document.domain + ':' + location.port);
            $(document).ready(function(){
                $('form').submit(function(e){
                    e.preventDefault();
                    $.post('/', {
                        user: $('#user').val()
                        
                    })
                });                
                socket.emit('expiration check');
                socket.on('expired', function(msg){
                    console.log(msg)
                })
            })

        </script>
    """


if __name__ == "__main__":
    eventlet_socket = eventlet.listen(('127.0.0.1', 5000))
    eventlet.wsgi.server(eventlet_socket, app)
