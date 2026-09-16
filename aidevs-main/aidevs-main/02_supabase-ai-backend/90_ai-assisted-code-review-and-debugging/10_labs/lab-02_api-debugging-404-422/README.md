# Lab 02. FastAPI 404, 405, 422

## 목표

FastAPI에서 자주 만나는 API 호출 오류를 구분합니다.

- 404: 없는 URL
- 405: URL은 있지만 HTTP Method가 다름
- 422: 요청 Body가 Pydantic 모델과 맞지 않음

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\90_ai-assisted-code-review-and-debugging\10_labs\lab-02_api-debugging-404-422
..\..\..\.venv\Scripts\Activate.ps1
python -m uvicorn broken_api:app --reload --host 127.0.0.1 --port 8092
```

Swagger:

```text
http://127.0.0.1:8092/docs
```

## 일부러 확인할 오류

```text
GET  /ai/chat      -> 405
POST /ai/missing   -> 404
POST /ai/chat {"message": ""} -> 422
POST /ai/chat {"text": "hello"} -> 422
```

## 1차 프롬프트

```text
FastAPI에서 404/405/422 오류가 나왔습니다.
아래 실행 명령, URL, Method, 요청 Body를 보고 어떤 오류인지 구분해주세요.
아직 코드는 수정하지 말고 Swagger에서 어떻게 다시 호출해야 하는지 알려주세요.
```

## 2차 프롬프트

```text
이 API가 초보자에게 더 이해하기 쉬운 오류 메시지를 주도록 최소 수정 계획을 세워주세요.
Pydantic 모델과 endpoint 경로를 기준으로 설명해주세요.
```
