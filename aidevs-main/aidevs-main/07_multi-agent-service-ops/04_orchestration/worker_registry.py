"""반복 Worker와 Team 선언을 YAML에서 읽고 시작 시점에 검증합니다."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent


def load_yaml(filename: str) -> dict:
    return yaml.safe_load((ROOT / filename).read_text(encoding="utf-8"))


def load_registry() -> tuple[dict[str, dict], dict[str, dict]]:
    workers = load_yaml("worker_definitions.yaml")["workers"]
    teams = load_yaml("team_definitions.yaml")["teams"]

    required_worker_fields = {"name", "goal", "provider", "output_contract"}
    for agent_id, config in workers.items():
        missing = required_worker_fields - set(config)
        if missing:
            raise ValueError(f"{agent_id} 설정 필드 누락: {sorted(missing)}")

    for team_id, team in teams.items():
        referenced = {
            *team["parallel_workers"],
            *team["required_workers"],
            *team["optional_workers"],
        }
        unknown = referenced - set(workers)
        if unknown:
            raise ValueError(f"{team_id}의 미등록 Worker: {sorted(unknown)}")
        if not set(team["required_workers"]).issubset(team["parallel_workers"]):
            raise ValueError(f"{team_id}의 필수 Worker가 병렬 목록에 없습니다.")

    return workers, teams
