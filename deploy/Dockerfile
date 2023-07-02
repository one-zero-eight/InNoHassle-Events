# Based on https://github.com/svx/poetry-fastapi-docker/blob/main/Dockerfile

###########################################################
# Base Python image. Set shared environment variables.
FROM python:3.11-slim-bullseye as base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_INSTALLER_MAX_WORKERS=10 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


###########################################################
# Builder stage. Build dependencies.
FROM base AS builder
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        vim \
        netcat \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry. Respects $POETRY_VERSION and $POETRY_HOME
ENV POETRY_VERSION=1.5.1
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    chmod a+x /opt/poetry/bin/poetry

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --only main,prod


###########################################################
# Production stage. Copy only runtime deps that were installed in the Builder stage.
FROM base AS production

COPY --from=builder $VENV_PATH $VENV_PATH

COPY ./deploy/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Create user with the name poetry
RUN groupadd -g 1500 poetry && \
    useradd -m -u 1500 -g poetry poetry

COPY --chown=poetry:poetry ./src /code/src
USER poetry
WORKDIR /code

EXPOSE 8000
ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD [ "gunicorn", "--worker-class uvicorn.workers.UvicornWorker", "--bind 0.0.0.0:8000", "--workers 4", "src.main:app" ]
