FROM python:3.8

# path
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/usr/src/app


RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # curl
  curl

# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata

# timezone env with default
ENV TZ=Europe/Kiev

# Upgrade pip
RUN pip install --upgrade pip
RUN pip install setuptools

# where the code lives
WORKDIR $PYTHONPATH

# poetry
RUN pip install poetry
ENV PATH "/root/.local/bin:$PATH"

RUN pip install moralis

# pyproject poetry
COPY poetry.lock pyproject.toml ./


RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-root --only main --no-interaction --no-ansi


COPY . .

