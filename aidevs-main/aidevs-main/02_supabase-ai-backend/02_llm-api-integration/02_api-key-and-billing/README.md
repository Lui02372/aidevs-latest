# 02_api-key-and-billing

이 단원은 LLM API를 실제로 호출하기 전에 필요한 **API key**, **환경변수**, **비용/결제 주의사항**, **보안 관리 기준**을 정리하는 설명 전용 문서입니다.

이 폴더에서는 Python 파일을 실행하지 않습니다. 실제 점검 실습은 이후 `10_labs/lab-02_api-key-safety-check`에서 진행합니다.

## 이 단원의 위치

```text
01_llm-api-concepts:
  실제 API 호출 없이 messages, parameter, token 개념을 이해합니다.

02_api-key-and-billing:
  API key 발급 위치, 비용/결제 확인, .env 작성, 보안 기준을 문서로 확인합니다.

03_single-turn-call:
  mock 예제를 먼저 실행한 뒤, Gemini API key가 준비된 경우 실제 단일 질문 호출을 실행합니다.

10_labs/lab-02_api-key-safety-check:
  .env에서 key를 읽고, key를 마스킹하고, 비용 안전 체크리스트를 코드로 실습합니다.
```

## 핵심 요약

```text
API key:
  코드가 LLM 서비스를 호출할 수 있도록 발급받는 비밀 키입니다.

.env:
  API key처럼 공개되면 안 되는 값을 저장하는 로컬 설정 파일입니다.

환경변수:
  Python 코드에서 os.getenv(...)로 읽어오는 설정 값입니다.

Billing:
  실제 API를 호출했을 때 사용량에 따라 비용이 발생할 수 있는 과금 체계입니다.

무료 범위와 호출 제한:
  provider, 모델, 계정 상태, 시점에 따라 달라질 수 있으므로 반드시 공식 화면에서 확인합니다.
```

## 이 과정의 LLM 사용 기준

```text
Gemini:
  02_llm-api-integration의 기본 LLM 실습 provider입니다.
  기본 모델 예시는 gemini-2.5-flash-lite를 사용합니다.

OpenAI:
  선택/비교 실습 provider입니다.
  OpenAI 예제 파일은 유지하지만 필수 실습은 아닙니다.
  기본 모델 예시는 gpt-4.1-mini를 사용합니다.
```

중요한 점은 **ChatGPT/Codex 앱 사용 결제와 OpenAI API 사용 결제는 별개**라는 것입니다. 앱에서 결제했더라도 API 호출 비용이 자동으로 포함되는 것이 아닐 수 있으므로, API 사용 전 OpenAI Platform의 Billing, Usage, Limits 화면을 별도로 확인해야 합니다.

## Gemini API key 준비 위치

Gemini API key는 Google AI Studio에서 발급받을 수 있습니다.

| 확인할 것 | 공식 위치 |
| --- | --- |
| Google AI Studio | https://aistudio.google.com/ |
| Gemini API key 생성 | https://aistudio.google.com/apikey |
| Gemini API 문서 | https://ai.google.dev/gemini-api/docs |
| Gemini API 가격/제한 | https://ai.google.dev/gemini-api/docs/pricing |

진행 흐름은 다음과 같습니다.

```text
1. Google 계정으로 Google AI Studio에 접속합니다.
2. API key 생성 화면으로 이동합니다.
3. 새 API key를 생성합니다.
4. 복사한 key를 코드에 직접 붙여 넣지 않습니다.
5. C:\aidev\02_supabase-ai-backend\.env 파일에 저장합니다.
```

## OpenAI API key, 결제, 사용량 확인 위치

OpenAI API는 선택/비교 실습에서 사용합니다.

| 확인할 것 | 공식 위치 |
| --- | --- |
| OpenAI Platform | https://platform.openai.com/ |
| OpenAI API keys | https://platform.openai.com/api-keys |
| OpenAI Billing | https://platform.openai.com/settings/organization/billing |
| OpenAI Usage | https://platform.openai.com/usage |
| OpenAI Limits | https://platform.openai.com/settings/organization/limits |
| OpenAI API Pricing | https://openai.com/api/pricing/ |

OpenAI를 사용할 때는 아래 항목을 확인합니다.

