# Git Practice Project

이 프로젝트는 Git/GitHub 실습을 위해 만든 작은 Python 테스트 프로젝트입니다.

VS Code Source Control로 변경 파일을 확인하고, README를 작성하고, GitHub에 push하는 흐름을 연습합니다.

## 실행 방법

```powershell
python main.py
```

## 테스트 방법

```powershell
python -m pytest test_main.py
```

## 파일 구조

| 파일 | 설명 |
| --- | --- |
| main.py | 연습용 Python 함수 파일 |
| test_main.py | pytest 테스트 파일 |
| README.md | 프로젝트 설명 문서 |

## 작업 흐름

```mermaid
flowchart LR
    A[코드 작성] --> B[테스트 실행]
    B --> C[README 작성]
    C --> D[Commit]
    D --> E[GitHub Push]
```

## 학습 기록

- VS Code Source Control에서 변경 파일을 확인합니다.
- 변경 파일을 클릭해 diff를 확인합니다.
- 좋은 commit message를 작성합니다.
- GitHub에 push한 뒤 README가 잘 보이는지 확인합니다.
