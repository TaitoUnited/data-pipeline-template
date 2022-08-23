#!/bin/sh
set -e

# Read db password from env variable or secret file
export DATABASE_PASSWORD_SECRET="$(cat /run/secrets/DATABASE_PASSWORD)"
export DATABASE_PASSWORD=${DATABASE_PASSWORD:-$DATABASE_PASSWORD_SECRET}

if [ ${PYTHON_ENV} = "development" ]; then
  if [ ${MODE} = "worker" ]; then
    # Start worker threads in foreground
    supervisord --configuration supervisord-worker.conf
  fi

  if [ ${MODE} = "any" ]; then
    # Start worker threads in background
    supervisord --configuration supervisord-worker.conf &
  fi

  if [ ${MODE} = "api" ] || [ ${MODE} = "any" ]; then
    # Start flask API in development mode
    python -m debugpy --listen 0.0.0.0:9229 -m \
      flask run --host $API_BINDADDR --port $API_PORT --no-debugger
  fi
else
  if [ ${MODE} = "worker" ]; then
    # Start worker threads
    supervisord --configuration supervisord-worker.conf
  fi

  if [ ${MODE} = "api" ]; then
    # Start API
    supervisord --configuration supervisord.conf
  fi

  if [ ${MODE} = "any" ] || [ "${MODE}" = "" ]; then
    echo "Mode 'any' not allowed on production"
  fi
fi
