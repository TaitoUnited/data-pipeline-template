#!/bin/sh
set -e

if [ ${PYTHON_ENV} = "development" ]; then
  # Start Jupyter in background
  python src/manage.py shell_plus --notebook &

  if [ ${MODE} = "worker" ]; then
    # Start worker threads in foreground
    supervisord --configuration supervisord-worker.conf
  fi

  if [ ${MODE} = "any" ]; then
    # Start worker threads in background
    supervisord --configuration supervisord-worker.conf &
  fi

  if [ ${MODE} = "api" ] || [ ${MODE} = "any" ]; then
    # Start django API in development mode
    python -m debugpy --listen 0.0.0.0:9229 -m \
      src.manage runserver $API_BINDADDR:$API_PORT
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
