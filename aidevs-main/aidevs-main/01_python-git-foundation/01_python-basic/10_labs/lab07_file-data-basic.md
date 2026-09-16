# Lab 07 - File Data Basic

파일에 데이터를 저장하고 다시 읽는 실습입니다.

## 목표

- `Path`로 폴더와 파일 경로를 만들 수 있습니다.
- JSON 파일에 dict와 list를 저장할 수 있습니다.

## 실습 1. data 폴더 만들기

`practice\lab07_path.py` 파일을 만듭니다.

요구사항:

```text
1. data 폴더를 만듭니다.
2. data 폴더 경로를 출력합니다.
3. student.json 파일 경로를 출력합니다.
```

## 실습 2. 학생 정보 JSON 저장

`practice\lab07_student_json.py` 파일을 만듭니다.

요구사항:

```text
1. 학생 정보 dict를 만듭니다.
2. student.json 파일로 저장합니다.
3. 저장한 JSON 파일을 다시 읽습니다.
4. 이름과 점수를 출력합니다.
```

## 실습 3. 서비스 로그 JSON 저장

`practice\lab07_logs_json.py` 파일을 만듭니다.

요구사항:

```text
1. list 안에 dict 형태로 로그 3개를 저장합니다.
2. service_logs.json으로 저장합니다.
3. 다시 읽어 로그 level과 message를 출력합니다.
```

## 선택 실습. 설정 JSON 저장

`practice\lab07_config_json.py` 파일을 만듭니다.

요구사항:

```text
1. app_name, debug, default_model 값을 dict에 저장합니다.
2. config.json 파일로 저장합니다.
3. 다시 읽어 각 설정값을 출력합니다.
```

## 확인 질문

```text
1. dict를 JSON으로 저장하면 어떤 모양이 되나요?
2. list 안의 dict를 JSON으로 저장하면 어떤 데이터에 적합한가요?
3. ensure_ascii=False는 왜 사용하나요?
```