```text
1. OpenAI Platform에 로그인했는가?
2. API key를 발급했는가?
3. Billing에서 결제 수단과 크레딧 상태를 확인했는가?
4. Usage에서 현재 사용량을 확인할 수 있는가?
5. Limits에서 프로젝트/조직의 호출 제한과 사용 한도를 확인했는가?
6. OPENAI_API_KEY를 .env에만 저장하고 GitHub에 올리지 않는가?
```

## .env 파일 작성 예시

`C:\aidev\02_supabase-ai-backend\.env` 파일에 아래 형식으로 작성합니다.

```env
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite

OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

OpenAI API를 사용하지 않을 경우 `OPENAI_API_KEY`는 비워 두어도 됩니다.

```env
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

`your-gemini-api-key`, `your-openai-api-key`처럼 예시로 적어 둔 값은 실제 key가 아닙니다. 실제 호출이 필요한 단원에서는 placeholder가 아닌 실제 key가 필요합니다.

## .gitignore와 key 유출 주의

`.env` 파일은 GitHub에 올라가면 안 됩니다.

이 저장소에는 이미 아래 제외 규칙이 들어 있습니다.

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
```

확인 위치:

```text
C:\aidev\.gitignore
C:\aidev\02_supabase-ai-backend\.gitignore
```

API key가 GitHub, README, 코드, 화면 공유, 강의 녹화에 노출되면 즉시 해당 key를 삭제하거나 재발급해야 합니다.

## 실제 API 호출 전 체크리스트

실제 Gemini 또는 OpenAI API를 호출하기 전에 아래를 확인합니다.

```text
1. .env에 key를 저장했는가?
2. key를 코드나 README에 직접 적지 않았는가?
3. .env가 .gitignore에 포함되어 있는가?
4. 공식 가격/무료 범위/호출 제한 화면을 확인했는가?
5. max_tokens 또는 maxOutputTokens를 너무 크게 잡지 않았는가?
6. 반복문 안에서 실제 API를 무제한 호출하지 않는가?
7. 오류 발생 시 재시도 횟수를 제한했는가?
8. 화면 공유 중 API key가 보이지 않는가?
9. OpenAI API 결제와 ChatGPT/Codex 앱 결제가 별개임을 이해했는가?
```

## 비용을 줄이는 기본 습관

```text
1. 처음에는 mock 예제로 구조를 확인합니다.
2. 실제 API 호출은 작은 입력과 짧은 출력부터 시작합니다.
3. 같은 질문을 반복 호출하지 않도록 합니다.
4. 테스트 중에는 max_tokens 또는 maxOutputTokens를 작게 둡니다.
5. 반복문, 배치 처리, 자동 재시도 코드를 조심합니다.
6. 오류 발생 시 무한 재시도하지 않습니다.
7. 사용량 대시보드를 자주 확인합니다.
```

## 실습은 어디에서 하나요?

이 단원에서는 설명만 확인합니다. 실제로 `.env`를 읽고 key를 마스킹하는 실습은 아래 lab에서 진행합니다.

```text
02_llm-api-integration/10_labs/lab-02_api-key-safety-check
```

해당 lab에서 연습할 내용:

```text
1. .env 파일 읽기
2. GEMINI_API_KEY, OPENAI_API_KEY 설정 여부 확인
3. API key 전체를 출력하지 않고 일부만 마스킹하기
4. 실제 호출 전 비용 안전 체크리스트 출력하기
```

## 이후 단원과의 연결

```text
03_single-turn-call:
  Gemini API key가 있으면 실제 단일 질문 호출을 실행합니다.

04_multi-turn-call:
  이전 대화 이력을 포함한 메시지 구조를 실습합니다.

05_fastapi-llm-endpoint:
  FastAPI endpoint에서 key를 읽고 LLM API를 호출합니다.

04_supabase-ai-mini-project:
  사용자별 대화 이력, 응답 저장, SSE 스트리밍 흐름과 연결합니다.
```

## 확인 질문

```text
1. API key를 코드에 직접 적으면 왜 위험한가요?
2. .env와 .gitignore는 각각 어떤 역할을 하나요?
3. Gemini API와 OpenAI API를 이 과정에서 어떻게 구분해서 사용하나요?
4. ChatGPT/Codex 앱 결제와 OpenAI API 결제는 왜 별도로 봐야 하나요?
5. 실제 API 호출 전에 비용을 줄이기 위해 어떤 습관이 필요한가요?
6. API key가 유출되었다면 어떤 조치를 해야 하나요?
```
