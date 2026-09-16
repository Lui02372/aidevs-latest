# 06_data-processing-advanced

이 단원에서는 JSON, 날짜, 경로 처리를 본 과정에서 필요한 만큼만 다룹니다.

핵심은 파일 저장형 실습, API 응답 저장, 설정 파일 관리로 이어지는 데이터 처리 흐름입니다.

## 이 단원에서 배우는 것

| 예제 | 핵심 내용 | 과정 연결 |
| --- | --- | --- |
| 01_path_and_data_folder.py | `pathlib.Path`, 데이터 폴더 만들기 | 프로젝트 파일 저장 위치 관리 |
| 02_json_config_and_response.py | JSON 설정/응답 저장 | API 응답, 설정 파일, Supabase 저장 전 데이터 확인 |
| 04_datetime_log_record.py | 날짜/시간 문자열 만들기 | 생성 시간, 로그 시간, 저장 시각 기록 |

## 실행 전 준비

이 폴더에서는 별도의 `.venv`를 만들지 않습니다. `01_python-git-foundation` 최상위에서 만든 공통 가상환경을 사용합니다.

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1
```

## 실행 방법

```powershell
python .\02_python-advanced\06_data-processing-advanced\01_path_and_data_folder.py
python .\02_python-advanced\06_data-processing-advanced\02_json_config_and_response.py
python .\02_python-advanced\06_data-processing-advanced\04_datetime_log_record.py
```

## 핵심 확인

```text
Path:
  운영체제에 맞는 파일 경로를 안전하게 다룹니다.

JSON:
  dict/list 데이터를 파일로 저장하거나 다시 읽을 때 사용합니다.

datetime:
  데이터 생성 시각, 로그 시각, 처리 시각을 남길 때 사용합니다.
```

이번 단원에서는 복잡한 데이터 분석을 다루지 않습니다. 이후 FastAPI, Supabase, 미니 프로젝트에서 필요한 파일 저장과 로그 기록 흐름에 집중합니다.
