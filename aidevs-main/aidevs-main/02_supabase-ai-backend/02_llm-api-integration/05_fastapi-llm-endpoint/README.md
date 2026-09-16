# 05_fastapi-llm-endpoint

이 단원에서는 FastAPI endpoint에서 LLM 호출 흐름을 연결하는 방법을 학습합니다.

앞 단원까지는 Python 파일에서 싱글턴/멀티턴 호출 구조를 확인했습니다. 이번 단원에서는 프론트엔드나 API client가 `POST /ai/chat`으로 질문을 보내면, FastAPI가 요청을 검증하고 Gemini SDK를 통해 응답을 생성하는 구조를 만듭니다.

## 실행 흐름

| 순서 | 파일 | 역할 |
| --- | --- | --- |
| 1 | `01_mock_llm_endpoint.py` | 실제 API 호출 없이 FastAPI 요청/응답 구조 확인 |
| 2 | `02_gemini_sdk_endpoint_small.py` | 예외 처리 없이 가장 작은 Gemini SDK endpoint 확인 |
| 3 | `03_gemini_sdk_endpoint.py` | key 확인과 오류 안내가 포함된 Gemini SDK endpoint |
| 4 | `04_openai_sdk_endpoint.py` | OpenAI SDK 선택/비교 endpoint |

