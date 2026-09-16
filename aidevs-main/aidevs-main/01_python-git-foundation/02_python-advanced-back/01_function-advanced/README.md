# 01_function-advanced

이 단원에서는 함수 심화 문법 전체를 넓게 다루지 않습니다. 이후 FastAPI, Supabase, 외부 API, 미니 프로젝트에서 실제로 자주 쓰는 함수 사용법만 학습합니다.

핵심은 “함수를 재사용 가능한 작은 단위로 나누고, 필요한 데이터를 유연하게 전달하는 방법”입니다.

## 이 단원에서 배우는 것

| 예제 | 핵심 내용 | 과정 연결 |
| --- | --- | --- |
| 01_args_kwargs_api_options.py | `*args`, `**kwargs`, 옵션 전달 | API 호출 옵션, 검색 조건, 설정값 전달 |
| 02_unpacking_request_data.py | 리스트/딕셔너리 언패킹 | 요청 데이터, 설정 dict를 함수 인자로 전달 |
| 03_callback_service_flow.py | 함수를 인자로 전달 | 처리 전략 선택, 검증 함수, 서비스 로직 분리 |
| 04_decorator_fastapi_preview.py | 데코레이터 기초 | FastAPI의 `@app.get`, `@app.post` 이해 |
| 05_practice_chat_request_builder.py | 함수 분리 미니 실습 | LLM 질문 요청 데이터 만들기 |

## 실행 전 준비

이 폴더에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위에서 만든 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

## 실행 방법

```powershell
python .\02_python-advanced\01_function-advanced\01_args_kwargs_api_options.py
python .\02_python-advanced\01_function-advanced\02_unpacking_request_data.py
python .\02_python-advanced\01_function-advanced\03_callback_service_flow.py
python .\02_python-advanced\01_function-advanced\04_decorator_fastapi_preview.py
python .\02_python-advanced\01_function-advanced\05_practice_chat_request_builder.py
```

## 핵심 확인

```text
*args는 여러 위치 인자를 tuple로 받습니다.
**kwargs는 여러 키워드 인자를 dict로 받습니다.
*list는 리스트 값을 함수 인자로 풀어 전달합니다.
**dict는 딕셔너리 key/value를 함수 인자로 풀어 전달합니다.
함수를 인자로 전달하면 처리 방식을 바꿀 수 있습니다.
데코레이터는 함수 앞뒤에 기능을 덧붙이는 문법입니다.
```
