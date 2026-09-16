# 01 Simple Chat Project

이 예제는 프로젝트 폴더 구조를 처음 익히기 위한 가장 단순한 버전입니다.

아직 JSON 저장, 입력 검증, 예외 처리는 넣지 않습니다. 먼저 `main.py`, `models.py`, `services.py`, `tests`가 각각 어떤 역할을 하는지만 확인합니다.

## 구조

```text
01_simple_chat_project
├─ README.md
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ models.py
│  └─ services.py
└─ tests
   └─ test_basic_services.py
```

## 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\04_project-structure\01_simple_chat_project\main.py
```

## 테스트

```powershell
python -m pytest .\02_python-advanced\04_project-structure\01_simple_chat_project
```

## 파일 역할

| 파일 | 역할 |
| --- | --- |
| `main.py` | 프로그램 실행 시작점 |
| `app/models.py` | 질문과 답변 데이터 모양 정의 |
| `app/services.py` | 질문을 받아 연습용 답변 만들기 |
| `tests/test_basic_services.py` | 서비스 함수가 예상대로 동작하는지 확인 |

## 다음 예제와의 차이

다음 예제인 `02_simple_chat_project`에서는 아래 내용을 추가합니다.

```text
질문 앞뒤 공백 제거
빈 질문 검증
ValueError 예외 처리
JSON 파일 저장과 읽기
테스트 항목 확장
```
