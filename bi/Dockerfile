FROM apache/superset:latest as builder

USER root

RUN mkdir -p /app/docker
COPY original/*.sh /app/docker
COPY original/*.py /app/pythonpath

ENV FLASK_ENV production
ENV SUPERSET_ENV production
ENV SUPERSET_PORT 8080
ENV SUPERSET_LOAD_EXAMPLES no
ENV CYPRESS_CONFIG false

USER superset
