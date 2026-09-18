#!/usr/bin/env bash
set -Eeuo pipefail
# Run on EC2: bash releases/<sha>/deploy.sh <sha>
release=${1:?Usage: deploy.sh GIT_SHA}
[[ "$release" =~ ^[0-9a-f]{40}$ ]] || { echo 'Expected full commit SHA'; exit 2; }
base="$HOME/multi-agent-09"
mkdir -p "$base/shared"
exec 9>"$base/shared/deploy.lock"
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
export APP_ENV_FILE="$base/shared/app.env"
export APP_IMAGE="multi-agent-09:$release"
test -s "$APP_ENV_FILE"
chmod 600 "$APP_ENV_FILE"
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
compose=(docker compose --project-name multi-agent-09 -f "$here/compose.yaml")
override=()
if [[ -f "$base/shared/compose.override.yaml" ]]; then
  override=(-f "$base/shared/compose.override.yaml")
  compose+=("${override[@]}")
fi
"${compose[@]}" config --quiet
docker image inspect "$APP_IMAGE" >/dev/null
# Schema is deliberately initialized once by the learner, not during every release.
"${compose[@]}" run --rm --no-deps api python 09_integrated-deployment-and-operations/deploy/ec2/check_database.py
previous=''
if [[ -f "$base/shared/current" ]]; then previous=$(cat "$base/shared/current"); fi
rollback() {
  trap - ERR
  echo 'Deployment failed; attempting previous application release.'
  if [[ "$previous" =~ ^[0-9a-f]{40}$ && -f "$base/releases/$previous/compose.yaml" ]]; then
    export APP_IMAGE="multi-agent-09:$previous"
    docker compose --project-name multi-agent-09 -f "$base/releases/$previous/compose.yaml" "${override[@]}" up -d --wait --wait-timeout 180 || echo 'Rollback failed: inspect EC2 containers.'
  else
    echo 'No previous release exists. Inspect EC2 containers; data volumes are retained.'
  fi
  exit 1
}
trap rollback ERR
"${compose[@]}" up -d --wait --wait-timeout 180
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:18000/health/ready
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:18501/_stcore/health
"${compose[@]}" exec -T api python 09_integrated-deployment-and-operations/deploy/ec2/check_database.py
printf '%s\n' "$release" > "$base/shared/current.tmp"
mv "$base/shared/current.tmp" "$base/shared/current"
trap - ERR
echo "Application release ready: $release"
