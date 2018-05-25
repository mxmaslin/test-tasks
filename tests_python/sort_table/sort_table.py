import string

from flask import (Flask,
                   abort,
                   jsonify,
                   request)


MY_ALPHABET = string.digits + ''.join([chr(i) for i in range(32, 127) if chr(i) not in string.digits])


def my_sort(s):
    return [MY_ALPHABET.index(c) for c in s]


app = Flask(__name__)


@app.route('/sort-table', methods=['POST'])
def sort_table():
    if not request.json or 'table' not in request.json:
        abort(400)
    table_sorted = {'table': []}
    for row in request.json['table']:
        columns = row.split('\t')
        table_sorted['table'].append('\t'.join(sorted(columns, key=my_sort)))
    return jsonify(table_sorted), 201


if __name__ == '__main__':
    app.run(debug=True)
