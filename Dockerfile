FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y openjdk-11-jre-headless && apt-get clean

RUN pip install waitress

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["waitress-serve", "--call", "app:create_app"]
