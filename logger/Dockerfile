FROM python:3.7.1

RUN python -m venv /venv

COPY ./logger/requirements.txt /usr/src/app/requirements.txt
COPY ./common/requirements.txt /usr/src/app/common/requirements.txt

WORKDIR /usr/src/app/

RUN /venv/bin/pip install -r requirements.txt -r common/requirements.txt

COPY logger logger
COPY common common
COPY .pylintrc ./

RUN /venv/bin/pip install --no-cache ./logger ./common

RUN /venv/bin/mypy --ignore-missing-imports ./logger
RUN /venv/bin/pylint ./logger/logger/*.py
#RUN /venv/bin/pytest
