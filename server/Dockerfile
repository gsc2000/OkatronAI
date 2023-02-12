FROM python:3.9-buster

ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools wheel

COPY ./server/ ./server/