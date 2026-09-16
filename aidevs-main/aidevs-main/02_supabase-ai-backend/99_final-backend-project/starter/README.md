# Starter

최종 프로젝트를 시작할 때 사용할 수 있는 최소 FastAPI 예제입니다.

## 실행 방법

```powershell
cd C:\aidev\02_supabase-ai-backend\99_final-backend-project\starter
uvicorn app.main:app --reload
# 위 명령에서 오류가 나면 아래처럼 실행합니다.
python -m uvicorn app.main:app --reload
```

브라우저에서 확인합니다.

```text
http://127.0.0.1:8000/docs
```

이 starter는 `GET /health`만 제공합니다. 프로젝트 주제에 맞게 endpoint를 하나씩 추가합니다.
