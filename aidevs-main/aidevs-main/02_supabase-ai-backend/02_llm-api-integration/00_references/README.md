# 00_references

`02_llm-api-integration` 단원에서 자주 확인하는 개념 문서입니다.

이 폴더는 암기용 문서가 아니라, 실습 중 헷갈리는 용어를 빠르게 다시 확인하기 위한 참고 자료입니다. 처음부터 모든 내용을 외우기보다 예제를 실행하면서 필요한 문서를 찾아보는 방식으로 사용합니다.

## 문서 목록

| 문서 | 확인할 내용 |
| --- | --- |
| `llm-api-cheatsheet.md` | LLM API 전체 흐름과 핵심 용어 |
| `message-format-guide.md` | `system`, `user`, `assistant` 메시지 구조 |
| `parameter-guide.md` | `temperature`, `top_p`, `max_tokens` 의미 |
| `model-parameter-comparison-guide.md` | Gemini, OpenAI, mock 사용 기준 |
| `token-cost-safety-guide.md` | token, 비용, API key 안전 기준 |

## 이 단원의 기준

```text
기본 provider: Gemini
기본 Gemini 모델 예시: gemini-2.5-flash-lite
OpenAI 선택 모델 예시: gpt-4.1-mini
기본 실습 방식: mock-first
실제 호출 여부 표시: actual_api_called
```

## 읽는 순서

1. LLM API가 처음이면 `llm-api-cheatsheet.md`를 봅니다.
2. message 구조가 헷갈리면 `message-format-guide.md`를 봅니다.
3. 응답 길이와 창의성 설정이 헷갈리면 `parameter-guide.md`를 봅니다.
4. Gemini와 OpenAI의 역할을 구분하려면 `model-parameter-comparison-guide.md`를 봅니다.
5. 실제 API 호출 전에는 `token-cost-safety-guide.md`를 반드시 확인합니다.
