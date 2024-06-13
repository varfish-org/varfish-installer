# syntax=docker/dockerfile:1.3

# ---------------------------------------------------------------------------
# Python Base Image
# ---------------------------------------------------------------------------

FROM python:3.11-bookworm AS python-base

LABEL org.opencontainers.image.authors="Manuel.Holtgrewe@bih-charite.de"
LABEL org.opencontainers.image.source https://github.com/varfish-org/varfish-installer

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

ENV DEBIAN_FRONTEND noninteractive
ENV CUSTOM_STATIC_DIR /usr/src/app/local-static,frontend/static

WORKDIR /usr/src/app

# ---------------------------------------------------------------------------
# Python Dependencies
# ---------------------------------------------------------------------------

FROM python-base AS python-deps

# Install pip and pipenv
RUN python -m pip install -U pip pipenv

# Copy Pipfile and lock into the Docker image.
COPY src/Pipfile src/Pipfile.lock ./

# Install Python dependencies via pipenv.
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install \
        --python=/usr/local/bin/python \
        --deploy

# ---------------------------------------------------------------------------
# Python Runtime
# ---------------------------------------------------------------------------

FROM python-base as python-runtime

# Install runtime dependencies
RUN apt-get install -y libsqlite3-dev

# Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /usr/local/bin/wait
RUN chmod +x /usr/local/bin/wait

# Copy the worker from the dedicated worker build.
COPY --from=ghcr.io/varfish-org/varfish-server-worker:main /usr/local/bin/varfish-server-worker /usr/local/bin/varfish-server-worker

# Copy virtual env from python-deps stage
COPY --from=python-deps /usr/src/app/.venv /usr/src/app/.venv
ENV PATH="/usr/src/app/.venv/bin:$PATH"

# Copy in the source code and install it.
COPY src /tmp/src
RUN pushd /tmp/src && \
    pip install . &&
    rm -rf /tmp/src

# Define the entry point
COPY utils/docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
