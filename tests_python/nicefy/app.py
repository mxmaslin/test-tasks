import json

from itertools import zip_longest
from datetime import datetime
from pathlib import Path

from dictdiffer import diff
from flask import Flask, render_template, request

app = Flask(__name__)

DATA_FOLDER = './data/data'

NOT_SPECIFIED = 'Not specified'


def get_filenames():
    path = Path(DATA_FOLDER)
    file_names = [x.name for x in path.iterdir() if x.is_file()]
    return file_names


def get_data_from_file(filename):
    path_to_data = Path(DATA_FOLDER)
    for path in path_to_data.iterdir():
        if path.is_file() and path.name == filename:
            with path.open() as json_file:
                data = json.load(json_file)
                return data
    return {}


def get_diff(current_action, prev_action):
    current_action_issues = {x['id']: x for x in current_action}
    prev_action_issues = {x['id']: x for x in prev_action}
    difference = list(diff(current_action_issues, prev_action_issues))
    return difference


def compose_user_diff_message(user_diff):
    message = None
    if user_diff:
        message = f'User name {user_diff[0][0]}'
    return message


def compose_order_items_diff_message(order_items_diff):
    # can't implement because there's no difference in order items
    message = None
    if order_items_diff:
        print('Found order items diff')
    return message


def compose_fulfillments_diff_message(fulfillments_diff):
    message = None
    if fulfillments_diff:
        message = f'{fulfillments_diff[0][0]} {fulfillments_diff[1][1][1]} to {fulfillments_diff[0][2][0]}'
    return message


def compose_issues_diff_message(issues_diff):
    message = None
    if issues_diff:
        import ast
        try:
            issue = ast.literal_eval(issues_diff[0][2][0][1]["message"])['service_id'][0]
        except SyntaxError:
            issue = issues_diff[0][2][0][1]["message"]
        message = f'{issues_diff[0][0]} issue "{issue}"'
    return message


def compose_diff(current_action, prev_action):
    user_diff = list(diff(current_action['user'], prev_action['user']))
    user_diff = compose_user_diff_message(user_diff)

    order_items_diff = get_diff(
        current_action['model_data']['order_items'],
        prev_action['model_data']['order_items']
    )
    order_items_diff = compose_order_items_diff_message(order_items_diff)

    fulfillments_diff = get_diff(
        current_action['model_data']['fulfillments'],
        prev_action['model_data']['fulfillments']
    )
    fulfillments_diff = compose_fulfillments_diff_message(fulfillments_diff)

    issues_diff = get_diff(
        current_action['model_data']['order_issues'],
        prev_action['model_data']['order_issues']
    )
    issues_diff = compose_issues_diff_message(issues_diff)

    diffs = user_diff, order_items_diff, fulfillments_diff, issues_diff
    diffs = [diff for diff in diffs if diff]
    return diffs


def nicefy(current_action, prev_action):
    nicefied = {}
    nicefied['action'] = current_action.get('model_data', {}).get('status_display', NOT_SPECIFIED)

    action_dt = current_action.get('event_time')
    action_dt = datetime.strptime(action_dt, '%Y-%m-%dT%H:%M:%S.%fZ')
    nicefied['date'] = action_dt.date().strftime('%d-%m-%Y')
    nicefied['time'] = action_dt.time().strftime('%H:%M')

    user = current_action.get('user')
    username = 'System'
    if isinstance(user, dict):
        username = user.get('username') or NOT_SPECIFIED
    nicefied['username'] = username

    current_action_is_update = current_action.get('event_type') == 'updated'
    nicefied['diff_with_prev'] = []
    if current_action_is_update and prev_action:
        nicefied['diff_with_prev'] = compose_diff(current_action, prev_action)
    return nicefied


@app.route('/')
def represent():
    filename = request.args.get('filename', default='sample1.json')
    data_from_file = get_data_from_file(filename).get('results', [])
    data_from_file = [
        nicefy(current, prev)
        for current, prev in zip_longest(data_from_file, data_from_file[1:])
    ]
    filenames = sorted(get_filenames())
    context = {'filenames': filenames, 'nicefied': data_from_file}
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run()

