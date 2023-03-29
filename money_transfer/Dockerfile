FROM python:3.11.1-buster

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /usr/src/money_transfer

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/money_transfer/requirements.txt
COPY . /usr/src/money_transfer/
COPY ./entrypoint.sh /usr/src/money_transfer/entrypoint.sh

RUN pip install -r /usr/src/money_transfer/requirements.txt

ENTRYPOINT ["/usr/src/money_transfer/entrypoint.sh"]
