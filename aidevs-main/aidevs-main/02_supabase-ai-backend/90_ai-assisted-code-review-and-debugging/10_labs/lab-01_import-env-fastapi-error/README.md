# Lab 01. import, venv, .env 오류

## 목표

실행 환경 문제를 Codex에게 정확히 설명하는 연습을 합니다.

이 lab의 `broken_app.py`는 의도적으로 다음 문제가 섞여 있습니다.

- 존재하지 않는 패키지 import
- `.env` 위치 확인 필요
- `DEMO_API_KEY`가 없거나 예시값이면 오류

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend\90_ai-assisted-code-review-and-debugging\10_labs\lab-01_import-env-fastapi-error
..\..\..\.venv\Scripts\Activate.ps1
python .\broken_app.py
```

## 1차 프롬프트

```text
아래 Python 실행 오류를 분석해주세요.
아직 코드를 수정하지 말고 원인과 확인 순서만 알려주세요.

파일:
C:\aidev\02_supabase-ai-backend\90_ai-assisted-code-review-and-debugging\10_labs\lab-01_import-env-fastapi-error\broken_app.py

실행 명령:
python .\broken_app.py

오류 메시지:
여기에 Traceback을 붙여 넣습니다.

확인하고 싶은 것:
1. 가상환경 문제인지
2. import 문제인지
3. .env 문제인지
4. 어떤 명령으로 확인해야 하는지
```

## 2차 프롬프트

```text
위 원인 분석을 바탕으로 최소 수정 방향을 제안해주세요.
관련 없는 기능 추가는 하지 말고, 실행 가능한 상태로 만들기 위한 수정만 알려주세요.
```

## 기록

`templates/ai-debugging-session-template.md`에 실행 명령, 오류, 프롬프트, 수정 결과를 기록합니다.
