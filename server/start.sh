#!/bin/sh
set -e

if [ ${MODE} = "worker" ]; then
  # Start worker threads
  ./execute start_worker
elif [ ${PYTHON_ENV} = "development" ]; then
  # Start flask API in development mode
  python -m debugpy --listen 0.0.0.0:9229 -m \
    flask run --host $API_BINDADDR --port $API_PORT --no-debugger
else
  # Start flask API with uwsgi
  uwsgi --ini uwsgi.ini
fi
