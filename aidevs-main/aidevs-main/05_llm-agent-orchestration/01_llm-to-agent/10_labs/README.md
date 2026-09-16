# 01 Labs

## 실행 위치

Lab 1~2의 판단 연습은 Backend 없이 진행합니다. 실제 GPT·Gemini·Ollama 호출이나
완성 화면을 확인할 때는 `mini_agent_01_llm`의 Backend를 먼저 실행합니다.

```powershell
cd C:\mini_agent_st\mini_agent_01_llm\backend
uvicorn app.main:app --reload --port 8000
```

그다음 과정 폴더에서 `04_real_provider_call.py`를 실행하거나 새 터미널에서
`C:\mini_agent_st\mini_agent_01_llm\frontend`의 Streamlit 앱을 실행합니다.

## Lab 1. 점심 문의 분류

`recommendation`, `budget`, `allergy`, `needs_clarification`으로 요청을 분류합니다.

## Lab 2. 낮은 confidence 처리

confidence가 `0.6`보다 낮으면 답변하지 않고 추가 질문을 생성합니다.

## 기록

- 고정 규칙으로 충분했던 입력
- 의미 판단이 필요했던 입력
- 잘못 분류된 입력과 개선 방법
