# Lab 04. OOP 핵심만 사용하기

이 실습에서는 객체지향 프로그래밍 전체를 깊게 다루지 않고, 이후 FastAPI와 Supabase 코드에서 자주 쓰이는 부분만 연습합니다.

## 실습 목표

```text
1. 클래스를 정의할 수 있습니다.
2. __init__과 self의 역할을 설명할 수 있습니다.
3. 메서드로 객체의 상태를 바꿀 수 있습니다.
4. dataclass 객체를 dict로 변환할 수 있습니다.
```

## 실습 1. 학습 노트 클래스 만들기

`LearningNote` 클래스를 만듭니다.

요구사항:

```text
1. title과 content를 저장합니다.
2. print_summary() 메서드를 만듭니다.
3. "제목 - 내용" 형태로 출력합니다.
```

## 실습 2. 상태가 바뀌는 Task 만들기

`Task` 클래스를 만들고 완료 상태를 관리합니다.

요구사항:

```text
1. title을 저장합니다.
2. done은 처음에 False로 시작합니다.
3. complete() 메서드를 호출하면 done이 True가 됩니다.
4. label() 메서드는 [진행중] 또는 [완료] 문장을 반환합니다.
```

## 실습 3. dataclass와 dict 변환

`Contact` dataclass를 만들고 `asdict`로 변환합니다.

요구사항:

```text
1. name, phone, email 필드를 만듭니다.
2. Contact 객체를 하나 만듭니다.
3. asdict(contact) 결과를 출력합니다.
4. 이 dict가 JSON 저장이나 API 응답에 쓰일 수 있음을 메모합니다.
```

## 상속은 어떻게 이해하면 되나요?

이번 실습에서는 상속 예제를 필수로 작성하지 않습니다. 다만 FastAPI/Pydantic에서 아래와 같은 문법을 볼 수 있습니다.

```python
class UserCreate(BaseModel):
    ...
```

이 문법은 `BaseModel`의 기능을 물려받아 `UserCreate` 클래스를 만든다는 뜻입니다. 지금은 “기존 클래스 기능을 빌려 쓰는 문법” 정도로만 이해하면 충분합니다.

## 제출 기준

```text
1. 클래스 예제가 있어야 합니다.
2. 메서드로 객체 상태를 변경하는 예제가 있어야 합니다.
3. dataclass와 asdict 예제가 있어야 합니다.
4. 상속은 필수 구현 대상이 아닙니다.
```
