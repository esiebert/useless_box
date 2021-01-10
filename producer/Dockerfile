FROM python:3.7.1

COPY ./producer/requirements.txt /usr/src/app/requirements.txt
COPY ./common/requirements.txt /usr/src/app/common/requirements.txt

WORKDIR /usr/src/app/

RUN pip install -r requirements.txt -r common/requirements.txt

COPY . .

RUN mypy --ignore-missing-imports ./producer
RUN pylint ./producer/*.py
