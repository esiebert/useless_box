FROM python:3.7.1

RUN python -m venv /venv

COPY ./producer/requirements.txt /usr/src/app/requirements.txt
COPY ./common/requirements.txt /usr/src/app/common/requirements.txt

WORKDIR /usr/src/app/

RUN /venv/bin/pip install -r requirements.txt -r common/requirements.txt

COPY producer producer
COPY common common
COPY .pylintrc ./

RUN /venv/bin/pip install --no-cache ./producer ./common

RUN /venv/bin/mypy --ignore-missing-imports ./producer
RUN /venv/bin/pylint ./producer/producer/*.py
