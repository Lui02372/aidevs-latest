# 04_multi-turn-call

이 단원에서는 **멀티턴 LLM 호출**을 학습합니다.

멀티턴 호출은 이전 대화 이력을 함께 보내서 모델이 문맥을 이어서 답변하도록 만드는 방식입니다. 중요한 점은 모델이 우리 서비스의 대화를 자동으로 기억하는 것이 아니라, 코드에서 이전 `user`/`assistant` 또는 `user`/`model` 메시지를 다시 넣어 보내야 한다는 것입니다.

## 핵심 요약

```text
싱글턴 호출:
  현재 질문 1개만 모델에 보냅니다.

멀티턴 호출:
  이전 질문과 답변을 messages 또는 contents 목록에 함께 넣어 보냅니다.

대화 메모리:
  사용자의 이전 질문과 AI 답변을 저장하고 다시 불러오는 구조입니다.

Gemini SDK 중심 구조:
  실제 프로젝트에서는 SDK 방식으로 먼저 구현합니다.
```

## 실행 흐름

| 순서 | 파일 | 역할 |
| --- | --- | --- |
| 1 | `01_mock_multi_turn.py` | 실제 API 호출 없이 멀티턴 messages 구조 확인 |
| 2 | `02_gemini_sdk_multi_turn_small.py` | 예외 처리 없이 가장 작은 Gemini SDK 멀티턴 호출 확인 |
| 3 | `03_gemini_sdk_multi_turn.py` | key 확인과 오류 안내가 포함된 Gemini SDK 멀티턴 호출 |
| 4 | `04_openai_sdk_multi_turn.py` | OpenAI SDK 선택/비교 실습 |

가상환경은 `02_supabase-ai-backend` 폴더 아래의 `.venv`를 사용합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\04_multi-turn-call\01_mock_multi_turn.py
python .\02_llm-api-integration\04_multi-turn-call\02_gemini_sdk_multi_turn_small.py
python .\02_llm-api-integration\04_multi-turn-call\03_gemini_sdk_multi_turn.py
python .\02_llm-api-integration\04_multi-turn-call\04_openai_sdk_multi_turn.py
```

처음에는 `01_mock_multi_turn.py`로 비용 없이 구조를 확인합니다. 실제 Gemini API 호출은 `02_gemini_sdk_multi_turn_small.py`에서 가장 작은 코드로 먼저 보고, 오류 처리와 안전장치는 `03_gemini_sdk_multi_turn.py`에서 확인합니다. OpenAI SDK 예제는 선택/비교 실습입니다.

## 1. Mock 멀티턴 실행

```powershell
python .\02_llm-api-integration\04_multi-turn-call\01_mock_multi_turn.py
```

이 예제는 `messages` 목록에 이전 대화를 직접 넣어 보내는 구조를 보여줍니다.

```text
system
user
assistant
user
```

모델은 이 목록을 보고 마지막 질문이 무엇을 이어서 묻는지 추론합니다.

## 2. 가장 작은 Gemini SDK 멀티턴 호출

```powershell
python .\02_llm-api-integration\04_multi-turn-call\02_gemini_sdk_multi_turn_small.py
```

이 파일은 예외 처리와 자세한 오류 안내를 일부러 넣지 않습니다. 수강생이 먼저 볼 것은 아래 구조입니다.

```text
1. .env에서 GEMINI_API_KEY를 읽습니다.
2. genai.Client를 만듭니다.
3. 이전 user/model 메시지를 contents 목록으로 만듭니다.
4. client.models.generate_content(...)를 호출합니다.
5. response.text를 출력합니다.
```

## 3. Gemini SDK 멀티턴 호출

```powershell
python .\02_llm-api-integration\04_multi-turn-call\03_gemini_sdk_multi_turn.py
```

이 파일은 실제 수업 중 사용하기 좋은 안내형 예제입니다.

```text
1. GEMINI_API_KEY가 실제 key인지 확인합니다.
2. google-genai 패키지 설치 여부를 확인합니다.
3. Gemini 503, 429, 400/401/403 오류를 이해하기 쉬운 메시지로 출력합니다.
4. 이전 대화가 포함된 contents를 Gemini SDK로 보냅니다.
```

Gemini에서는 이전 AI 답변을 `role: "model"`로 표현합니다. OpenAI의 `role: "assistant"`와 비슷한 역할입니다.

## 4. OpenAI SDK 선택/비교 멀티턴 호출

OpenAI 예제는 필수가 아닙니다. 모델 공급자별 메시지 구조 차이를 비교할 때 사용합니다.

```powershell
python .\02_llm-api-integration\04_multi-turn-call\04_openai_sdk_multi_turn.py
```

OpenAI API 결제는 ChatGPT/Codex 앱 결제와 별개입니다. 실제 호출 전 OpenAI Platform의 Billing 화면을 확인합니다.

## 멀티턴 호출 흐름

```text
사용자 질문 입력
-> 이전 대화 이력 조회
-> system/user/assistant 또는 user/model 메시지 목록 구성
-> 최신 user 메시지 추가
-> Gemini SDK 호출
-> assistant 응답 저장
-> 응답 반환
```

## 대화 이력은 어디에 저장하나요?

이 단원에서는 Python 코드 안의 목록으로 대화 이력을 표현합니다. 실제 서비스에서는 이 구조가 다음처럼 확장됩니다.

```text
메모리 리스트
-> Supabase conversations/messages 테이블
-> 사용자별 대화 이력 조회
-> 최근 메시지 또는 요약 메시지 구성
-> Gemini SDK 호출
```

## 멀티턴 호출이 필요한 경우

```text
1. 이어지는 질문에 답해야 할 때
2. 사용자가 "그 내용", "방금 말한 것"처럼 문맥을 참조할 때
3. 사용자별 대화 흐름을 유지해야 할 때
4. 이전 답변을 바탕으로 추가 설명이나 수정 요청을 받을 때
```

## 주의할 점

```text
1. 대화가 길어질수록 입력 토큰이 늘어납니다.
2. 비용과 응답 시간이 증가할 수 있습니다.
3. 오래된 메시지를 모두 보내는 것이 항상 좋은 것은 아닙니다.
4. 필요한 경우 최근 메시지만 보내거나 요약본을 만들어야 합니다.
5. 실제 서비스에서는 사용자별로 대화 이력을 구분해야 합니다.
```

## 이후 단원과의 연결

```text
05_fastapi-llm-endpoint:
  FastAPI endpoint에서 사용자 질문과 대화 이력을 받아 Gemini SDK로 LLM API를 호출합니다.

03_supabase-db-and-auth:
  대화 이력을 Supabase에 저장하고 사용자별로 조회합니다.

03_supabase-ai-frontend:
  Streamlit 화면에서 이전 대화를 보여주고 새 질문을 입력받습니다.

04_supabase-ai-mini-project:
  SSE 스트리밍, Supabase 저장, 대화 이력 조회를 통합합니다.
```

## 확인 질문

```text
1. 멀티턴 호출은 모델이 자동으로 기억하는 방식인가요?
2. 이전 assistant/model 답변을 다시 보내야 하는 이유는 무엇인가요?
3. 대화가 길어지면 왜 최근 메시지만 자르거나 요약해야 하나요?
4. Gemini의 role="model"과 OpenAI의 role="assistant"는 어떤 관계인가요?
5. 이후 프로젝트에서 Gemini SDK 방식을 기본으로 사용하는 이유는 무엇인가요?
```
