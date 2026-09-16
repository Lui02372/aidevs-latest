# State Session Notes

## 핵심 개념

Streamlit은 사용자가 입력하거나 버튼을 누를 때마다 스크립트를 다시 실행합니다. 따라서 화면에서 계속 유지해야 하는 값은 `st.session_state`에 저장합니다.

## 이 단원의 상태 종류

- UI 상태: 입력값, 선택값, 버튼 결과
- 로그인 상태: 사용자 이름, access token, 로그인 여부
- 데이터 상태: 사용자별 조회 결과, 대화 이력
- 캐시 상태: 반복 호출 결과

## 04 단원과 05 단원의 차이

`05_ai-chatbot-interface`에서는 챗봇 화면을 먼저 만들고, mock 응답과 간단한 대화 이력 미리보기를 확인합니다.

`04_state-session-and-data`에서는 같은 화면 흐름을 실제 서비스 상태 관리로 확장합니다. 로그인 token을 저장하고, Authorization header를 붙여 백엔드 API를 호출하고, 사용자별 대화 이력과 서비스 로그를 조회합니다.

## 인증 연동 흐름

```text
로그인 폼 입력
-> FastAPI 로그인 API 호출
-> access token 응답 수신
-> st.session_state에 token 저장
-> Authorization header로 보호된 API 호출
-> 로그아웃 시 token 삭제
```

## 보안 기준

- Supabase service role key는 프론트엔드에 두지 않습니다.
- Gemini API key는 실제 서비스 구조에서 백엔드에 둡니다.
- Streamlit은 백엔드 API 주소인 `API_BASE_URL`을 통해서만 데이터를 요청합니다.

