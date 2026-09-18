#!/usr/bin/env bash
set -euo pipefail
# SSM AWS-RunShellScript에서 root로 실행. 환경 파일은 서버에서만 관리한다.
release_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$release_dir"
test -s /opt/weather-07/shared/.env
ln -sfn /opt/weather-07/shared/.env .env
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.application.yml config --quiet
docker compose -f compose.infrastructure.yml up -d --wait --wait-timeout 120
# 실행 중인 앱을 내리기 전에 build한다. DB/Redis의 project name과 volume은 고정한다.
docker compose -f compose.application.yml build
docker compose -f compose.application.yml up -d --wait --wait-timeout 180
curl --fail --retry 6 --retry-delay 5 --retry-all-errors http://127.0.0.1:8000/health/ready
ln -sfn "$release_dir" /opt/weather-07/current
echo "Deployment readiness passed: $release_dir"
