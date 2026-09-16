"""Auto Healing worker 예시입니다.

실행 방법:
    cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
    python worker/main.py

실제 프로젝트에서는 이 worker가 큐나 DB에서 장애 이벤트를 가져와 처리할 수 있습니다.
"""

import time


def main() -> None:
    """worker가 살아 있음을 주기적으로 보여 주는 최소 예제입니다."""

    while True:
        print("[worker] waiting for auto healing events...")
        time.sleep(10)


if __name__ == "__main__":
    main()
