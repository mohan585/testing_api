FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y openjdk-11-jre-headless && apt-get clean

RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["waitress-serve", "--call", "main:app"]