가상환경은 `02_supabase-ai-backend` 폴더 아래의 `.venv`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
cd .\02_llm-api-integration\05_fastapi-llm-endpoint
uvicorn 01_mock_llm_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 01_mock_llm_endpoint:app --reload
uvicorn 02_gemini_sdk_endpoint_small:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_gemini_sdk_endpoint_small:app --reload
uvicorn 03_gemini_sdk_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 03_gemini_sdk_endpoint:app --reload
uvicorn 04_openai_sdk_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 04_openai_sdk_endpoint:app --reload
```

한 번에 하나의 서버만 실행합니다. 다른 파일을 실행하려면 기존 서버를 `Ctrl + C`로 종료한 뒤 다음 명령을 실행합니다.

## 공통 확인 주소

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

확인할 endpoint:

```text
GET /health
POST /ai/chat
```

## 1. Mock endpoint 실행

```powershell
uvicorn 01_mock_llm_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 01_mock_llm_endpoint:app --reload
```

이 파일은 실제 Gemini 또는 OpenAI API를 호출하지 않습니다.

Swagger UI에서 `POST /ai/chat`을 열고 아래 JSON을 입력합니다.

```json
{
  "message": "FastAPI에서 Pydantic을 왜 사용하나요?",
  "memo_context": "Pydantic은 요청 데이터를 검증하고 응답 모델을 정리합니다.",
  "temperature": 0.3,
  "max_tokens": 300
}
```

`actual_api_called`가 `false`이면 실제 Gemini/OpenAI API를 호출하지 않았다는 의미입니다.

## 2. 가장 작은 Gemini SDK endpoint 실행

```powershell
uvicorn 02_gemini_sdk_endpoint_small:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 02_gemini_sdk_endpoint_small:app --reload
```

이 파일은 예외 처리와 자세한 오류 안내를 일부러 넣지 않습니다. 수강생이 먼저 볼 것은 아래 구조입니다.

```text
1. FastAPI가 POST /ai/chat 요청을 받습니다.
2. Pydantic이 message 필드를 검증합니다.
3. .env에서 GEMINI_API_KEY를 읽습니다.
4. genai.Client를 만듭니다.
5. client.models.generate_content(...)를 호출합니다.
6. response.text를 JSON 응답으로 반환합니다.
```

이 파일은 `GEMINI_API_KEY`가 설정되어 있으면 실제 Gemini API를 호출합니다. 실제 호출 전에는 무료 한도, quota, billing 상태를 확인합니다.

요청 예시:

```json
{
  "message": "FastAPI에서 Pydantic을 왜 사용하나요?"
}
```

## 3. Gemini SDK endpoint 실행

```powershell
uvicorn 03_gemini_sdk_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 03_gemini_sdk_endpoint:app --reload
```

이 파일은 실제 수업 중 사용하기 좋은 안내형 예제입니다.

```text
1. GEMINI_API_KEY가 실제 key인지 확인합니다.
2. google-genai 패키지 설치 여부를 확인합니다.
3. 사용자 질문과 memo_context를 prompt로 구성합니다.
4. Gemini 503, 429, 400/401/403 오류를 이해하기 쉬운 메시지로 반환합니다.
5. provider/model/actual_api_called/answer를 JSON으로 반환합니다.
```

요청 예시:

```json
{
  "message": "FastAPI에서 Pydantic을 왜 사용하나요?",
  "memo_context": "Pydantic은 요청 데이터를 검증합니다.",
  "temperature": 0.3,
  "max_output_tokens": 300
}
```

이 파일은 `GEMINI_API_KEY`가 없거나 placeholder 값이면 실제 API를 호출하지 않고 안내 응답을 반환합니다.

## 4. OpenAI SDK endpoint 선택/비교 실행

OpenAI 예제는 필수가 아닙니다. 모델 공급자별 endpoint 구현 차이를 비교할 때 사용합니다.

```powershell
uvicorn 04_openai_sdk_endpoint:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn 04_openai_sdk_endpoint:app --reload
```

OpenAI API 결제는 ChatGPT/Codex 앱 결제와 별개입니다. 실제 호출 전 OpenAI Platform의 Billing 화면을 확인합니다.

요청 예시:

```json
{
  "message": "FastAPI에서 Pydantic을 왜 사용하나요?",
  "memo_context": "Pydantic은 요청 데이터를 검증합니다.",
  "temperature": 0.3,
  "max_tokens": 300
}
```

## FastAPI endpoint 흐름

```text
사용자 질문 입력
-> POST /ai/chat 요청
-> Pydantic 요청 검증
-> prompt/context 구성
-> Gemini SDK 호출 또는 mock 응답 생성
-> provider/model/actual_api_called/answer 반환
```

## 실제 서비스로 확장할 때 필요한 것

```text
1. 사용자 인증
2. 사용자별 대화 이력 조회
3. Supabase에 질문/응답 저장
4. 서비스 로그 저장
5. API 호출 실패 처리
6. 호출 제한과 비용 관리
7. SSE 기반 실시간 응답 스트리밍
```

SSE 기반 AI 응답 스트리밍은 `04_supabase-ai-mini-project`에서 백엔드, Streamlit 화면, Supabase 저장 흐름과 함께 통합 실습으로 다룹니다.

## 이후 단원과의 연결

```text
03_supabase-db-and-auth:
  사용자 정보와 대화 이력을 Supabase에 저장합니다.

90_ai-assisted-code-review-and-debugging:
  LLM endpoint 실행 오류, API key 오류, 응답 형식 문제를 점검합니다.

99_final-backend-project:
  FastAPI, LLM 호출, Supabase 저장을 작은 최종 프로젝트로 정리합니다.

03_supabase-ai-frontend:
  Streamlit 화면에서 /ai/chat endpoint를 호출합니다.

04_supabase-ai-mini-project:
  실시간 스트리밍, 로그 저장, 배포까지 연결합니다.
```

## 확인 질문

```text
1. FastAPI endpoint에서 LLM API를 직접 호출할 때 왜 요청 검증이 필요한가요?
2. actual_api_called 값을 응답에 포함하면 어떤 점이 좋나요?
3. mock endpoint를 먼저 만드는 이유는 무엇인가요?
4. Gemini SDK endpoint를 프로젝트 기본 구현으로 두는 이유는 무엇인가요?
5. 작은 Gemini SDK endpoint와 안내형 Gemini SDK endpoint는 어떤 차이가 있나요?
```
