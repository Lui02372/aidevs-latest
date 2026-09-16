# Codex와 ChatGPT 사용 준비 가이드

이 과정에서는 코드 오류 분석, 리팩토링, 문서 초안 작성, 테스트 케이스 작성, 프로젝트 구조 검토에 AI 보조 도구를 사용합니다. 수업에서는 환경에 따라 ChatGPT, Codex, GitHub Copilot Chat 중 사용할 수 있는 도구를 선택합니다.

공식 문서:

- [Using Codex with your ChatGPT plan](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
- [What is ChatGPT Business?](https://help.openai.com/en/articles/8792828-what-is-chatgpt-business)
- [Managing members, seat types, and roles in ChatGPT Business](https://help.openai.com/en/articles/8542216-managing-members-seat-types-and-roles-in-chatgpt-business)

## 1. 이 문서가 필요한 이유

수업 중에는 단순히 코드를 복사해서 붙여 넣는 것이 아니라, AI에게 다음 일을 시킵니다.

```text
오류 메시지 분석
코드 리뷰
주석문 보강
테스트 코드 작성
README 초안 작성
프로젝트 구조 개선
배포 오류 원인 정리
```

따라서 로그인 가능한 ChatGPT 또는 Codex 환경이 있으면 실습을 더 안정적으로 따라갈 수 있습니다.

## 2. 먼저 확인할 것

```text
[ ] ChatGPT에 로그인할 수 있다.
[ ] 수업에서 사용할 계정이 개인 계정인지, Business/Enterprise/Edu workspace인지 알고 있다.
[ ] Codex를 사용할 수 있는 plan 또는 workspace인지 확인했다.
[ ] 회사/기관 계정이라면 workspace 관리자 정책을 확인했다.
```

Codex 사용 가능 여부와 제한은 계정과 workspace 정책에 따라 달라질 수 있습니다. 수업 시작 전 현재 계정에서 실제로 사용할 수 있는 기능을 확인합니다.

## 3. ChatGPT 로그인

1. 브라우저에서 ChatGPT에 접속합니다.
2. 수업에서 사용할 계정으로 로그인합니다.
3. 개인 계정과 조직 workspace가 모두 보이면 수업에서 사용할 workspace를 선택합니다.
4. 새 대화를 열어 간단한 질문을 보내 봅니다.

확인 질문 예:

```text
Python 가상환경이 무엇인지 초보자 기준으로 설명해줘.
```

## 4. Codex 사용 확인

Codex를 사용하는 경우 공식 도움말의 안내에 따라 ChatGPT 계정으로 로그인합니다.

확인할 것:

```text
1. Codex 클라이언트 또는 앱을 실행할 수 있는가?
2. ChatGPT 계정으로 로그인되는가?
3. 현재 workspace에서 Codex 사용이 허용되는가?
4. 수업 저장소 폴더를 열고 파일을 읽을 수 있는가?
5. 변경 사항을 diff로 확인할 수 있는가?
```

Codex가 현재 계정에서 보이지 않거나 사용할 수 없다면, ChatGPT 웹 또는 VS Code의 GitHub Copilot Chat으로 대체 실습을 진행할 수 있습니다.

## 5. ChatGPT Business 또는 조직 계정 사용 시

조직 계정에서는 seat, role, workspace 정책이 중요합니다.

확인할 항목:

```text
내 계정이 어느 workspace에 속해 있는가?
내 role이 member인지 admin인지 확인했는가?
Codex seat 또는 사용 권한이 있는가?
조직 정책상 코드 업로드나 파일 연결이 허용되는가?
결제와 사용량 한도는 누가 관리하는가?
```

계정 권한은 수업 중 바로 해결하기 어려울 수 있으므로, 가능한 한 수업 전에 확인합니다.

## 6. AI에게 질문할 때 지켜야 할 기준

좋은 질문은 실행 위치, 실행 명령, 오류 메시지, 기대 결과를 함께 포함합니다.

예:

```text
나는 C:\aidev\02_supabase-ai-backend 폴더에서 실행 중입니다.
명령은 python -m uvicorn app.main:app --reload 입니다.
오류 메시지는 ModuleNotFoundError: No module named 'fastapi' 입니다.
현재 .venv는 활성화되어 있습니다.
원인과 확인 순서를 초보자 기준으로 알려 주세요.
```

나쁜 질문 예:

```text
안 돼요. 고쳐줘.
```

## 7. 절대 보내면 안 되는 정보

AI 도구에 질문할 때도 민감정보는 제거합니다.

```text
API Key
Supabase service_role key
AWS Access Key
비밀번호
실제 결제 정보
개인정보가 들어 있는 데이터
```

오류 메시지에 key가 포함되어 있으면 `***`로 가리고 질문합니다.

예:

```text
SUPABASE_SERVICE_ROLE_KEY=***
```

## 8. 수업에서 권장하는 사용 방식

```text
1. 먼저 README와 SETUP을 읽습니다.
2. 직접 실행해 봅니다.
3. 오류가 나면 오류 메시지 전체를 확인합니다.
4. AI에게 원인 후보와 확인 순서를 물어봅니다.
5. AI가 제안한 코드를 바로 믿지 말고, 변경 전후를 비교합니다.
6. 실행 결과를 다시 확인합니다.
7. 배운 내용을 README나 회고에 짧게 정리합니다.
```

AI는 정답을 대신 제출하는 도구가 아니라, 문제를 더 빨리 이해하고 검증하도록 돕는 도구로 사용합니다.
