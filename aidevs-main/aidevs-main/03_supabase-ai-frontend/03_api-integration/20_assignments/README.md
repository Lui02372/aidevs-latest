# 20_assignments

수업 후 제출 과제 안내입니다.

과제는 Streamlit 화면에서 FastAPI 백엔드를 호출하고, 응답 결과를 사용자가 이해하기 쉬운 형태로 표시하는 방식으로 진행합니다.

## 제출 과제

```text
assignment-01-api-health-page.md
assignment-02-message-api-client.md
assignment-03-error-handling-report.md
```

## 제출 기준

- FastAPI 샘플 백엔드를 실행한 뒤 Streamlit 앱에서 호출합니다.
- GET 요청과 POST 요청 중 하나 이상을 사용합니다.
- API 응답 JSON을 화면에 표시합니다.
- 서버 연결 실패 또는 잘못된 응답에 대한 오류 처리를 포함합니다.
- 실행 명령과 확인 결과를 문서에 정리합니다.

## 권장 진행 순서

```text
1. 00_sample_backend를 실행합니다.
2. /health 또는 /docs에서 백엔드가 켜져 있는지 확인합니다.
3. Streamlit 앱에서 API 호출 버튼을 만듭니다.
4. httpx로 API를 호출합니다.
5. status code와 JSON 응답을 확인합니다.
6. 성공/실패 메시지를 화면에 나누어 표시합니다.
```

## 평가 기준

| 항목 | 확인 기준 |
| --- | --- |
| 백엔드 실행 | `00_sample_backend`가 정상 실행됩니다. |
| API 호출 | GET 또는 POST 요청을 Streamlit에서 보낼 수 있습니다. |
| 응답 표시 | JSON 응답 중 필요한 값이 화면에 표시됩니다. |
| 오류 처리 | 서버 연결 실패, timeout, 잘못된 응답을 안내합니다. |
| 결과 정리 | 실행 명령과 테스트 결과가 문서에 정리되어 있습니다. |
