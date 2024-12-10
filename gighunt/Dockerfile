FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install poetry && poetry install

CMD ["poetry", "run", "start-backend"]
