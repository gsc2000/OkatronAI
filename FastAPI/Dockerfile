# python3.9のイメージをダウンロード
FROM python:3.9-buster

ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev

# # pipを使ってpoetryをインストール
# RUN python -m venv .venv
# RUN echo "source /.venv/bin/activate"
RUN pip install --upgrade pip setuptools
RUN pip install opencv-python greenlet fastapi uvicorn jinja2

# uvicornのサーバーを立ち上げる
# ENTRYPOINT ["python", "fastapi_app.py"]