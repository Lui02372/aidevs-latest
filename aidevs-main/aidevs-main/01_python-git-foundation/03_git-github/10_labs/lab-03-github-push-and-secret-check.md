# Lab 03. GitHub Push와 Secret 점검

이 실습에서는 VS Code에서 commit한 내용을 GitHub에 올리고, 민감정보가 포함되지 않았는지 확인합니다.

## 실습 목표

```text
1. VS Code에서 Push 또는 Sync Changes를 사용할 수 있습니다.
2. GitHub 웹에서 commit과 README를 확인할 수 있습니다.
3. .env와 .env.example의 차이를 설명할 수 있습니다.
4. GitHub에 올리면 안 되는 파일을 점검할 수 있습니다.
```

## 1. Push 전 확인

Source Control에서 변경 파일을 확인합니다.

commit 전에는 아래를 확인합니다.

```text
[ ] .env 파일이 Changes에 보이지 않습니다.
[ ] .venv 폴더가 Changes에 보이지 않습니다.
[ ] __pycache__ 폴더가 Changes에 보이지 않습니다.
[ ] README에 실제 API key가 없습니다.
[ ] sample.env.example에는 예시 값만 있습니다.
```

## 2. .env와 .env.example 차이

```text
.env:
  실제 key와 token이 들어가는 개인 파일입니다.
  GitHub에 올리면 안 됩니다.

.env.example:
  어떤 환경변수가 필요한지 보여주는 예시 파일입니다.
  실제 key를 넣지 않습니다.
  GitHub에 올려도 됩니다.
```

예시:

```env
GEMINI_API_KEY=your-gemini-api-key
SUPABASE_URL=your-supabase-url
```

## 3. VS Code에서 Push 하기

commit이 끝난 뒤 Source Control에 아래 버튼 중 하나가 보일 수 있습니다.

```text
Publish Branch
Push
Sync Changes
```

처음 GitHub에 올리는 branch라면 `Publish Branch`를 누릅니다.

이미 GitHub와 연결되어 있다면 `Push` 또는 `Sync Changes`를 사용합니다.

## 4. GitHub 웹에서 확인

GitHub 저장소 페이지를 열고 아래를 확인합니다.

```text
1. README가 화면에 보이나요?
2. 표와 코드 블록이 깨지지 않았나요?
3. Mermaid 도표가 보이나요?
4. 최근 commit message가 보이나요?
5. .env 파일이 올라가지 않았나요?
6. .venv 폴더가 올라가지 않았나요?
7. 실제 key나 token이 보이지 않나요?
```

## 5. 문제가 생겼을 때

### Push가 안 되는 경우

확인용 명령어:

```powershell
git status
git remote -v
```

확인할 내용:

```text
현재 폴더가 Git 저장소인가요?
GitHub 원격 저장소가 연결되어 있나요?
VS Code가 GitHub 계정으로 로그인되어 있나요?
```

### .env가 보이는 경우

즉시 멈추고 강사나 팀원에게 공유합니다.

처리 방향:

```text
1. .gitignore에 .env가 있는지 확인합니다.
2. 실제 key가 노출되었다면 key를 폐기하거나 재발급합니다.
3. 이미 push했다면 혼자 해결하려 하지 말고 상황을 공유합니다.
```

## 정리 질문

```text
1. commit과 push는 무엇이 다른가요?
2. .env.example은 왜 GitHub에 올려도 되나요?
3. 실제 API key가 GitHub에 올라가면 어떤 문제가 생기나요?
4. Push 후 GitHub 웹에서 무엇을 확인해야 하나요?
```
