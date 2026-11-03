#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME=kc-h04-sredir
export PYTHONUNBUFFERED=1

LABEL="KC-H04-SAML-REDIRECT"
WITNESS="kcs04b8n1"
BASE="http://127.0.0.1:18084"

down() {
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  local reason="$1"
  echo "FAIL ${LABEL} ${reason} ${WITNESS}" | tee poc-last-run.txt
  down
  exit 1
}

trap down EXIT

rm -f last-hop.html keycloak-tail.log
down

echo "== docker compose up =="
if ! docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
  fail_setup "compose-up-failed"
fi

echo "== wait ${BASE}/realms/master =="
ready=0
for i in $(seq 1 120); do
  code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 8 \
    "${BASE}/realms/master" || true)"
  if [[ "${code}" == "200" ]]; then
    ready=1
    echo "IOC master-ready attempt=${i} http=${code}"
    break
  fi
  echo "IOC master-wait attempt=${i} http=${code}"
  sleep 3
done
if [[ "${ready}" != 1 ]]; then
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 keycloak || true
  fail_setup "master-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py
rc=$?
set -e

if [[ "${rc}" -ne 0 ]]; then
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=160 keycloak > keycloak-tail.log || true
fi

if [[ ! -f poc-last-run.txt ]] || ! tail -n 1 poc-last-run.txt | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit-${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

exit "${rc}"
