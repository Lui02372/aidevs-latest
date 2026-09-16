# 02_variables-and-data-types

변수와 기본 자료형을 학습합니다.

## 핵심 내용

```text
변수
숫자형
문자열
불 자료형
형 변환
문자열 인덱싱과 슬라이싱
타입 힌트 기초
```

## 변수와 타입 힌트

가장 기본적인 변수 선언은 아래처럼 씁니다.

```python
name = "kim"
```

Python에서는 변수 이름 뒤에 타입 힌트를 붙일 수도 있습니다.

```python
name: str = "kim"
age: int = 20
height: float = 175.5
is_student: bool = True
```

`name: str = "kim"`은 “`name`이라는 변수는 문자열로 사용할 예정입니다”라는 표시입니다. Python이 실행 중에 항상 타입을 강제로 검사하는 것은 아니지만, VS Code가 코드를 이해하고 오류를 미리 알려 주는 데 도움이 됩니다.

이 단원에서는 변수에 붙이는 타입 힌트까지만 봅니다. 함수의 매개변수와 반환값에 타입 힌트를 붙이는 방법은 `06_function-basic`에서 다시 다룹니다.

이후 FastAPI와 Pydantic에서는 타입 힌트가 더 중요해집니다.

## 실행

```powershell
python .\02_variables-and-data-types\01_variables_types.py
python .\02_variables-and-data-types\02_string_practice.py
python .\02_variables-and-data-types\03_type_hint_basic.py
```
