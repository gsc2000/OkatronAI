FROM python:3.9-buster

ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools wheel

COPY ./ ./FastAPI/
WORKDIR /FastAPI

RUN pip install -r requirements.txt

CMD "python3 App.py"