import csv
import json
import random
from functools import lru_cache
from multiprocessing import Value
from typing import List
from flask import Flask, request, Response


app = Flask(__name__)


def config_to_list(filepath: str) -> List:
    entries = []
    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='\n')
        for entry in csvreader:
            entries.append(entry)
    return entries


@lru_cache
def get_list_config(filename):
    return config_to_list(filename)


@app.route('/', methods=['GET'])
def get_image():
    config = get_list_config('config.csv')
    categories = request.args.getlist('category')
    if not categories:
        random_entry = random.choice(config)
        _, _, *categories = random_entry

    category = random.choice(categories)
    for entry in config:
        image_url, display_counter, *entry_categories = entry
        display_counter = Value('i', int(display_counter))
        if category in entry_categories and display_counter.value > 0:
            with display_counter.get_lock():
                display_counter.value -= 1
            entry[1] = display_counter
            random.shuffle(config)
            resp = {
                'success': True, 'image': f'<img src="{image_url}">'
            }
            return Response(
                json.dumps(resp), status=200, mimetype='application/json'
            )

    resp = {'success': False, 'image': None}
    return Response(json.dumps(resp), status=400, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
