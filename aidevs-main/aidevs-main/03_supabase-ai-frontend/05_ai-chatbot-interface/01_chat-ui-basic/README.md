# 01_chat-ui-basic

Streamlit의 기본 채팅 UI 컴포넌트를 학습합니다.

이 폴더에서는 먼저 사용자 메시지와 assistant 메시지를 화면에서 구분해 보여 주는 방법을 익힙니다. 아직 실제 AI 호출이나 대화 저장은 중요하지 않습니다. 챗봇 화면의 말풍선 구조와 입력창 흐름을 이해하는 것이 핵심입니다.

## 학습 목표

- `st.chat_message("user")`로 사용자 메시지를 표시할 수 있습니다.
- `st.chat_message("assistant")`로 assistant 응답을 표시할 수 있습니다.
- `st.chat_input`으로 채팅 입력창을 만들 수 있습니다.
- 입력한 텍스트를 화면에 다시 출력할 수 있습니다.

## 예제 파일

```text
01_chat-message-basic.py
02_user-assistant-messages.py
03_chat-input-basic.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\01_chat-ui-basic\01_chat-message-basic.py
```

## 확인할 내용

- user와 assistant 메시지가 구분되어 보이는가?
- `st.chat_input`으로 입력창을 만들 수 있는가?
- 입력한 텍스트를 화면에 다시 출력할 수 있는가?
- 메시지 역할(role)이 화면 표현에 어떤 영향을 주는가?
