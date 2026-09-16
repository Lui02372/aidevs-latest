# Assignment 01 - Supabase 프로젝트와 환경변수 준비 보고서

Supabase 프로젝트를 만들고, FastAPI에서 사용할 환경변수를 안전하게 준비하는 과제입니다.

## 목표

- Supabase 프로젝트 생성 과정을 설명할 수 있습니다.
- `.env` 파일에 들어가는 값의 의미를 구분할 수 있습니다.
- key를 안전하게 관리해야 하는 이유를 설명할 수 있습니다.

## 제출물

Markdown 문서로 아래 내용을 작성합니다.

```text
1. Supabase 프로젝트 준비 여부
2. 생성한 테이블 또는 앞으로 생성할 테이블 목록
3. .env에 필요한 환경변수 이름
4. SUPABASE_URL의 역할
5. SUPABASE_ANON_KEY의 역할
6. SUPABASE_SERVICE_ROLE_KEY의 역할
7. 실제 key 값을 제출하지 않았다는 확인 문장
8. `.env` 파일 준비 여부와 실제 key 값을 제출하지 않았다는 확인 문장
```

## 실행 참고

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
dir .env
```

`.env` 파일은 직접 제출하지 않습니다. 문서에는 변수 이름과 역할만 작성하고 실제 key 값은 적지 않습니다.

## 확인 기준

- 실제 key 값이 문서에 포함되어 있지 않습니다.
- `anon key`와 `service role key`의 차이를 설명했습니다.
- service role key를 프론트엔드에 넣으면 안 되는 이유를 설명했습니다.

## 제출 전 점검

- `.env` 파일을 GitHub에 올리지 않았습니다.
- 문서에는 key 이름만 있고 실제 값은 없습니다.
- Supabase Dashboard에서 key 위치를 찾을 수 있습니다.
