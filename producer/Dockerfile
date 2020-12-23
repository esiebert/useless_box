FROM python:3.7.1

COPY ./producer/requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app/

RUN pip install -r requirements.txt

COPY . .
