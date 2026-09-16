# 03_single-turn-call

이 폴더는 한 번의 사용자 입력에 대해 한 번의 LLM 응답을 받는 single-turn 호출 예제를 다룹니다.

## 실행 흐름

| 순서 | 파일 | 역할 |
| --- | --- | --- |
| 1 | `01_mock_single_turn.py` | 실제 API 호출 없이 single-turn 구조 확인 |
| 2 | `02_gemini_sdk_single_turn_small.py` | 예외 처리 없이 가장 작은 Gemini SDK 호출 확인 |
| 3 | `03_gemini_sdk_single_turn.py` | key 확인과 오류 안내가 포함된 Gemini SDK 호출 |
| 4 | `04_openai_sdk_single_turn.py` | OpenAI SDK 선택/비교 실습 |

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\03_single-turn-call\01_mock_single_turn.py
python .\02_llm-api-integration\03_single-turn-call\02_gemini_sdk_single_turn_small.py
python .\02_llm-api-integration\03_single-turn-call\03_gemini_sdk_single_turn.py
python .\02_llm-api-integration\03_single-turn-call\04_openai_sdk_single_turn.py
```

처음에는 `01_mock_single_turn.py`로 비용 없이 구조를 확인합니다. 실제 Gemini API 호출은 `02_gemini_sdk_single_turn_small.py`에서 가장 작은 코드로 먼저 보고, 오류 처리와 안전장치는 `03_gemini_sdk_single_turn.py`에서 확인합니다. OpenAI SDK 예제는 선택/비교 실습입니다.

## Gemini 503 UNAVAILABLE 오류

실제 Gemini API를 호출할 때 아래와 같은 오류가 날 수 있습니다.

```text
503 UNAVAILABLE
This model is currently experiencing high demand.
```

이 오류는 Python 코드 문법 오류가 아니라 Gemini API 서버가 일시적으로 바쁘거나 해당 모델 수요가 높은 상태라는 뜻입니다.

이럴 때는 아래 순서로 확인합니다.

```text
1. 잠시 뒤 같은 명령을 다시 실행합니다.
2. .env의 GEMINI_MODEL 값이 현재 사용 가능한 모델인지 확인합니다.
3. Google AI Studio에서 quota, rate limit, billing 상태를 확인합니다.
4. 수업 흐름을 계속 진행해야 하면 01_mock_single_turn.py로 구조를 먼저 복습합니다.
5. 오류 메시지를 더 쉽게 보고 싶으면 03_gemini_sdk_single_turn.py를 실행합니다.
```

가상환경을 활성화한 뒤에는 `py`보다 `python` 명령을 사용하는 것을 권장합니다. 그래야 현재 `.venv`의 Python을 사용하는지 확인하기 쉽습니다.

```powershell
python -c "import sys; print(sys.executable)"
python .\02_llm-api-integration\03_single-turn-call\03_gemini_sdk_single_turn.py
```
