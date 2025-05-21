FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==2.1.3

RUN apt-get update \
    && apt-get install -y build-essential

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

CMD ["python", "main.py"]
