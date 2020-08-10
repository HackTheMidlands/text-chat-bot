FROM python:3-alpine AS POETRY
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /bin/get-poetry

ARG POETRY_HOME=/etc/poetry
ARG POETRY_VERSION=1.0.5
RUN python /bin/get-poetry

WORKDIR /poetry
COPY ./pyproject.toml ./poetry.lock ./
RUN /etc/poetry/bin/poetry export -f requirements.txt > requirements.txt

FROM alpine AS config

RUN apk add --no-cache make gettext

ARG TOKEN
ARG SERVER_ID
ARG CATAGORY_ID

WORKDIR /app

COPY Makefile config_template.json /app/

RUN make config

FROM python:3.8.5-alpine3.12 AS BUILD

RUN apk add --no-cache --virtual .build-deps \
      gcc \
      musl-dev

WORKDIR /opt/chat-manager

COPY --from=poetry /poetry/requirements.txt .

RUN pip install -r /opt/chat-manager/requirements.txt && \
      apk del .build-deps

COPY --from=config /app/config.json /opt/chat-manager

COPY . /opt/chat-manager

ENTRYPOINT ["./docker-entrypoint.sh"]
