FROM python:3.9.16-buster

WORKDIR /usr/src/app


RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "api.py"]