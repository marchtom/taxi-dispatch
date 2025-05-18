# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install poetry==2.1.3

RUN apt-get update \
    && apt-get install -y build-essential

COPY pyproject.toml poetry.lock ./

# # Install any needed dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY app/ app/
EXPOSE 8081

# Run main.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
