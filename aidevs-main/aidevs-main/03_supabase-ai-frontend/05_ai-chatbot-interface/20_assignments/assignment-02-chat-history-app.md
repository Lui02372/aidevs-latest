# Assignment 02: Chat History Preview

## 목표

`st.session_state`를 사용해 현재 화면에서만 유지되는 간단한 대화 이력 미리보기 앱을 만듭니다.

이 과제는 사용자별 저장소나 로그인 연동까지 요구하지 않습니다. 본격적인 로그인 상태와 사용자별 대화 이력 관리는 `04_state-session-and-data`에서 다룹니다.

## 요구사항

- 메시지 목록을 `st.session_state.messages`에 저장합니다.
- 각 메시지는 `role`, `content`를 포함합니다.
- 새 질문을 입력하면 사용자 메시지와 assistant 응답이 목록에 추가됩니다.
- 대화 초기화 버튼을 제공합니다.
- 새로고침 또는 앱 재시작 시 데이터가 사라질 수 있음을 문서에 적습니다.

## 제출 파일 예시

```text
assignment-02-chat-history-preview.py
```
