"""환경변수 설정을 읽는 파일입니다.

프로젝트가 커지면 API 주소, retry 횟수, AWS region 같은 값을 코드에 직접 쓰지 않고
.env 또는 배포 환경변수로 관리합니다.
"""

import os


APP_ENV = os.getenv("APP_ENV", "local")
MAX_RETRY_COUNT = int(os.getenv("MAX_RETRY_COUNT", "2"))
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
