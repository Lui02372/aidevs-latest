# 07. .env와 Secret 보안 가이드

`.env`는 API key, token, 비밀번호 같은 비밀 값을 저장하는 파일입니다.

이 파일은 절대 GitHub에 올리지 않습니다.

## 1. .env와 .env.example 차이

```text
.env
  실제 실행에 사용하는 비밀 값이 들어갑니다.
  GitHub에 올리지 않습니다.

.env.example
  어떤 환경변수가 필요한지 보여주는 예시 파일입니다.
  실제 key를 넣지 않습니다.
  GitHub에 올려도 됩니다.
```

## 2. .env 예시

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=real-anon-key
SUPABASE_SERVICE_ROLE_KEY=real-service-role-key
GEMINI_API_KEY=real-gemini-key
```

위 값들은 실제 값이면 GitHub에 올리면 안 됩니다.

## 3. .env.example 예시

```env
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
GEMINI_API_KEY=your-gemini-api-key
```

## 4. GitHub에 올리면 안 되는 값

```text
Gemini API Key
OpenAI API Key
Supabase service role key
Upstash Redis token
AWS Access Key
AWS Secret Access Key
데이터베이스 비밀번호
개인정보 원문
```

## 5. .gitignore 확인

```gitignore
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
```

## 6. 실수로 key를 올렸다면

```text
1. 즉시 해당 key를 폐기하거나 재발급합니다.
2. 새 key를 .env에 다시 넣습니다.
3. 팀원 또는 강사에게 상황을 공유합니다.
4. GitHub 기록에 남은 secret 처리 방법을 확인합니다.
```

단순히 파일에서 지우고 다시 commit하는 것만으로는 과거 commit 기록에 key가 남아 있을 수 있습니다.

## 7. 체크리스트

```text
[ ] .env 파일을 만들었다.
[ ] .env.example에는 예시 값만 있다.
[ ] .gitignore에 .env가 들어 있다.
[ ] README에 실제 key를 적지 않았다.
[ ] 터미널 출력이나 화면 캡처에 key가 보이지 않는다.
```

