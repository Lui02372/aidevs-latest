# 03_conversation-history-preview

`st.session_state`를 사용해 간단한 대화 이력 맛보기를 진행합니다.

이 폴더는 대화 이력을 본격적으로 설계하는 단원이 아닙니다. 챗봇 UI에서 메시지가 한 번만 보이고 사라지면 불편하다는 점을 확인하고, `session_state`로 메시지 목록을 잠시 유지할 수 있다는 감각을 익히는 단계입니다.

사용자별 대화 이력, 로그인 상태, Supabase 저장, 서비스 로그는 `04_state-session-and-data`에서 본격적으로 다룹니다.

## 학습 목표

- 메시지 목록에 `role`, `content`를 저장할 수 있습니다.
- 화면이 다시 실행되어도 메시지 목록이 유지되는 흐름을 확인할 수 있습니다.
- 대화 초기화 버튼을 만들 수 있습니다.
- 메시지에 간단한 metadata를 붙일 수 있습니다.

## 예제 파일

```text
01_session-message-list.py
02_append-chat-history.py
03_clear-chat-history.py
04_chat-history-with-metadata.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\03_conversation-history-preview\02_append-chat-history.py
```

## 확인할 내용

- 새 질문을 입력해도 이전 메시지가 유지되는가?
- 메시지 목록에 role과 content가 저장되는가?
- 대화 초기화 버튼이 정상 동작하는가?
- 이 구조를 사용자별 저장소로 확장하려면 어떤 정보가 더 필요한가?
