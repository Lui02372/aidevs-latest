# Lab 04. 작은 프로젝트 구조

## 목표

같은 프로젝트 구조를 두 단계로 확인합니다.

```text
1단계: 01_simple_chat_project에서 main.py, models.py, services.py, tests 역할 확인
2단계: 02_simple_chat_project에서 storage.py, JSON 저장, 입력 검증, 예외 처리 확인
```

## 먼저 실행

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\04_project-structure\01_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\01_simple_chat_project

python .\02_python-advanced\04_project-structure\02_simple_chat_project\main.py
python -m pytest .\02_python-advanced\04_project-structure\02_simple_chat_project
```

## 해야 할 일

먼저 `01_simple_chat_project/app/services.py`의 `create_mock_answer` 함수가 반환하는 문장을 바꿔 봅니다.

예:

```python
return f"'{question}'에 대해 구조화된 답변을 준비했습니다."
```

그 다음 `01_simple_chat_project/main.py`를 다시 실행해서 화면 출력이 바뀌는지 확인합니다.

이후 `02_simple_chat_project/main.py`를 실행해서 같은 질문/답변 흐름에 JSON 저장 기능이 추가된 것을 확인합니다.

## 완료 기준

```text
[ ] 01_simple_chat_project의 services.py에서 답변 문장을 수정했다.
[ ] 01_simple_chat_project/main.py 실행 결과가 바뀌었다.
[ ] 01_simple_chat_project의 pytest가 통과한다.
[ ] 02_simple_chat_project/main.py를 실행했다.
[ ] 02_simple_chat_project/data/chat_messages.json 파일이 생성되는 것을 확인했다.
[ ] 02_simple_chat_project의 pytest가 통과한다.
```

## 생각해 보기

```text
답변 생성 로직은 왜 main.py가 아니라 services.py에 있을까요?
01_simple_chat_project에는 storage.py가 없고, 02_simple_chat_project에는 storage.py가 있는 이유는 무엇일까요?
```
