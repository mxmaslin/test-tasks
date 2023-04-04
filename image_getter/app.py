import csv
from typing import List
from flask import Flask, request


app = Flask(__name__)


def config_to_list(filepath: str) -> List:
    entries = []
    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='\n')
        for entry in csvreader:
            entries.append(entry)
    return entries

config = config_to_list('config.csv')


@app.route('/', methods=['GET'])
def get_image():
    categories = request.args.getlist('category')
    print(config)
    return '200'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
