FROM python:3-alpine AS POETRY
ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /bin/get-poetry

ARG POETRY_HOME=/etc/poetry
ARG POETRY_VERSION=1.1.2
RUN python /bin/get-poetry

WORKDIR /poetry
COPY ./pyproject.toml ./poetry.lock ./
RUN /etc/poetry/bin/poetry export -f requirements.txt > requirements.txt

FROM python:3.8.5-alpine3.12 AS BUILD

RUN apk add --no-cache --virtual .build-deps \
      gcc \
      musl-dev

WORKDIR /opt/chat-manager

COPY --from=poetry /poetry/requirements.txt .

RUN pip install -r /opt/chat-manager/requirements.txt && \
      apk del .build-deps

COPY . /opt/chat-manager

VOLUME [ "/data" ]

ENTRYPOINT ["./docker-entrypoint.sh"]
