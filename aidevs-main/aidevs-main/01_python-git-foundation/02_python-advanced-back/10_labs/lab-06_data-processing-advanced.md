# Lab 06. JSON 데이터 처리

이 실습에서는 JSON, 날짜/시간, 파일 경로를 이용해 작은 서비스 로그 데이터를 저장합니다.

## 실습 목표

```text
1. pathlib로 data 폴더와 파일 경로를 만들 수 있습니다.
2. dict/list 데이터를 JSON 파일로 저장할 수 있습니다.
3. datetime으로 생성 시각을 기록할 수 있습니다.
```

## 실습 1. data 폴더 만들기

`Path("data")`를 사용해 data 폴더를 만듭니다.

```python
from pathlib import Path

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)
```

확인할 내용:

```text
data 폴더가 생성되었나요?
이미 폴더가 있어도 오류 없이 실행되나요?
```

## 실습 2. JSON 응답 저장하기

아래 형태의 채팅 응답 데이터를 JSON 파일로 저장합니다.

```python
record = {
    "question": "FastAPI에서 JSON은 왜 사용하나요?",
    "answer": "JSON은 API 데이터 교환에 자주 사용됩니다.",
}
```

요구사항:

```text
1. json.dumps를 사용합니다.
2. ensure_ascii=False를 사용해 한글이 깨지지 않게 합니다.
3. indent=2를 사용해 사람이 읽기 좋게 저장합니다.
4. 저장한 파일을 다시 읽어 question 값을 출력합니다.
```

## 실습 3. 로그 생성 시각 추가하기

각 로그에 `created_at` 값을 추가합니다.

```python
from datetime import datetime, timezone

created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
```

확인할 내용:

```text
created_at 값이 문자열로 저장되나요?
로그마다 생성 시각을 기록하면 어떤 점이 좋은가요?
```

## 제출 기준

```text
1. JSON 저장 예제가 있어야 합니다.
2. created_at 날짜/시간 값이 포함되어야 합니다.
3. data 폴더를 코드에서 직접 생성해야 합니다.
4. 실행 후 생성된 파일 내용을 확인한 결과를 README에 정리합니다.
```
