import csv
import logging

from datetime import datetime
from urllib.request import urlretrieve

from progress.bar import Bar
from sqlalchemy.orm import Session, sessionmaker

from engine import engine
from models import Agency, City, Crime, State


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

data_url = 'https://gist.github.com/tm-minty/c39f9ab2de1c70ca9d4d559505678234/raw/8ecaee79b2c2cce88d60815aadeebb5ac209603a/police-department-calls-for-service.csv.zip'
filename = 'police-department-calls-for-service.csv'

logging.basicConfig(
    filename='log.txt', level=logging.INFO,
    format='%(asctime)s %(message)s', filemode='w'
)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    return instance


def get_records_amount():
    with open(filename) as f:
        return sum(1 for line in f)


def fill_db():
    file = urlretrieve(data_url, 'data.zip')
    print(file)
    # with open(filename, 'r') as f:
    #     upload_started = datetime.now()
    #     logging.info(f'Upload started at {upload_started}')
    #     reader = csv.reader(f, delimiter=',')
    #     next(reader)
    #     total_records = get_records_amount()
    #     bar = Bar('Uploading', max=total_records)
    #     crimes = []
        
    #     with Session() as session:
    #         for i, row in enumerate(reader):
    #             row = ['NULL' if val == '' else val for val in row]
    #             (
    #                 crime_id, crime_type, report_date, _, offence_date, _,
    #                 call_dt, disposition, address, city, state, agency_id,
    #                 address_type, common_location
    #             ) = row

    #             city = get_or_create(session, City, name=city)
    #             state = get_or_create(session, State, name=state)
    #             agency = get_or_create(
    #                 session, Agency, agency_id=agency_id,
    #                 address_type=address_type, location=common_location
    #             )
    #             crime = Crime(
    #                 crime_id=crime_id, crime_type=crime_type,
                    
    #                 report_date=datetime.strptime(report_date, '%Y-%m-%dT%H:%M:%S'),
    #                 offence_date=datetime.strptime(offence_date, '%Y-%m-%dT%H:%M:%S'),
    #                 call_dt=datetime.strptime(call_dt, '%Y-%m-%dT%H:%M:%S'),
                    
    #                 disposition=disposition, address=address,
    #                 city_id=city.id,
    #                 state_id=state.id, agency_id=agency.id
    #             )
    #             crimes.append(crime)
            
    #             if i % 10000 == 0:
    #                 session.bulk_save_objects(crimes)
    #                 session.commit()
    #                 crimes = []
                
    #             bar.next()
        
    #         session.commit()
    #         logging.info(f'Upload finished at {datetime.now()}')
    #         logging.info(f'{total_records} added to db')
    #         logging.info(f'Time elapsed: {(datetime.now() - upload_started).total_seconds()} seconds')
    #         bar.finish()


if __name__ == '__main__':
    fill_db()
