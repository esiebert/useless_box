FROM python:3.7.1

COPY ./consumer/requirements.txt /usr/src/app/requirements.txt
COPY ./common/requirements.txt /usr/src/app/common/requirements.txt

WORKDIR /usr/src/app/

RUN pip install -r requirements.txt -r common/requirements.txt

COPY ./consumer/ ./consumer/
COPY ./common/ ./common/

RUN mypy --ignore-missing-imports ./consumer
RUN pylint ./consumer/*.py
