# 04. Prompt-driven UI Development

이 문서는 프롬프트만으로 작은 Streamlit UI를 단계적으로 만드는 전략을 설명합니다.

핵심은 "Streamlit으로 멋진 챗봇 앱을 전부 만들어줘"가 아닙니다. 화면 목적, 사용자 흐름, mock 데이터, 상태 관리, API 연결, 오류 처리, UI 리뷰를 나누어 요청합니다.

## 나쁜 방식

```text
Streamlit으로 로그인, 챗봇, 대시보드, 배포까지 되는 앱을 만들어줘.
```

이 방식은 파일이 한 번에 커지고, 화면이 깨지거나 API 연결이 실패했을 때 어디서부터 고쳐야 할지 알기 어렵습니다.

## 좋은 방식

```text
화면 목적 정의
-> 사용자 흐름
-> 화면 구성
-> mock 데이터 UI
-> session_state
-> API 연결
-> 오류/로딩/빈 상태
-> UI 리뷰
-> README 작성
```

## 예제 주제: 학습 상담 챗봇 UI

처음에는 백엔드를 붙이지 않고 mock 응답으로 시작합니다.

필수 화면:

```text
로그인 상태 표시
질문 입력
응답 표시
대화 이력
오류 메시지 영역
```

선택 확장:

```text
백엔드 /api/chat 연결
Authorization header 전달
대화 이력 조회
서비스 로그 대시보드
Streamlit Community Cloud 배포
```

## Step 1. 화면 목적과 사용자 흐름 정리

```text
학습 상담 챗봇 UI를 만들고 싶습니다.
아직 코드는 작성하지 말고, 사용자가 화면에서 어떤 순서로 행동하는지 5단계 이하로 정리해주세요.
초보자 수업용이므로 기능은 너무 많이 넣지 말아주세요.
```

## Step 2. 화면 구성 제안

```text
위 사용자 흐름을 Streamlit 화면으로 만들려고 합니다.
필요한 영역을 title, sidebar, input, button, message area 정도로 나누어 제안해주세요.
아직 코드는 작성하지 말아주세요.
```

## Step 3. mock 데이터 UI 먼저 만들기

```text
백엔드 API 없이 mock 응답만 사용해서 Streamlit 챗봇 UI를 만들어주세요.
파일 하나로 작성하고, 실행 명령도 함께 알려주세요.
session_state는 아직 최소한으로만 사용해주세요.
```

## Step 4. session_state로 대화 이력 유지

```text
현재 Streamlit 챗봇 UI에 st.session_state를 추가해서 대화 이력이 화면 재실행 후에도 유지되게 해주세요.
새 기능 추가는 하지 말고 messages 리스트 초기화와 메시지 추가 흐름만 정리해주세요.
```

## Step 5. API 연결 붙이기

```text
mock 응답 대신 FastAPI 백엔드의 POST /api/chat을 호출하도록 바꾸고 싶습니다.
API_BASE_URL은 코드 상단 변수로 두고, timeout과 status code 오류 처리를 포함해주세요.
실제 API key는 프론트엔드에 넣지 않는다는 주석도 추가해주세요.
```

## Step 6. 로그인 token 연결

```text
로그인 후 받은 access_token을 st.session_state에 저장하고,
백엔드 호출 시 Authorization: Bearer token header를 보내는 흐름을 추가해주세요.
token 원문을 화면에 계속 노출하지 말고 로그인 여부만 표시해주세요.
```

## Step 7. 로딩, 빈 상태, 오류 상태 추가

```text
이 Streamlit 화면을 사용자 관점에서 개선해주세요.
확인할 것:
1. 응답 생성 중 로딩 표시가 있는가?
2. 대화가 없을 때 빈 상태 안내가 있는가?
3. API 실패 시 사용자가 이해할 수 있는 메시지가 있는가?
4. 버튼 중복 클릭을 줄일 수 있는가?
```

## Step 8. UI 리뷰와 제출 전 점검

```text
이 Streamlit 앱을 제출 전 리뷰해주세요.
화면 흐름, 상태 관리, API 연결, 오류 처리, 보안 키 노출, README 실행 가이드 기준으로 문제를 찾아주세요.
아직 파일은 수정하지 말고 우선순위가 높은 수정 사항부터 알려주세요.
```

## 운영 원칙

- 한 프롬프트에는 한 목표만 담습니다.
- 계획을 먼저 받고, 코드는 그 다음에 요청합니다.
- mock UI로 먼저 실행되게 만듭니다.
- API 연결과 인증 token은 나중에 붙입니다.
- 프론트엔드에는 `SUPABASE_SERVICE_ROLE_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`를 넣지 않습니다.
- 수정 후에는 항상 Streamlit 실행 명령과 확인 버튼 순서를 확인합니다.
