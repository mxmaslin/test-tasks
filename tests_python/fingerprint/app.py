from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fingerprint = db.Column(db.String(32), index=True)
    first_name = db.Column(db.String(64), nullable=True)
    second_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    def is_known(self):
        return self.first_name or self.second_name

    def __repr__(self):
        first_name = '?'
        second_name = '?'
        if self.first_name:
            first_name = self.first_name
        if self.second_name:
            second_name = self.second_name
        return f'{first_name} {second_name}'


@app.route('/fingerprint/<string:fingerprint>', methods=['GET'])
def get_task(fingerprint):
    user = User.query.filter_by(fingerprint=fingerprint).first()
    output = {'lives_in_db': False, 'is_known': False, 'name': None}
    if user:
        output['lives_in_db'] = True
        if user.is_known():
            output['is_known'] = True
            output['name'] = str(user)
    else:
        user = User(fingerprint=fingerprint)
        db.session.add(user)
        db.session.commit()
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
