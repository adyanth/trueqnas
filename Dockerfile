ARG UBUNTU_TAG=24.04

FROM ubuntu:${UBUNTU_TAG} AS makemkv
ARG MAKEMKV_VERSION=1.18.1
ARG MAKEMKV_OSS_URL=https://www.makemkv.com/download/makemkv-oss-${MAKEMKV_VERSION}.tar.gz
ARG MAKEMKV_BIN_URL=https://www.makemkv.com/download/makemkv-bin-${MAKEMKV_VERSION}.tar.gz
RUN apt update && apt install -y \
  build-essential \
  pkg-config \
  libc6-dev \
  libssl-dev \
  libexpat1-dev \
  libavcodec-dev \
  libgl1-mesa-dev \
  qtbase5-dev \
  wget \
  zlib1g-dev
RUN wget ${MAKEMKV_OSS_URL} && \
  tar xzvf makemkv-oss-${MAKEMKV_VERSION}.tar.gz && \
  cd makemkv-oss-${MAKEMKV_VERSION} && \
  ./configure && \
  ENABLE_GUI=false make && \
  ENABLE_GUI=false make install
RUN wget ${MAKEMKV_BIN_URL} && \
  tar xzvf makemkv-bin-${MAKEMKV_VERSION}.tar.gz && \
  cd /makemkv-bin-${MAKEMKV_VERSION} && \
  install -t /usr/bin bin/amd64/makemkvcon

FROM ubuntu:${UBUNTU_TAG} AS trueqnas
ARG QNAP8528=v1.4
RUN apt update && apt install -y \
  evtest \
  gcc \
  git \
  kmod \
  libelf-dev \
  make \
  python3 \
  python3-evdev \
  rsync \
  libexpat1-dev \
  libavcodec-dev \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN git clone https://github.com/0xGiddi/qnap8528.git \
  && cd qnap8528 \
  && git checkout ${QNAP8528}
WORKDIR /app
COPY . .
COPY --from=makemkv /usr/lib/lib*.so* /usr/lib/
COPY --from=makemkv \
  /usr/bin/makemkvcon \
  /usr/bin/mmccextr \
  /usr/bin/mmgplsrv \
  /usr/bin/
ENTRYPOINT [ "/app/entrypoint.sh" ]
