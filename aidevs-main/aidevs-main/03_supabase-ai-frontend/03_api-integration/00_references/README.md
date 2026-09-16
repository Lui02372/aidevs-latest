# 00_references

`03_api-integration`을 진행하기 전에 읽는 참고 자료입니다.

이 폴더는 Streamlit 프론트엔드가 FastAPI 백엔드와 통신할 때 필요한 핵심 개념을 정리합니다. API 호출 자체는 어렵지 않지만, 주소, method, JSON key, status code 중 하나만 어긋나도 화면에서 오류가 발생할 수 있습니다.

## 문서 목록

```text
api-integration-notes.md
```

## 먼저 확인할 내용

- Streamlit은 화면과 사용자 입력을 담당합니다.
- FastAPI는 요청을 받고 JSON 응답을 반환합니다.
- `GET`은 주로 조회, `POST`는 주로 데이터 전송에 사용합니다.
- JSON key 이름은 백엔드가 기대하는 Pydantic 모델과 맞아야 합니다.
- 서버가 꺼져 있거나 주소가 틀리면 프론트엔드에서 연결 오류가 발생합니다.

## 확인 질문

```text
프론트엔드와 백엔드는 어떤 주소로 연결되나요?
GET과 POST는 언제 다르게 사용하나요?
status code 200은 무엇을 의미하나요?
JSON 응답에서 필요한 key가 없으면 화면에서는 어떻게 처리해야 하나요?
```
