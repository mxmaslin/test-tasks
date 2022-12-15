from datetime import datetime

from flask import request, jsonify
from sqlalchemy import and_

from app import app, db
from models import Crime

ROWS_PER_PAGE = 20


@app.route('/crimes')
def crimes():
    page = int(request.args.get('page', default=1))

    date_from = request.args.get('date_from', default=datetime.min)
    date_to = request.args.get('date_to', default=datetime.max)
    
    crimes = db.session.query(Crime).filter(
        Crime.report_date.between(date_from, date_to)
    ).paginate(page=page, per_page=ROWS_PER_PAGE).items

    return jsonify([x.as_dict() for x in crimes])


if __name__ == '__main__':
    app.run(debug=True)
