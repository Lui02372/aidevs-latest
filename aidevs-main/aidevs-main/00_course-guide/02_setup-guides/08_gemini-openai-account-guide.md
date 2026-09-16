# 08. Gemini/OpenAI 계정과 비용 가이드

이 과정에서는 초반 LLM API 실습의 기본 모델로 Gemini를 사용합니다. OpenAI는 선택 비교 예제와 05 이후 Agent 실습에서 사용할 수 있습니다.

API 호출은 비용 또는 사용량 제한이 있을 수 있으므로, key 발급 전에 공식 화면에서 무료 범위, 결제, 사용량 제한을 확인합니다.

## 1. Gemini API Key 준비

공식 사이트:

```text
Google AI Studio: https://aistudio.google.com/
Gemini API Key: https://aistudio.google.com/app/apikey
Gemini API 문서: https://ai.google.dev/gemini-api/docs
Gemini 가격: https://ai.google.dev/gemini-api/docs/pricing
Gemini Rate Limits: https://ai.google.dev/gemini-api/docs/rate-limits
```

진행 순서:

```text
1. Google 계정으로 Google AI Studio에 로그인합니다.
2. API Key 메뉴로 이동합니다.
3. Create API key를 누릅니다.
4. 발급된 key를 복사합니다.
5. 과정 폴더의 .env 파일에 GEMINI_API_KEY로 저장합니다.
```

예시:

```env
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.5-flash-lite
```

주의:

```text
GEMINI_API_KEY를 README에 적지 않습니다.
GitHub에 올리지 않습니다.
화면 캡처에 key 전체가 보이지 않게 합니다.
호출 제한 또는 503 오류가 날 수 있으므로 수업 중 과도하게 반복 호출하지 않습니다.
```

## 2. OpenAI API Key 준비

공식 사이트:

```text
OpenAI Platform: https://platform.openai.com/
API Keys: https://platform.openai.com/api-keys
Usage: https://platform.openai.com/usage
Billing help: https://help.openai.com/en/collections/3675945-understanding-openai-api-billing-and-usage
```

진행 순서:

```text
1. OpenAI Platform에 로그인합니다.
2. API Keys 화면으로 이동합니다.
3. 새 API key를 생성합니다.
4. 필요한 프로젝트 또는 조직이 맞는지 확인합니다.
5. Billing/Usage 화면에서 결제와 사용량을 확인합니다.
6. .env 파일에 OPENAI_API_KEY로 저장합니다.
```

예시:

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

## 3. ChatGPT 구독과 API 결제는 다릅니다

ChatGPT Plus/Pro/Business 구독이 있어도 API 사용량은 별도로 과금될 수 있습니다.

확인할 것:

```text
[ ] OpenAI Platform에 로그인했다.
[ ] API key를 발급했다.
[ ] Billing/Usage 화면을 확인했다.
[ ] 월 사용량 한도 또는 예산 기준을 확인했다.
[ ] API key를 .env에만 저장했다.
```

## 4. 수업 중 비용 안전 기준

```text
1. 처음에는 mock 예제로 흐름을 확인합니다.
2. 실제 API 호출은 필요한 예제에서만 실행합니다.
3. 반복 실행 전에 모델명과 호출 횟수를 확인합니다.
4. 오류가 났다고 무한 반복 실행하지 않습니다.
5. key를 GitHub, README, 발표 자료, 로그에 노출하지 않습니다.
```

## 5. 자주 나는 문제

| 문제 | 확인할 것 |
| --- | --- |
| API key가 없다는 오류 | `.env` 파일 위치와 변수 이름 |
| 인증 오류 | key 복사 누락, 잘못된 프로젝트 key |
| 결제 오류 | Billing 설정, 사용량 한도 |
| rate limit 오류 | 잠시 후 재실행, 호출 횟수 줄이기 |
| Gemini 503 오류 | 모델 수요 증가, 잠시 후 재시도, 모델 변경 |

