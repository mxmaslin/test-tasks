from flask import request, jsonify

from app import app


@app.route('/')
def hello():
    user_agent = request.headers.get('User-Agent')
    return 'Helloa!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)