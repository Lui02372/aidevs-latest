# Assignment 07 - Basic Python Final

Python 기초 문법을 모두 사용해 작은 프로그램을 완성하는 종합 과제입니다.

## 과제 파일

```text
submissions/assignment07_learning_record_app.py
```

## 주제

학습 기록 관리 프로그램을 만듭니다.

수강생이 오늘 배운 내용을 기록하고, 완료한 학습만 따로 보고, 총 학습 시간을 계산할 수 있는 콘솔 프로그램입니다.

## 해야 할 일

아래 기능을 순서대로 구현합니다.

| 순서 | 해야 할 일 | 설명 |
| --- | --- | --- |
| 1 | 메뉴 출력 | 추가, 전체 보기, 완료한 학습 보기, 총 시간 보기, 저장, 불러오기, 종료 메뉴를 보여 줍니다. |
| 2 | 학습 기록 추가 | 제목, 학습 시간, 완료 여부를 입력받아 `list`에 `dict`로 저장합니다. |
| 3 | 전체 기록 조회 | 저장된 모든 학습 기록을 반복문으로 출력합니다. |
| 4 | 완료 기록 조회 | `done` 값이 `True`인 기록만 출력합니다. |
| 5 | 총 학습 시간 계산 | 모든 기록의 `minutes` 값을 더해 출력합니다. |
| 6 | JSON 저장 | 학습 기록 목록을 JSON 파일로 저장합니다. |
| 7 | JSON 불러오기 | 저장된 JSON 파일을 다시 읽어 프로그램에서 사용합니다. |
| 8 | 종료 | `q` 또는 종료 메뉴를 선택하면 프로그램을 끝냅니다. |

## 필수 기능

```text
1. 메뉴를 출력합니다.
2. 학습 기록을 추가합니다.
3. 전체 학습 기록을 출력합니다.
4. 완료한 학습만 출력합니다.
5. 총 학습 시간을 계산합니다.
6. 학습 기록을 JSON 파일로 저장합니다.
7. JSON 파일에서 학습 기록을 읽어옵니다.
8. q를 입력하면 프로그램을 종료합니다.
```

## 필수 문법

```text
input()
if / elif / else 또는 match-case
while True
break
list
dict
function
Path
json
```

## 데이터 구조

```python
record = {
    "title": "반복문 복습",
    "minutes": 30,
    "done": True
}
```

## 필수 함수

```text
add_record(records)
print_records(records)
print_done_records(records)
calculate_total_minutes(records)
save_records(records, file_path)
load_records(file_path)
```

## 제출 전 확인

```text
1. 프로그램이 실행되는가?
2. 기록을 2개 이상 추가할 수 있는가?
3. JSON 저장과 읽기가 되는가?
4. q 입력 시 종료되는가?
5. 함수가 역할별로 나뉘어 있는가?
6. 코드에 설명 주석이 있는가?
```
