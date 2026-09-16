"""Lab 03-07에서 반복되는 Worker 설정을 YAML로 읽습니다.

Router·Supervisor의 판단과 실행 순서는 Python에 남겨 두고, Worker의 이름, 목표,
지시문, Provider처럼 같은 형식으로 반복되는 선언만 YAML에서 관리합니다.
"""

from pathlib import Path

import yaml


DEFINITION_FILE = Path(__file__).resolve().parent / "worker_definitions.yaml"


def load_worker_registry() -> dict[str, dict[str, str]]:
    document = yaml.safe_load(DEFINITION_FILE.read_text(encoding="utf-8"))
    workers = document.get("workers", {})
    if not workers:
        raise ValueError("YAML에 workers 설정이 없습니다.")

    required_fields = {"name", "goal", "instructions", "provider", "output_contract"}
    for agent_id, config in workers.items():
        missing_fields = required_fields - set(config)
        if missing_fields:
            raise ValueError(f"{agent_id}에 필요한 설정이 없습니다: {sorted(missing_fields)}")
    return workers
