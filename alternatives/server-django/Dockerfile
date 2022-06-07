# Builder, tester and runtime container for local development
FROM python:3.9
# FOR SPARK: FROM bitnami/spark:3 as builder

ENV NODE_ENV development
ENV PYTHON_ENV development
ENV DJANGO_ENV development
ENV DJANGO_APP django

RUN useradd supervisor && useradd python

RUN apt-get -y update && apt-get -y install \
  build-essential \
  libffi-dev \
  python3-dev \
  libssl-dev \
  cargo \
  gdal-bin \
  libgdal-dev \
  supervisor \
  npm

ENV PYTHONPATH=/develop/django
RUN mkdir -p /develop
WORKDIR /develop

ARG SERVICE_DIR=.

# FOR SPARK:
# COPY ${SERVICE_DIR}/spark-libs.sh /tmp/
# RUN /tmp/spark-libs.sh

COPY ${SERVICE_DIR}/requirements-dev.txt /develop/
RUN pip3 install --upgrade pip pip-tools debugpy
RUN pip3 install -r requirements-dev.txt

EXPOSE 8080
CMD pip-compile requirements-dev.in; \
  pip-compile requirements-prod.in; \
  pip3 install -r requirements-dev.txt; \
  ./start.sh
