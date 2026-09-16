# 01. Debugging Playbook

오류가 나면 바로 코드를 고치기보다, 먼저 재현 가능한 정보를 모읍니다.

좋은 디버깅은 추측으로 시작하지 않습니다. "어디서, 어떤 명령으로, 무엇을 기대했는데, 실제로 무엇이 나왔는지"를 정리하는 것부터 시작합니다.

## 1. 실행 명령 확인

어떤 폴더에서 어떤 명령을 실행했는지 확인합니다.

```powershell
Get-Location
python -c "import sys; print(sys.executable)"
```

FastAPI 실행 예:

```powershell
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload
```

수업 자료에서는 아래 방식도 자주 사용합니다. Windows에서 `uvicorn.exe`가 보안 정책에 막힐 때는 `python -m uvicorn` 방식이 더 안정적입니다.

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 2. 오류 유형 분류

| 오류 유형 | 먼저 볼 것 |
| --- | --- |
| `ModuleNotFoundError` | `.venv` 활성화, `pip install -r requirements.txt` 실행 여부 |
| 404 Not Found | URL 경로가 코드의 endpoint와 같은지 |
| 405 Method Not Allowed | GET/POST/PUT/DELETE를 맞게 사용했는지 |
| 422 Validation Error | 요청 Body가 Pydantic 모델과 맞는지 |
| Gemini 503 | 모델 수요가 높아 일시적으로 실패했는지 |
| Supabase table error | 테이블명과 컬럼명이 실제 SQL과 같은지 |
| Invalid login credentials | 회원가입 여부, 이메일 인증 설정, 비밀번호 확인 |
| RLS access error | JWT/Bearer token, RLS policy, key 종류 확인 |
| Redis cache miss | key 이름, TTL 만료 여부, Upstash REST URL/token |
| pytest 실패 | 어떤 테스트 함수가 실패했는지, 기대값과 실제값 차이 |

## 3. Traceback 읽는 순서

Traceback은 위에서부터 전부 읽기보다 아래쪽부터 봅니다.

```text
마지막 줄: 오류 종류와 핵심 메시지
그 위 몇 줄: 내 파일의 어느 줄에서 터졌는지
더 위쪽: FastAPI, Supabase, httpx 같은 라이브러리 내부 호출
```

예를 들어 `ModuleNotFoundError`라면 먼저 `.venv`와 패키지 설치를 확인합니다. `HTTPException`이라면 내가 의도적으로 반환한 오류 메시지일 수 있으므로 코드의 `raise HTTPException(...)` 위치를 찾습니다.

## 4. AI에게 보내기 전 정리할 정보

- 실행 위치: `Get-Location`
- Python 경로: `python -c "import sys; print(sys.executable)"`
- 실행 명령
- 기대 결과
- 실제 결과
- 오류 메시지 또는 응답 JSON
- 관련 파일 경로
- 민감 정보 마스킹 여부

## 5. Codex에게 물어보는 형식

```text
아래 오류를 분석해주세요.

실행 위치:
C:\aidev\02_supabase-ai-backend\...

실행 명령:
uvicorn main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn main:app --reload

기대 결과:
Swagger에서 POST /ai/chat이 동작해야 합니다.

실제 결과:
405 Method Not Allowed

요청:
아직 코드를 수정하지 말고, 가능한 원인과 확인 순서를 초보자 기준으로 설명해주세요.
```

## 6. 수정 요청은 두 번째 단계에서

원인 분석이 끝나면 그 다음에 수정 요청을 보냅니다.

```text
위 원인 분석을 바탕으로 최소 범위만 수정해주세요.
관련 없는 리팩토링은 하지 말아주세요.
수정한 파일과 검증 명령을 함께 알려주세요.
```

## 7. 수정 후 검증

- 같은 명령을 다시 실행했는가?
- Swagger에서 같은 endpoint를 다시 호출했는가?
- `python -m pytest tests`가 통과하는가?
- 오류가 바뀌었다면 새 오류를 다시 기록했는가?
- 수정한 내용이 다른 예제를 망가뜨리지 않았는가?
