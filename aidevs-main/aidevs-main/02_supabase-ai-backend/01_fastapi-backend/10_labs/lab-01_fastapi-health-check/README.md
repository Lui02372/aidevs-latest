# Lab 01 - FastAPI Health Check

## 목표

FastAPI 앱을 만들고 기본 상태 확인 API를 구현합니다.

## 요구사항

1. `FastAPI()` 앱을 생성합니다.
2. `GET /`에서 환영 메시지를 반환합니다.
3. `GET /health`에서 서버 상태를 반환합니다.
4. Swagger UI에서 두 API를 직접 실행합니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\01_fastapi-backend\10_labs\lab-01_fastapi-health-check
uvicorn starter:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn starter:app --reload
```

정답 확인:

```powershell
uvicorn solution:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn solution:app --reload
```

## 확인 질문

```text
1. FastAPI 앱 객체 이름은 왜 app으로 자주 쓰나요?
2. /health API는 실제 서비스에서 어떤 용도로 쓰이나요?
3. Swagger UI는 어떤 주소에서 확인하나요?
```
