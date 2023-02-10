FROM python:3.11.1-buster

WORKDIR /usr/src/mapper

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/mapper/requirements.txt
COPY . /usr/src/mapper/

RUN pip install -r /usr/src/mapper/requirements.txt

CMD [ "pytest", "test_mapper.py" ]
