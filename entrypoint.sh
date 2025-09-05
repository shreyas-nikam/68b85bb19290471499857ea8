#!/bin/sh
set -eu

# Load env vars if baked in
if [ -f /run/secrets/app.env ]; then
  set -a
  . /run/secrets/app.env
  set +a
fi

exec streamlit run app.py \
  --server.address=0.0.0.0 \
  --server.port="${PORT:-8501}" \
  --server.headless=true
