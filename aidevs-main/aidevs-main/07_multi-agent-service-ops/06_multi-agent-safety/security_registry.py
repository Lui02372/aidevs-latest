"""
[파일 역할]
06의 여러 Lab이 같은 YAML 보안 정책을 읽도록 돕는 공통 모듈입니다.
Lab에서 실행할 시나리오는 아니며, 정책 파일의 위치와 읽기 방법을 한곳에 모읍니다.
초보자는 먼저 security_policies.yaml을 열어 값과 Python 로직의 책임을 비교합니다.
"""

from __future__ import annotations

from pathlib import Path

import yaml


POLICY_PATH = Path(__file__).with_name("security_policies.yaml")


def load_security_policies() -> dict[str, object]:
    """사람이 읽는 YAML 정책을 Python 딕셔너리로 불러옵니다."""
    with POLICY_PATH.open(encoding="utf-8") as policy_file:
        policies = yaml.safe_load(policy_file)
    if not isinstance(policies, dict):
        raise ValueError("보안 정책의 최상위 값은 객체여야 합니다.")
    return policies
