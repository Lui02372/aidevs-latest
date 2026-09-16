"""Container 내부에서 API Liveness를 검사하고 성공 여부를 종료 코드로 반환합니다."""

import sys
from urllib.request import urlopen


try:
    with urlopen("http://127.0.0.1:8000/health/live", timeout=3) as response:
        sys.exit(0 if response.status == 200 else 1)
except Exception as error:
    print(f"health check failed: {type(error).__name__}: {error}")
    sys.exit(1)
