# 07_file-data-basic

파일에 데이터를 저장하고 읽는 기초를 학습합니다.

## 핵심 내용

```text
파일 경로
JSON 파일 쓰기
JSON 파일 읽기
list/dict 데이터를 파일에 저장하기
```

## 파일과 데이터를 배우는 이유

프로그램이 실행되는 동안 만든 값은 보통 메모리에만 있습니다. 프로그램이 종료되면 메모리에 있던 값은 사라집니다. 데이터를 남기려면 파일, 데이터베이스, 외부 저장소에 저장해야 합니다.

이 단원에서는 가장 기본적인 파일 저장 방식을 먼저 연습합니다. 이후에는 Supabase에 사용자 정보, 대화 이력, 서비스 로그를 저장하게 됩니다. 파일 저장을 먼저 이해하면 데이터가 “어떤 구조로 저장되고 다시 읽히는지”를 더 쉽게 이해할 수 있습니다.

예외 처리는 다음 단계에서 따로 학습합니다. 이 단원은 뒤 과정과 바로 연결되는 `Path`와 JSON 저장 흐름에 먼저 집중합니다. 텍스트 파일, CSV, 설정 JSON은 보충 예제로 둡니다.

## 필수 예제

| 파일 | 내용 |
| --- | --- |
| `01_path_basic.py` | `Path`를 사용해 폴더와 파일 경로를 다룹니다. |
| `05_json_dict_basic.py` | dict 한 개를 JSON 파일로 저장하고 읽습니다. |
| `06_json_list_logs.py` | list 안에 dict를 넣은 로그 데이터를 JSON 파일로 저장합니다. |

## 선택 예제

| 파일 | 내용 |
| --- | --- |
| `02_text_file_write_read.py` | 텍스트 파일에 문자열을 저장하고 다시 읽습니다. |
| `03_text_file_lines_append.py` | 여러 줄 텍스트를 저장하고 뒤에 내용을 추가합니다. |
| `04_csv_basic.py` | 표 형태 데이터를 CSV 파일로 저장하고 읽습니다. |
| `07_config_json_basic.py` | 설정값을 JSON 파일로 저장하고 프로그램에서 읽어옵니다. |

## 필수 예제 실행

```powershell
python .\07_file-data-basic\01_path_basic.py
python .\07_file-data-basic\05_json_dict_basic.py
python .\07_file-data-basic\06_json_list_logs.py
```

## 선택 예제 실행

```powershell
python .\07_file-data-basic\02_text_file_write_read.py
python .\07_file-data-basic\03_text_file_lines_append.py
python .\07_file-data-basic\04_csv_basic.py
python .\07_file-data-basic\07_config_json_basic.py
```

## 생성되는 파일

예제를 실행하면 현재 실행 위치 아래에 `data` 폴더가 만들어지고, 그 안에 연습용 파일이 생성됩니다.

```text
data
├─ memo.txt
├─ daily_log.txt
├─ students.csv
├─ student.json
├─ service_logs.json
└─ config.json
```

필수 예제만 실행하면 `student.json`, `service_logs.json` 중심으로 확인하면 됩니다. 선택 예제까지 실행하면 텍스트 파일, CSV, config JSON도 함께 생성됩니다. 내용을 직접 열어 보면 Python 자료구조가 파일 안에서 어떻게 표현되는지 확인할 수 있습니다.
