"""운영 이벤트 로그를 남기는 위치입니다.

처음에는 print 또는 메모리 저장으로 시작하고,
프로젝트가 확장되면 DB, CloudWatch, 외부 로그 시스템으로 연결할 수 있습니다.
"""


def write_event_log(message: str) -> None:
    """운영 이벤트를 콘솔에 출력합니다."""

    print(f"[auto-healing-event] {message}")
