# Gitignore And Secret Guide

이 문서는 GitHub에 올리면 안 되는 파일과 민감정보 관리 기준을 설명합니다.

## 민감정보란?

민감정보는 공개되면 안 되는 값입니다.

예시:

```text
Gemini API key
OpenAI API key
Supabase service role key
Upstash Redis token
데이터베이스 비밀번호
개인 이메일/전화번호
```

## `.env`와 `.env.example` 차이

```text
.env
-> 실제 key와 token이 들어가는 개인 환경 파일
-> GitHub에 올리면 안 됨

.env.example
-> 어떤 환경변수가 필요한지 보여주는 예시 파일
-> 실제 key를 넣지 않음
-> GitHub에 올려도 됨
```

## `.gitignore`에 자주 넣는 항목

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

## key가 노출되었을 때 해야 할 일

1. 해당 key를 즉시 폐기하거나 재발급합니다.
2. 새 key를 `.env`에 다시 넣습니다.
3. GitHub에 올라간 기록이 있는지 확인합니다.
4. 진행 중인 상황을 공유합니다.
5. 같은 실수를 막기 위해 `.gitignore`를 점검합니다.

## 커밋 전 확인 문장

커밋하기 전에 아래 질문을 스스로 확인합니다.

```text
이 변경 내용에 실제 API key가 들어 있나요?
.env 파일이 Git에 추가되었나요?
터미널 출력이나 캡처에 secret이 보이나요?
.env.example에는 예시 값만 들어 있나요?
```

