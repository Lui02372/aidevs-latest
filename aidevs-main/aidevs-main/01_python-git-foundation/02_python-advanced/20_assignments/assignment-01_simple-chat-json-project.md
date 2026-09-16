# Assignment 01. 질문/답변 JSON 저장 프로그램

## 주제

간단한 질문/답변 기록 프로그램을 만듭니다.

실제 LLM API는 호출하지 않습니다. 질문을 입력하면 mock 답변을 만들고 JSON 파일에 저장합니다.

## 필수 기능

| 순서 | 해야 할 일 | 설명 |
| --- | --- | --- |
| 1 | 질문 문자열 준비 | 직접 코드에 질문 문자열을 하나 작성합니다. |
| 2 | 질문 정리 함수 | 앞뒤 공백을 제거하는 함수를 만듭니다. |
| 3 | 질문 검증 함수 | 질문이 비어 있으면 `ValueError`를 발생시킵니다. |
| 4 | mock 답변 함수 | 실제 AI 대신 고정된 문장으로 답변을 만듭니다. |
| 5 | 응답 dict 만들기 | `question`, `answer`, `model` key를 가진 dict를 만듭니다. |
| 6 | JSON 저장 | 응답 dict를 JSON 파일에 저장합니다. |
| 7 | README 작성 | 실행 방법과 파일 역할을 적습니다. |

## 권장 구조

```text
simple_chat_assignment
├─ README.md
├─ main.py
├─ app
│  ├─ __init__.py
│  ├─ services.py
│  └─ storage.py
└─ data
   └─ chat_messages.json
```

## 선택 기능

시간이 충분하면 하나만 선택해서 추가합니다.

```text
pytest 테스트 1~2개 작성
dataclass로 ChatMessage object 만들기
저장된 JSON 파일 다시 읽어서 개수 출력
```

## 실행 방법 예시

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
python .\02_python-advanced\20_assignments\simple_chat_assignment\main.py
```

## 완료 기준

```text
[ ] main.py가 실행된다.
[ ] 질문이 비어 있으면 오류가 처리된다.
[ ] JSON 파일이 생성된다.
[ ] JSON 파일에 한글이 깨지지 않는다.
[ ] README에 실행 방법이 있다.
```

## 이후 과정과의 연결

```text
services.py:
  이후 FastAPI service 함수로 연결됩니다.

storage.py:
  이후 Supabase 저장 함수로 연결됩니다.

response dict:
  이후 Pydantic Response Model로 연결됩니다.
```
