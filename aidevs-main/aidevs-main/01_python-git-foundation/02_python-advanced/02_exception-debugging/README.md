# 02_exception-debugging

이 단원에서는 오류를 무서워하지 않고 읽는 연습을 합니다.

FastAPI, Supabase, LLM API를 사용하면 오류를 자주 만납니다. 중요한 것은 오류가 나지 않게 만드는 것이 아니라, 오류가 났을 때 원인을 찾을 수 있는 것입니다.

## 예제

| 파일 | 내용 |
| --- | --- |
| `01_try_except_basic.py` | `try/except`로 숫자 변환 오류 처리 |
| `02_raise_validation.py` | 잘못된 값을 직접 검사하고 `raise` 사용 |
| `03_read_json_safely.py` | JSON 파일을 안전하게 읽기 |
| `config.json` | 정상 JSON 예제 |
| `broken_config.json` | 일부러 깨진 JSON 예제 |

## 실행 방법

```powershell
cd C:\aidev\01_python-git-foundation
.\.venv\Scripts\Activate.ps1

python .\02_python-advanced\02_exception-debugging\01_try_except_basic.py
python .\02_python-advanced\02_exception-debugging\02_raise_validation.py
python .\02_python-advanced\02_exception-debugging\03_read_json_safely.py
```

## 핵심 정리

```text
try:
  오류가 날 수 있는 코드를 넣습니다.

except:
  오류가 났을 때 실행할 코드를 넣습니다.

raise:
  코드에서 직접 오류를 발생시킵니다.

traceback:
  오류가 난 파일, 줄 번호, 오류 종류를 보여 주는 메시지입니다.
```
