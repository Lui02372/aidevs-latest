# 다음 과정과의 연결

`02_python-advanced`에서 배우는 내용은 `02_supabase-ai-backend`의 FastAPI 코드와 직접 연결됩니다.

| 이번 단원 | 다음 과정에서 만나는 모습 |
| --- | --- |
| 함수 | FastAPI endpoint 함수, service 함수 |
| import | `from app.services import ...` 같은 파일 분리 |
| try/except | API 호출 실패, JSON 파싱 실패, 외부 서비스 오류 처리 |
| raise | 잘못된 입력을 발견했을 때 오류 발생 |
| JSON | API 응답 구조, 설정 파일, 로그 저장 |
| pytest | endpoint와 service 함수 테스트 |
| project structure | `app/main.py`, `routers`, `schemas`, `services` 구조 |
| dataclass object | 이후 Pydantic `BaseModel`을 이해하기 위한 준비 |

이번 단원에서 모든 문법을 외울 필요는 없습니다. 다음 과정의 코드를 읽을 때 “이 파일은 어떤 역할인가?”를 구분하는 것이 핵심입니다.
