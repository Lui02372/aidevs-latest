# Assignment 04 - Data Structures

자료구조를 사용해 학생 관리 데이터를 만듭니다.

## 과제 파일

```text
submissions/assignment04_student_data.py
```

## 요구사항

```text
1. 학생 3명 이상의 정보를 list 안의 dict로 저장합니다.
2. 각 학생 dict에는 name, score, tags를 포함합니다.
3. tags는 list로 저장합니다.
4. 모든 학생의 이름과 점수를 출력합니다.
5. 평균 점수를 계산합니다.
6. 60점 이상인 학생만 출력합니다.
7. 전체 tags를 set으로 변환해 중복을 제거합니다.
```

## 데이터 예시

```python
students = [
    {"name": "Jean", "score": 95, "tags": ["python", "backend"]},
    {"name": "Mina", "score": 82, "tags": ["python", "ui"]},
]
```

## 추가 과제

```text
가장 높은 점수를 받은 학생 이름을 출력합니다.
```

## 확인 기준

```text
list, dict, set을 모두 사용했는가?
반복문으로 자료구조를 처리했는가?
중복 태그가 제거되었는가?
```
