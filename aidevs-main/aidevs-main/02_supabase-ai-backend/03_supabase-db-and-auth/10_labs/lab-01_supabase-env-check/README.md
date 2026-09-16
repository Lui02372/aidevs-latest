# Lab 01 - Supabase 환경변수 확인

이 실습은 Supabase에 접속하기 전에 `.env` 파일이 제대로 준비되어 있는지 확인합니다.

## 학습 목표

- `.env` 파일의 역할을 설명할 수 있습니다.
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`의 차이를 구분할 수 있습니다.
- 실제 키 값을 화면에 그대로 출력하면 안 되는 이유를 이해합니다.

## 실행 방법

백엔드 과정 루트에서 실행합니다.

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\03_supabase-db-and-auth\10_labs\lab-01_supabase-env-check\solution.py
```

## 확인 기준

- 필수 환경변수가 모두 `설정됨`으로 표시됩니다.
- 키 전체가 출력되지 않고 앞뒤 일부만 마스킹되어 표시됩니다.
- placeholder 값이 들어 있으면 실제 Supabase Dashboard에서 발급받은 값으로 바꿉니다.

## 정리 질문

- `anon key`는 어떤 상황에서 사용할 수 있나요?
- `service role key`를 프론트엔드 코드에 넣으면 왜 위험한가요?
- `.env` 파일을 GitHub에 올리면 안 되는 이유는 무엇인가요?
