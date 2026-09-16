# 03. Prompt Recipes

Codex에게 요청할 때는 파일, 실행 명령, 기대 결과, 실제 결과를 함께 전달합니다.

## Streamlit 오류 분석

```text
아래 Streamlit 오류를 분석해주세요.

파일:
C:\aidev\03_supabase-ai-frontend\...

실행 명령:
streamlit run ...

오류 메시지:
...

요청:
1. 가능한 원인을 우선순위로 정리해주세요.
2. 확인 명령을 알려주세요.
3. 아직 파일은 수정하지 말아주세요.
```

## API 연결 리뷰

```text
이 Streamlit 파일의 API 호출 흐름을 리뷰해주세요.

리뷰 관점:
1. API_BASE_URL 사용이 적절한가?
2. 백엔드 연결 실패 처리가 있는가?
3. timeout과 status code 처리가 있는가?
4. token이나 API key가 화면 또는 로그에 노출되지 않는가?

아직 코드는 수정하지 말고 문제점만 알려주세요.
```

## 최종 프로젝트 점검

```text
99_final-frontend-project 제출 전 점검을 해주세요.

확인할 것:
1. Streamlit 앱이 실행되는지
2. API_BASE_URL로 백엔드를 호출하는지
3. 챗봇 UI와 대화 이력/로그 조회 화면이 있는지
4. 로딩/오류 상태가 표시되는지
5. 프론트엔드에 service role key나 LLM API key가 없는지

누락된 항목을 먼저 알려주세요.
```
