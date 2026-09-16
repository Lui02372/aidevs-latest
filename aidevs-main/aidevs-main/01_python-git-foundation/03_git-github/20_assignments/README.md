# 20. Assignments

이 폴더는 Git/GitHub 단원의 최종 과제 안내를 담고 있습니다.

과제의 목표는 Git 명령어를 많이 외우는 것이 아닙니다. **VS Code Source Control을 사용해 프로젝트를 GitHub에 올리고, README를 작성하고, 팀 협업 흐름을 설명할 수 있는지** 확인합니다.

## Assignment 01. GitHub 프로젝트 제출

### 과제 주제

작은 Python 테스트 프로젝트를 GitHub에 올리고 README를 작성합니다.

팀 프로젝트로 진행하는 경우, 팀원은 각자 branch에서 작업하고 main 관리자는 Pull Request를 확인한 뒤 merge합니다.

## 해야 할 일

| 순서 | 해야 할 일 | 설명 |
| --- | --- | --- |
| 1 | 작은 Python 파일 작성 | `main.py`에 간단한 함수를 작성합니다. |
| 2 | 테스트 파일 작성 | `test_main.py`에 pytest 테스트를 작성합니다. |
| 3 | 테스트 실행 | 테스트가 통과하는지 확인합니다. |
| 4 | README 작성 | 프로젝트 설명, 실행 방법, 테스트 방법을 작성합니다. |
| 5 | Markdown 요소 추가 | 표, 코드 블록, 이미지 링크, Mermaid 도표 중 3개 이상을 포함합니다. |
| 6 | VS Code에서 변경 확인 | Source Control에서 변경 파일과 diff를 확인합니다. |
| 7 | Commit | 좋은 commit message로 commit합니다. |
| 8 | GitHub Push | GitHub에 push하고 웹에서 결과를 확인합니다. |
| 9 | Secret 점검 | `.env`, `.venv`, 실제 key가 올라가지 않았는지 확인합니다. |

## 팀 프로젝트로 진행할 때 추가로 해야 할 일

| 역할 | 해야 할 일 |
| --- | --- |
| 팀원 | 최신 main을 받은 뒤 자기 branch를 만듭니다. |
| 팀원 | 담당 파일을 수정하고 commit합니다. |
| 팀원 | branch를 push하고 Pull Request를 만듭니다. |
| main 관리자 | PR의 `Files changed`를 확인합니다. |
| main 관리자 | 민감정보, 충돌, README 링크, 테스트 결과를 확인합니다. |
| main 관리자 | 문제가 없으면 merge합니다. |
| 팀원 | merge 후 main으로 돌아가 최신 코드를 pull 또는 sync합니다. |

## README 필수 포함 항목

```text
[ ] 프로젝트 이름
[ ] 프로젝트 설명
[ ] 실행 방법
[ ] 테스트 방법
[ ] 파일 구조 표
[ ] 이미지 링크 또는 실행 결과 캡처 안내
[ ] Mermaid 작업 흐름도
[ ] 실제 key를 넣지 않는다는 안내
```

## 제출물

개인 과제:

```text
1. GitHub 저장소 URL
2. README.md
3. commit 기록
4. 테스트 실행 결과
5. secret 점검 결과
```

팀 과제:

```text
1. GitHub 저장소 URL
2. 팀원별 branch 이름
3. 팀원별 Pull Request 링크
4. main 관리자 merge 기록
5. README.md
6. 테스트 실행 결과
7. secret 점검 결과
```

## main 관리자 Merge 체크리스트

```text
[ ] PR 제목이 작업 내용을 설명합니다.
[ ] PR 설명에 작업 내용이 정리되어 있습니다.
[ ] Files changed에서 실제 변경 내용을 확인했습니다.
[ ] .env 파일이 포함되지 않았습니다.
[ ] .venv 폴더가 포함되지 않았습니다.
[ ] 실제 API key나 token이 없습니다.
[ ] README 링크와 이미지 경로가 깨지지 않았습니다.
[ ] 테스트가 필요한 변경이라면 테스트 설명이 있습니다.
[ ] 충돌 표시가 없습니다.
[ ] 문제가 없어서 merge했습니다.
```

## 평가 기준

| 항목 | 기준 |
| --- | --- |
| VS Code Git 사용 | Source Control로 변경 확인, stage, commit을 진행했는가 |
| GitHub 업로드 | push 후 GitHub 웹에서 결과를 확인했는가 |
| README 품질 | 처음 보는 사람이 실행 방법을 알 수 있는가 |
| Markdown 활용 | 표, 코드 블록, 이미지, Mermaid 도표를 활용했는가 |
| 보안 | `.env`, `.venv`, 실제 key가 올라가지 않았는가 |
| 팀 협업 | branch, Pull Request, main 관리자 merge 흐름을 이해했는가 |
