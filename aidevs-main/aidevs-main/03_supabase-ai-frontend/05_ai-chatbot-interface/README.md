# 05_ai-chatbot-interface

Streamlit으로 AI 챗봇 화면을 구성하는 단원입니다.

이 단원에서는 챗봇 화면의 기본 구조를 먼저 만듭니다. 기본 실습은 비용이 들지 않는 mock 응답으로 진행합니다. 프론트엔드에서 Gemini/OpenAI API를 직접 호출하지 않고, 실제 LLM 호출은 FastAPI 백엔드를 통해 처리한다는 기준을 유지합니다.

중요한 기준은 다음과 같습니다.

```text
04_state-session-and-data
-> session_state 본격 학습
-> 로그인 상태
-> 사용자별 대화 이력
-> 서비스 로그와 데이터 관리

05_ai-chatbot-interface
-> mock 챗봇 UI 중심
-> 백엔드 mock chat API 호출
-> 백엔드 Gemini chat API 선택 호출
-> 대화 이력 누적 화면 맛보기
```

즉, 이 단원은 “챗봇 화면을 어떻게 만들고 응답을 어떻게 보여 줄 것인가”에 집중합니다. 대화 저장, 사용자별 이력 조회, Supabase 저장, SSE 스트리밍은 뒤 과정에서 더 깊게 다룹니다.

## 학습 목표

- Streamlit의 chat UI 컴포넌트를 사용할 수 있습니다.
- 사용자 메시지와 assistant 응답을 구분해 출력할 수 있습니다.
- 프롬프트 입력값을 검증하고 mock 응답 화면을 만들 수 있습니다.
- 응답 생성 함수를 화면 코드와 분리할 수 있습니다.
- 백엔드 mock chat API 응답을 챗봇 메시지로 표시할 수 있습니다.
- 간단한 대화 이력을 `st.session_state`에 누적해 화면에 표시할 수 있습니다.
- 실제 서비스에서는 LLM API key를 프론트엔드에 두지 않고 백엔드 API를 호출해야 함을 설명할 수 있습니다.

## 학습 순서

```text
01_chat-ui-basic
-> 02_prompt-input-and-response
-> 03_conversation-history-preview
-> 04_mock-and-optional-gemini-interface
-> 10_labs
-> 20_assignments
```

## 폴더 구성

```text
05_ai-chatbot-interface
├─ README.md
├─ 00_references
├─ 00_sample_backend
├─ 01_chat-ui-basic
├─ 02_prompt-input-and-response
├─ 03_conversation-history-preview
├─ 04_mock-and-optional-gemini-interface
├─ 10_labs
└─ 20_assignments
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\01_chat-ui-basic\01_chat-message-basic.py
```

## 챗봇 샘플 백엔드 실행

`04_mock-and-optional-gemini-interface`의 백엔드 호출 예제는 챗봇 전용 샘플 백엔드를 먼저 실행합니다.

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
cd .\05_ai-chatbot-interface\00_sample_backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Gemini 실제 호출을 확인하려면 이 백엔드 폴더 안의 `.env`에 `GEMINI_API_KEY`를 설정합니다. 프론트엔드 최상위 `.env`에는 Gemini key를 넣지 않습니다.

## 대화 이력 누적 예제

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\05_chat-history-session.py
```

백엔드 Gemini 응답을 대화 이력으로 누적하는 선택 예제는 다음과 같습니다.

```powershell
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\07_backend-gemini-chat-history.py
```

최근 대화 이력 6개 메시지를 백엔드로 함께 보내 문맥을 이어가는 선택 예제는 다음과 같습니다.

```powershell
streamlit run .\05_ai-chatbot-interface\04_mock-and-optional-gemini-interface\08_backend-gemini-chat-with-history.py
```

## 실행 확인 기준

- 사용자와 assistant 메시지가 서로 다른 역할로 표시됩니다.
- 입력창에 질문을 넣으면 mock 응답이 화면에 표시됩니다.
- 응답 생성 함수가 화면 코드와 분리되어 있습니다.
- 여러 번 질문을 입력해도 이전 대화가 화면에 계속 출력됩니다.
- 선택 실습에서 백엔드 Gemini 응답을 대화 이력으로 누적할 수 있습니다.
- 선택 실습에서 최근 대화 일부를 백엔드로 함께 보내 문맥을 이어갈 수 있습니다.
- 실제 서비스에서는 프론트엔드가 Gemini/OpenAI API key를 직접 가지지 않는다는 기준을 설명할 수 있습니다.

## 필수와 선택 기준

| 구분 | 내용 |
| --- | --- |
| 필수 | chat UI, 프롬프트 입력, mock 응답, 간단한 대화 미리보기, 백엔드 mock chat API 호출 구조 |
| 선택 | 응답 표시 세부 디자인, 백엔드 Gemini chat API 호출 |
| 제외 | 대화 영구 저장, 사용자별 이력 관리, SSE 스트리밍 |

## 이전 단원 연결

`04_state-session-and-data`에서 배운 `st.session_state`, token 저장, Authorization header, 사용자별 데이터 조회 흐름은 이 단원의 챗봇 화면에서도 계속 활용합니다. 이 단원에서는 그 상태 관리 기반 위에 chat UI와 백엔드 chat API 연결을 얹는다고 보면 됩니다.

SSE 기반 실시간 응답 스트리밍은 백엔드 SSE 엔드포인트, Streamlit 표시, Supabase 최종 메시지 저장이 함께 필요하므로 `04_supabase-ai-mini-project`에서 통합 실습으로 다룹니다.
