# Builder, tester and runtime container for local development
FROM python:3.9
# FOR SPARK: FROM bitnami/spark:3 as builder

# Install python dependencies
RUN apt-get -y update && apt-get -y install \
  build-essential \
  libffi-dev \
  python3-dev \
  libssl-dev \
  cargo

RUN mkdir -p /develop
WORKDIR /develop
ENV PYTHONPATH /develop

ARG SERVICE_DIR=.
COPY ${SERVICE_DIR}/*.in ${SERVICE_DIR}/spark-libs.sh /tmp/
RUN pip3 install --upgrade pip pip-tools
RUN pip-compile /tmp/requirements-dev.in && \
    pip-compile /tmp/requirements-prod.in && \
    pip3 install -r /tmp/requirements-dev.txt && \
    pip3 install debugpy

# FOR SPARK: RUN /tmp/spark-libs.sh

# TODO: use debugpy
CMD cp /tmp/*.txt /develop && python3 src/server.py
