FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y default-jdk

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]
