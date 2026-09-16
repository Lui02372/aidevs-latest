# 02 Simple Chat Project

함수, import, 예외 처리, JSON 저장, 테스트를 하나의 작은 프로젝트로 연결하는 확장 예제입니다.

실제 AI API를 호출하지 않고 연습용 mock 답변을 만듭니다.

먼저 `01_simple_chat_project`에서 기본 폴더 구조를 확인한 뒤 이 예제를 봅니다.

`02_simple_chat_project`에서는 아래 내용이 추가됩니다.

```text
질문 앞뒤 공백 제거
빈 질문 검증
ValueError 예외 처리
JSON 파일 저장과 읽기
테스트 항목 확장
```

## 구조

```text
02_simple_chat_project
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ models.py
│  ├─ services.py
│  └─ storage.py
└─ tests
   └─ test_validated_services.py
```

## 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py
```

## 테스트

```powershell
python -m pytest .\02_python-advanced\04_project-structure\02_simple_chat_project
```

## 파일 역할

| 파일 | 역할 |
| --- | --- |
| `main.py` | 프로그램 실행 시작점 |
| `app/models.py` | 데이터 모양을 dataclass로 정의 |
| `app/services.py` | 질문 검증, mock 답변 생성, 응답 데이터 생성 |
| `app/storage.py` | JSON 파일 저장과 읽기 |
| `tests/test_validated_services.py` | 입력 검증이 포함된 핵심 서비스 함수 테스트 |
