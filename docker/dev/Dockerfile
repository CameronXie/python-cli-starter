FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN set -eux \
    && apt-get update && apt-get install -y --no-install-recommends \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg \
      jq \
      less \
      lsb-release \
      make \
      tree \
      vim \
      zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry>=1.7 pipx>=0.1

# TODO: Remove this once IntelliJ supports refresh Python packages in container.
COPY pyproject.toml poetry.lock /tmp/build/
WORKDIR /tmp/build
RUN poetry install \
    && rm -rf /tmp/build
