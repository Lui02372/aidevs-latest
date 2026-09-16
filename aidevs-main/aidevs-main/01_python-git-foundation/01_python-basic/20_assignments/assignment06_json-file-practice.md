# Assignment 06 - JSON File Practice

JSON 파일에 데이터를 저장하고 다시 읽는 선택 과제입니다.

`07_file-data-basic`의 필수 흐름은 텍스트/CSV 전체가 아니라 `Path`와 JSON 저장입니다. 이 과제도 그 흐름에 맞춰 JSON dict/list 저장과 읽기에 집중합니다.

## 과제 파일

```text
submissions/assignment06_file_data.py
```

## 요구사항

```text
1. data 폴더를 만듭니다.
2. 학생 정보 1개를 student.json으로 저장합니다.
3. 서비스 로그 목록을 service_logs.json으로 저장합니다.
4. 저장한 JSON 파일들을 다시 읽어 화면에 출력합니다.
5. 한글이 깨지지 않도록 ensure_ascii=False를 사용합니다.
6. 사람이 읽기 쉽도록 indent=2를 사용합니다.
```

## student.json에 들어갈 정보

```text
name
score
passed
```

## service_logs.json에 들어갈 정보

```text
level
message
user
```

## 확인 기준

```text
Path를 사용했는가?
dict 데이터를 JSON으로 저장하고 다시 읽었는가?
list 안의 dict 데이터를 JSON으로 저장하고 다시 읽었는가?
ensure_ascii=False를 사용해 한글이 잘 보이게 저장했는가?
indent=2를 사용해 JSON 파일을 읽기 좋게 저장했는가?
```
