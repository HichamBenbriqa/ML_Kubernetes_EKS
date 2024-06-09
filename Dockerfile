#
# Build image: get requirements.txt from the the pyproject.toml file.
#

FROM python:3.10.9-slim AS builder

WORKDIR /app
COPY pyproject.toml /app
COPY poetry.lock /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN PIP_TIMEOUT=500 poetry install --no-root --without dev
RUN poetry export -f requirements.txt >> requirements.txt

#
# Prod image
#

FROM python:3.10.9-slim AS runtime

WORKDIR /app

COPY .env /app/.env

COPY app.py neptune_utils.py /app/

COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN pip install --default-timeout=1000 --no-cache-dir -r /app/requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8001", "-w", "4", "app:main()"]