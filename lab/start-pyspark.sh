#!/bin/bash
set -e

wrapper=""
if [[ "${RESTARTABLE}" == "yes" ]]; then
    wrapper="run-one-constantly"
fi

export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="lab --no-browser --ip=${BIND_ADDR:-0.0.0.0} --port=${BIND_PORT:-8888} --LabApp.allow_origin=${COMMON_URL} ${JUPYTER_OPTIONS}"

. /usr/local/bin/start.sh $wrapper pyspark "$@"
