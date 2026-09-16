# 05_data-structures-basic

여러 값을 관리하는 자료구조를 학습합니다.

## 핵심 내용

```text
list
tuple
dict
set
반복문과 자료구조
중첩 자료구조
API 응답 형태 이해
```

## 자료구조를 배우는 이유

프로그램은 대부분 여러 개의 데이터를 다룹니다. 한 명의 사용자만 저장하는 것이 아니라 여러 사용자 목록을 다루고, 하나의 메시지만 처리하는 것이 아니라 여러 대화 기록을 조회합니다.

Python에서는 이런 데이터를 주로 `list`, `tuple`, `dict`, `set`으로 표현합니다. 이후 FastAPI, Supabase, LLM API를 사용할 때도 요청 데이터와 응답 데이터를 이런 자료구조로 다루게 됩니다.

## 예제 순서

| 파일 | 내용 |
| --- | --- |
| `01_list_basic.py` | 순서가 있고 수정 가능한 여러 값을 `list`로 관리합니다. |
| `02_tuple_basic.py` | 한 번 만들면 바꿀 수 없는 여러 값을 `tuple`로 관리합니다. |
| `03_dict_basic.py` | 이름표 역할을 하는 key와 실제 값인 value를 `dict`로 관리합니다. |
| `04_set_basic.py` | 중복을 제거하고 집합 연산을 할 수 있는 `set`을 학습합니다. |
| `05_loop_with_data_structures.py` | `list` 안의 `dict`를 반복문으로 처리합니다. |
| `06_nested_api_response.py` | 실제 API 응답처럼 중첩된 `dict`, `list` 구조에서 필요한 값을 꺼냅니다. |

## 실행

```powershell
python .\05_data-structures-basic\01_list_basic.py
python .\05_data-structures-basic\02_tuple_basic.py
python .\05_data-structures-basic\03_dict_basic.py
python .\05_data-structures-basic\04_set_basic.py
python .\05_data-structures-basic\05_loop_with_data_structures.py
python .\05_data-structures-basic\06_nested_api_response.py
```

## 언제 어떤 자료구조를 사용할까?

| 상황 | 추천 자료구조 |
| --- | --- |
| 여러 값을 순서대로 저장하고 수정해야 할 때 | `list` |
| 여러 값을 순서대로 저장하지만 바꾸면 안 될 때 | `tuple` |
| 이름표(key)로 값을 찾고 싶을 때 | `dict` |
| 중복을 제거하고 싶을 때 | `set` |
| 여러 명의 사용자, 여러 개의 메시지처럼 복잡한 데이터를 표현할 때 | `list` + `dict` |
