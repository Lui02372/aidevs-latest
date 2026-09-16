# FastAPI DB 연동 패턴

FastAPI에서 DB를 연결할 때는 처음부터 복잡한 구조를 만들기보다, 작은 예제로 흐름을 이해한 뒤 역할별로 분리합니다.

이 과정에서는 Supabase SDK를 사용해 FastAPI와 Supabase를 연결합니다.

## 처음에는 단순하게 시작

초반 실습에서는 `main.py` 안에 endpoint, Pydantic model, Supabase 호출 코드를 함께 작성해도 됩니다.

```text
main.py
```

이 방식은 파일이 적어서 흐름을 보기 쉽습니다.

## 프로젝트가 커질 때 분리하는 구조

기능이 많아지면 아래처럼 역할을 나누는 것이 좋습니다.

기본적인 `main.py`, `routers`, `schemas`, `services`, `tests` 분리는 앞 단원의 `01_fastapi-backend/10_labs/lab-100_project-structure-refactor`에서 먼저 연습했습니다.

```text
app
├─ main.py
├─ settings.py
├─ database.py
├─ schemas.py
├─ repositories
│  └─ notes_repository.py
└─ services
   └─ notes_service.py
```

## 역할

| 파일 또는 폴더 | 역할 |
|---|---|
| `main.py` | FastAPI 앱 생성과 라우팅 |
| `settings.py` | `.env` 환경변수 읽기 |
| `database.py` | Supabase client 생성 |
| `schemas.py` | 요청/응답 Pydantic 모델 |
| `repositories` | Supabase table 호출 |
| `services` | 서비스 규칙과 비즈니스 로직 |

## 현재 과정에서의 기준

`03_fastapi-supabase-integration`에서는 먼저 단일 `main.py` 중심으로 흐름을 익힙니다.

이후 미니 프로젝트나 최종 프로젝트로 확장할 때는 역할별 분리를 적용할 수 있습니다.

## Supabase 호출 위치

Supabase table을 직접 호출하는 코드는 endpoint 안에 계속 늘어놓기보다, 프로젝트가 커지면 repository 함수로 분리하는 것이 좋습니다.

```python
def create_note(title: str, content: str) -> dict:
    return (
        supabase.table("learning_notes")
        .insert({"title": title, "content": content})
        .execute()
        .data[0]
    )
```

endpoint는 요청과 응답 흐름을 담당하고, repository는 데이터 저장소 호출을 담당하게 나누면 코드를 읽기 쉬워집니다.
