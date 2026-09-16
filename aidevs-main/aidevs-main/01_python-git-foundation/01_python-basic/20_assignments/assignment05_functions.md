# Assignment 05 - Functions

기존 코드를 함수로 분리하는 과제입니다.

## 과제 파일

```text
submissions/assignment05_functions.py
```

## 요구사항

아래 함수를 모두 만듭니다.

```text
get_grade(score)
is_passed(score)
calculate_average(scores)
filter_passed_students(students)
print_student(student)
```

## 함수 설명

```text
get_grade(score): 점수를 받아 A/B/C/D를 반환합니다.
is_passed(score): 60점 이상이면 True를 반환합니다.
calculate_average(scores): 점수 list를 받아 평균을 반환합니다.
filter_passed_students(students): 통과한 학생 dict만 모아 list로 반환합니다.
print_student(student): 학생 dict 하나를 보기 좋게 출력합니다.
```

## 데이터 예시

```python
students = [
    {"name": "Jean", "score": 95},
    {"name": "Mina", "score": 82},
    {"name": "Jun", "score": 58},
]
```

## 확인 기준

```text
함수가 값을 return하는가?
함수 이름이 역할을 잘 설명하는가?
같은 함수를 여러 데이터에 재사용했는가?
```
