FROM python:3.9-buster

ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools wheel

# COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# COPY ./ ./server/