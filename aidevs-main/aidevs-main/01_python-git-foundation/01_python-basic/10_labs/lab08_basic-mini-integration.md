# Lab 08 - Basic Mini Integration

기초 문법을 묶어 작은 학습 기록 관리 프로그램을 만드는 통합 실습입니다.

## 목표

- 조건문, 반복문, 자료구조, 함수, 파일 저장을 함께 사용할 수 있습니다.
- 메뉴 기반 프로그램을 만들 수 있습니다.
- 학습 기록을 JSON 파일에 저장하고 다시 읽을 수 있습니다.

## 최종 과제

`practice\lab08_learning_records.py` 파일을 만듭니다.

## 기능 요구사항

```text
1. while True로 프로그램을 계속 실행합니다.
2. match-case 또는 if/elif/else로 메뉴를 처리합니다.
3. 메뉴 1: 학습 기록 추가
4. 메뉴 2: 전체 학습 기록 보기
5. 메뉴 3: 완료한 학습만 보기
6. 메뉴 4: JSON 파일로 저장
7. 메뉴 5: JSON 파일에서 읽기
8. q: 프로그램 종료
```

## 데이터 구조

학습 기록은 아래 형태의 dict로 저장합니다.

```python
{
    "title": "조건문 복습",
    "minutes": 30,
    "done": True
}
```

전체 기록은 list에 담습니다.

```python
records = []
```

## 함수 요구사항

아래 함수를 만들어 사용합니다.

```text
add_record(records)
print_records(records)
print_done_records(records)
save_records(records, file_path)
load_records(file_path)
```

## 저장 파일

JSON 파일은 아래 위치에 저장합니다.

```text
data/learning_records.json
```

## 완료 기준

```text
1. 기록을 2개 이상 추가할 수 있습니다.
2. 전체 기록을 출력할 수 있습니다.
3. 완료한 기록만 출력할 수 있습니다.
4. JSON 파일로 저장할 수 있습니다.
5. 프로그램을 다시 실행한 뒤 JSON 파일에서 읽어올 수 있습니다.
6. q를 입력하면 종료됩니다.
```

## 확장 아이디어

기본 기능을 완성한 뒤 아래 기능 중 하나를 추가해 봅니다.

```text
1. 총 학습 시간 계산
2. 완료율 계산
3. 특정 키워드가 들어간 기록 검색
4. 잘못된 메뉴 입력 안내
```
