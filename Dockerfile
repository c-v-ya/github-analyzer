FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # Dependencies for building Python packages
  && apt-get install -y build-essential \
  # Installing `poetry` package manager
  # https://github.com/python-poetry/poetry
  && pip install 'poetry>=1.0'  \
  && poetry --version \
  # Cleaning cache
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .
ENTRYPOINT ["python", "main.py"]