# 06_function-basic

함수 기초를 학습합니다.

## 핵심 내용

```text
함수 정의
함수 호출
매개변수
반환값
기본값 매개변수
키워드 인자
여러 반환값
자료구조와 함수
조건문과 함수
코드 정리
```

## 함수를 배우는 이유

처음에는 코드를 위에서 아래로 한 줄씩 작성합니다. 하지만 같은 코드가 반복되거나 프로그램이 길어지면 읽기 어렵고 수정하기 어려워집니다.

함수는 코드를 작은 역할 단위로 나누는 방법입니다. 이후 FastAPI에서 API endpoint를 만들 때도 함수로 요청을 처리하고, LLM API 호출이나 Supabase 저장 로직도 함수로 나누어 작성합니다.

## 예제 순서

| 파일 | 내용 |
| --- | --- |
| `01_define_and_call.py` | 함수를 정의하고 호출하는 가장 기본 흐름을 확인합니다. |
| `02_parameter_basic.py` | 매개변수를 사용해 함수에 값을 전달합니다. |
| `03_return_value.py` | `return`으로 함수 결과를 다시 사용할 수 있게 만듭니다. |
| `04_default_keyword_arguments.py` | 기본값 매개변수와 키워드 인자를 사용합니다. |
| `05_multiple_return_values.py` | 여러 값을 한 번에 반환하고 나누어 받습니다. |
| `06_function_with_list_dict.py` | `list`, `dict` 같은 자료구조를 함수로 처리합니다. |
| `07_condition_function.py` | 조건문을 함수 안에 넣어 판단 로직을 재사용합니다. |
| `08_calculator_refactor.py` | 반복문 단원의 계산기 로직을 함수로 분리합니다. |

## 실행

```powershell
python .\06_function-basic\01_define_and_call.py
python .\06_function-basic\02_parameter_basic.py
python .\06_function-basic\03_return_value.py
python .\06_function-basic\04_default_keyword_arguments.py
python .\06_function-basic\05_multiple_return_values.py
python .\06_function-basic\06_function_with_list_dict.py
python .\06_function-basic\07_condition_function.py
python .\06_function-basic\08_calculator_refactor.py
```

## 함수 작성 순서

처음에는 아래 순서로 생각하면 됩니다.

```text
1. 이 코드가 어떤 일을 하는지 이름을 정합니다.
2. 함수 안으로 들어와야 하는 값이 있는지 생각합니다.
3. 함수 밖으로 돌려줘야 하는 결과가 있는지 생각합니다.
4. 같은 함수를 다른 값으로 여러 번 호출해 봅니다.
```
