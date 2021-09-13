FROM nvidia/cuda:11.1-devel-ubuntu20.04

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

# タイムゾーン設定
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Tokyo
ENV NVIDIA_VISIBLE_DEVICES all

RUN apt-get update \
    && cd /usr/local/bin \
    # tzdataのinteractive configurationバイパス用
    && DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata \
    && apt-get install -y libgl1-mesa-dev \
    && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 libpq-dev  \
    # SCREEEN
    && apt-get install -y screen \
    # # Python
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -r /usr/src/app/requirements.txt
COPY . /usr/src/app