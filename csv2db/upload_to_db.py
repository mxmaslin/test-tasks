import csv
import logging
import os
import requests
import shutil

from datetime import datetime

from progress.bar import Bar
from sqlalchemy.orm import Session, sessionmaker

from engine import engine
from logger import setup_console_logger, setup_file_logger
from models import Agency, City, Crime, State, get_or_create


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
from app import db
db.metadata.create_all(engine)

data_url = 'https://gist.github.com/tm-minty/c39f9ab2de1c70ca9d4d559505678234/raw/8ecaee79b2c2cce88d60815aadeebb5ac209603a/police-department-calls-for-service.csv.zip'


file_logger = setup_file_logger(
    'file_logger',
    logging.Formatter('%(asctime)s %(levelname)s %(message)s'),
    'upload.log'
)
console_logger = setup_console_logger(
    'console_logger',
    logging.Formatter('%(message)s')
)


class Downloader:
    def __init__(self, url, logger):
        self.url = url
        self.filename = url.split('/')[-1]
        self.logger = logger

    @property
    def url_response(self):
        return requests.get(self.url, stream=True)

    def count_chunks(self):
        chunks_count = 0
        for chunk in self.url_response.iter_content(chunk_size=1024):
            if chunk:
                chunks_count += 1
                self.logger.info(f'Chunks: {chunks_count}')
        return chunks_count

    def download(self):
        chunks_count = self.count_chunks()
        bar = Bar('Downloading zipped csv', max=chunks_count)
        with open(self.filename, 'wb') as f:
            for chunk in self.url_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.next()
            bar.finish()
            return f


def csv_records_count(filename):
    with open(filename) as f:
        return sum(1 for line in f)


def fill_db(data_url):
    downloader = Downloader(data_url, console_logger)
    downloader.download()
    shutil.unpack_archive(downloader.filename)
    csv_file_name = downloader.filename.rstrip('.zip')
    
    with open(csv_file_name, 'r') as f:
        filling_db_started = datetime.now()
        file_logger.info(f'CSV to DB started at {filling_db_started}')
        reader = csv.reader(f, delimiter=',')
        next(reader)
        total_records = csv_records_count(csv_file_name)
        bar = Bar('Writing data to DB', max=total_records)
        crimes = []
        
        with Session() as session:
            for i, row in enumerate(reader):
                row = ['NULL' if val == '' else val for val in row]
                (
                    crime_id, crime_type, report_date, _, offence_date, _,
                    call_dt, disposition, address, city, state, agency_id,
                    address_type, common_location
                ) = row

                city = get_or_create(session, City, name=city)
                state = get_or_create(session, State, name=state)
                agency = get_or_create(
                    session, Agency, agency_id=agency_id,
                    address_type=address_type, location=common_location
                )
                crime = Crime(
                    crime_id=crime_id,
                    crime_type=crime_type,
                    report_date=datetime.strptime(report_date, '%Y-%m-%dT%H:%M:%S'),
                    offence_date=datetime.strptime(offence_date, '%Y-%m-%dT%H:%M:%S'),
                    call_dt=datetime.strptime(call_dt, '%Y-%m-%dT%H:%M:%S'),
                    disposition=disposition,
                    address=address,
                    city_id=city.id,
                    state_id=state.id,
                    agency_id=agency.id
                )
                crimes.append(crime)
            
                if i % 10000 == 0:
                    session.bulk_save_objects(crimes)
                    session.commit()
                    crimes = []
                
                bar.next()
        
            session.commit()
            file_logger.info(f'DB filling up finished at {datetime.now()}')
            file_logger.info(f'{total_records} added to db')
            file_logger.info(
                f'Time elapsed: {(datetime.now() - filling_db_started).total_seconds()} seconds'
            )
            bar.finish()


if __name__ == '__main__':
    fill_db(data_url)
