ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim-bullseye as poetry

RUN set -x; apt-get update \
    && apt-get install -y \
        curl \
        gcc \
    && curl \
        -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py \
        | python -

WORKDIR /srv
COPY . .

RUN set -x; . $HOME/.poetry/env \
    && poetry config virtualenvs.create false \
    && poetry install

FROM poetry as test

RUN scripts/test

FROM poetry as release

ARG PYPI_TOKEN
ARG CODECOV_TOKEN
ARG GIT_SHA

COPY --from=test /srv/coverage.xml .

RUN . $HOME/.poetry/env \
    && poetry publish --build \
        --username __token__ \
        --password $PYPI_TOKEN \
    && codecov \
        --token $CODECOV_TOKEN \
        --commit $GIT_SHA