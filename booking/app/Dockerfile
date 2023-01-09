FROM python:3.9.16-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

COPY loadenv.py ./

CMD ["python", "./loadenv.py"]
