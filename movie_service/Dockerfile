FROM python:3.8-slim

COPY /app /app

COPY requirements.txt ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /

ENTRYPOINT ["python" , "app/main.py"]