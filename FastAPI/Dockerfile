FROM python:3.9

COPY ./fastapi/requirements.txt ./fastapi/requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./fastapi/requirements.txt
RUN rm -rf ./fastapi/requirements.txtc

COPY ./fastapi/api ./fastapi/api