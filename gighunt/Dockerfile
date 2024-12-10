FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry==1.8.5 && poetry install --no-cache-dir

CMD ["poetry", "run", "start-backend"]
