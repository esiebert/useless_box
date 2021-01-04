FROM python:3.7.1

COPY ./consumer/requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app/

RUN pip install -r requirements.txt

COPY . .

RUN mypy --ignore-missing-imports ./producer
RUN pylint ./consumer/*.py
