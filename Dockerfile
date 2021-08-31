FROM python:3.6

ENV CMAKE_VERSION=3.21.2
ENV CMAKE_BUILD=2
RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y zlib1g-dev libpng-dev libjpeg-dev
RUN apt-get install -y ninja-build yasm

WORKDIR /opt/
RUN wget https://github.com/Kitware/CMake/releases/download/v$CMAKE_VERSION/cmake-$CMAKE_VERSION.tar.gz
RUN tar -xzvf cmake-$CMAKE_VERSION.tar.gz
WORKDIR /opt/cmake-$CMAKE_VERSION/
RUN ls -la
RUN ./bootstrap
RUN make -j$(nproc)
RUN make install
RUN cmake --version

WORKDIR /opt/
RUN git clone -b v0.9.1 https://github.com/AOMediaCodec/libavif.git
WORKDIR /opt/libavif/ext
RUN ./aom.cmd

WORKDIR /opt/libavif/build/
RUN cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=0 -DAVIF_CODEC_AOM=1 -DAVIF_LOCAL_AOM=1 -DAVIF_BUILD_APPS=1 ..
RUN make
RUN cp ./avifenc /usr/bin/

WORKDIR /app/avif_converter/
# RUN avifenc
