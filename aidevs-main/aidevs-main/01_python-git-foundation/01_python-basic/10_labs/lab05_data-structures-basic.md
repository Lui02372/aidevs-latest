# Lab 05 - Data Structures Basic

여러 값을 자료구조로 관리하는 실습입니다.

## 목표

- `list`, `tuple`, `dict`, `set`의 차이를 설명할 수 있습니다.
- 반복문으로 자료구조 안의 값을 처리할 수 있습니다.
- `list` 안의 `dict` 구조를 사용할 수 있습니다.
- API 응답처럼 중첩된 데이터에서 필요한 값을 꺼낼 수 있습니다.

## 실습 1. 할 일 목록 list

`practice\lab05_todo_list.py` 파일을 만듭니다.

요구사항:

```text
1. 할 일 3개를 list에 저장합니다.
2. append()로 할 일을 하나 추가합니다.
3. enumerate()로 번호와 함께 출력합니다.
```

## 실습 2. 사용자 정보 dict

`practice\lab05_user_dict.py` 파일을 만듭니다.

요구사항:

```text
1. 이름, 이메일, 역할을 dict에 저장합니다.
2. role 값을 "admin" 또는 "member"로 저장합니다.
3. items()를 사용해 key와 value를 모두 출력합니다.
```

## 실습 3. 태그 중복 제거 set

`practice\lab05_tags.py` 파일을 만듭니다.

요구사항:

```text
1. 중복이 있는 태그 list를 만듭니다.
2. set으로 중복을 제거합니다.
3. 최종 태그 목록을 출력합니다.
```

## 실습 4. 학생 목록 평균 계산

`practice\lab05_students.py` 파일을 만듭니다.

요구사항:

```text
1. list 안에 dict 형태로 학생 3명의 이름과 점수를 저장합니다.
2. 반복문으로 전체 점수 합계를 구합니다.
3. 평균 점수를 출력합니다.
4. 60점 이상인 학생만 출력합니다.
```

## 실습 5. 중첩 API 응답 읽기

`practice\lab05_api_response.py` 파일을 만듭니다.

요구사항:

```text
1. dict 안에 data list를 넣습니다.
2. data list 안에는 message dict를 2개 이상 넣습니다.
3. 각 message에서 작성자 이름과 메시지 내용을 출력합니다.
```

## 확인 질문

```text
1. list와 tuple의 차이는 무엇인가요?
2. dict에서 값을 꺼낼 때 사용하는 것은 무엇인가요?
3. set은 어떤 상황에서 유용한가요?
```
