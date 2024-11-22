ARG UBUNTU_TAG=24.04
ARG QNAP8528=v1.2

FROM ubuntu:${UBUNTU_TAG}
RUN apt update && apt install -y \
  gcc \
  git \
  kmod \
  libelf-dev \
  make \
  && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/0xGiddi/qnap8528.git \
  && cd qnap8528 \
  && git checkout ${QNAP8528}