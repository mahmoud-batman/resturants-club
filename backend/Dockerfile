FROM python:3
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /app/backend/
WORKDIR /app/backend/

RUN apt-get update \
    && apt-get install -yyq netcat

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/app/backend/entrypoint.sh"]
