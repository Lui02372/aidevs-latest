# 04_loop-basic

반복문을 학습합니다.

## 핵심 내용

```text
for
while
while True
range
break
continue
누적 계산
사용자 입력을 이용한 반복 종료
```

## 예제 순서

| 파일 | 내용 |
| --- | --- |
| `01_for_loop.py` | 리스트와 `range()`를 사용해 정해진 횟수만큼 반복합니다. |
| `02_for_continue_break.py` | `for` 반복문에서 `continue`와 `break`의 차이를 확인합니다. |
| `03_while_loop.py` | 조건이 참인 동안 반복하는 `while` 기본 구조를 확인합니다. |
| `04_while_continue_break.py` | `while` 반복문에서 `continue`와 `break`를 사용할 때 주의할 점을 확인합니다. |
| `05_infinite_loop_until_q.py` | `while True`로 계속 실행하다가 사용자가 `q`를 입력하면 종료합니다. |
| `06_loop_calculator.py` | 두 수와 사칙연산 기호를 입력받아 계산 결과를 출력하고, `q`로 종료합니다. |

## 실행

```powershell
python .\04_loop-basic\01_for_loop.py
python .\04_loop-basic\02_for_continue_break.py
python .\04_loop-basic\03_while_loop.py
python .\04_loop-basic\04_while_continue_break.py
python .\04_loop-basic\05_infinite_loop_until_q.py
python .\04_loop-basic\06_loop_calculator.py
```

`05_infinite_loop_until_q.py`는 직접 입력을 받는 예제입니다. 실행 후 아무 값이나 입력하면 계속 진행되고, `q`를 입력하면 종료됩니다.

`06_loop_calculator.py`도 직접 입력을 받는 예제입니다. 첫 번째 숫자 입력 위치에서 `q`를 입력하면 종료됩니다.
