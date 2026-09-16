# 01_function-and-import

이 단원에서는 함수와 import를 함께 다룹니다.

목표는 한 파일에 모든 코드를 몰아넣지 않고, 필요한 기능을 함수와 다른 파일로 나누는 것입니다.

## 예제

| 파일 | 내용 |
| --- | --- |
| `01_function_basic_review.py` | 함수의 입력값, 반환값, 실행 흐름 복습 |
| `02_dict_parameter.py` | dict 데이터를 함수에 전달하고 필요한 값을 꺼내기 |
| `03_import_my_module.py` | 직접 만든 `my_tools.py`에서 함수를 가져와 사용하기 |
| `my_tools.py` | import 연습에 사용할 함수 모음 |

## 실행 방법

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\01_function-and-import\01_function_basic_review.py
python .\02_python-advanced\01_function-and-import\02_dict_parameter.py
python .\02_python-advanced\01_function-and-import\03_import_my_module.py
```

## 핵심 정리

```text
함수:
  반복되는 코드를 이름 붙여 다시 사용할 수 있게 만든 것입니다.

매개변수:
  함수가 일을 할 때 필요한 입력값입니다.

return:
  함수가 처리한 결과를 밖으로 돌려주는 문법입니다.

dict:
  여러 값을 key/value 형태로 묶는 자료형입니다.

import:
  다른 .py 파일에 있는 함수를 가져오는 문법입니다.
```
