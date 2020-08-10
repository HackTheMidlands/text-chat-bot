FROM python:3-alpine

RUN mkdir -p /opt/chat-manager
WORKDIR /opt/chat-manager

RUN apk add gcc make libffi-dev musl-dev postgresql-dev
RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /opt/chat-manager/
RUN poetry install --no-root

COPY . /opt/chat-manager

CMD ./docker-entrypoint.sh
