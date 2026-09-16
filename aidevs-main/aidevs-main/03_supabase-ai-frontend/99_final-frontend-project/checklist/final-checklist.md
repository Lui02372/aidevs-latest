# Final Checklist

이 문서는 `99_final-frontend-project`를 완성한 뒤 스스로 확인하는 체크리스트입니다.

기본 제출 기준은 `backend_mock`과 Streamlit solution 연결입니다. Streamlit solution은 탭 구조인 `solution_tabs` 또는 멀티페이지 구조인 `solution_multipage` 중 하나를 선택해 사용합니다. `backend_service`, Render, Upstash, Streamlit Community Cloud 배포는 선택/심화 기준입니다.

## 필수 완성 체크

- [ ] `backend_mock`을 실행했다.
- [ ] Streamlit `solution_tabs` 또는 `solution_multipage`를 실행했다.
- [ ] Streamlit 화면에서 `/health` 연결 확인에 성공했다.
- [ ] 회원가입 폼에서 `/auth/signup`을 호출했다.
- [ ] 회원가입 성공/실패 메시지를 화면에 표시했다.
- [ ] 로그인 폼에서 `/auth/signin`을 호출했다.
- [ ] 로그인 성공 후 `st.session_state["access_token"]`에 token을 저장했다.
- [ ] 로그인 성공 후 `st.session_state["current_user"]`에 사용자 정보를 저장했다.
- [ ] 보호 API 호출 시 `Authorization: Bearer ...` header를 보냈다.
- [ ] 로그아웃 시 token, 사용자 정보, 현재 대화 상태를 정리했다.
- [ ] 챗봇 화면에서 사용자 메시지와 assistant 응답을 구분해 표시했다.
- [ ] 응답 생성 중 `st.spinner`, `st.status`, `st.empty` 중 하나로 대기 상태를 표시했다.
- [ ] 대화 기록 화면에서 `/conversations` 응답을 화면에 표시했다.
- [ ] 서비스 로그 화면에서 `/service-logs` 응답을 표로 표시했다.
- [ ] backend 연결 실패, 로그인 실패, API 오류를 `st.error` 또는 `st.warning`으로 표시했다.

## 보안 체크

- [ ] 프론트엔드 코드에 `SUPABASE_SERVICE_ROLE_KEY`가 없다.
- [ ] 프론트엔드 코드에 `GEMINI_API_KEY` 또는 `OPENAI_API_KEY`가 없다.
- [ ] 프론트엔드 코드에 `UPSTASH_REDIS_REST_TOKEN`이 없다.
- [ ] `.env` 파일을 GitHub에 올리지 않는다.
- [ ] token 전체를 화면, 캡처, 제출 문서에 노출하지 않는다.

## 선택/심화 체크

- [ ] `backend_service`를 로컬에서 실행했다.
- [ ] Supabase SQL Editor에서 `backend_service/schema.sql`을 실행했다.
- [ ] Supabase Auth 회원가입/로그인을 확인했다.
- [ ] Gemini API 호출을 확인했다.
- [ ] 선택 사항으로 Upstash Redis 캐시를 연결했다.
- [ ] 같은 Streamlit `solution_tabs` 또는 `solution_multipage`를 `backend_service`의 `API_BASE_URL`로 연결했다.
- [ ] Render에 `backend_service`를 배포했다.
- [ ] Streamlit Community Cloud에 `solution_tabs` 또는 `solution_multipage`를 배포했다.
- [ ] Streamlit Secrets에는 `API_BASE_URL`만 등록했다.
- [ ] Render 환경변수에 Supabase/Gemini/Upstash key를 등록했다.

## 제출 전 확인

- [ ] 실행 화면 캡처를 준비했다.
- [ ] 회원가입/로그인 화면 캡처를 준비했다.
- [ ] 챗봇 질문/응답 화면 캡처를 준비했다.
- [ ] 대화 기록 화면 캡처를 준비했다.
- [ ] 서비스 로그 화면 캡처를 준비했다.
- [ ] 배포를 진행했다면 Streamlit URL과 Render `/health` URL을 정리했다.
