# LLM API Cheatsheet

LLM API는 Python 코드나 FastAPI 서버에서 AI 모델에게 질문을 보내고 응답을 받는 방법입니다.

ChatGPT 화면에 직접 질문을 입력하는 것과 달리, API를 사용하면 우리 서비스 안에서 AI 응답을 자동으로 만들 수 있습니다.

## 기본 흐름

```text
사용자 질문
-> Python 코드 또는 FastAPI endpoint
-> LLM API 요청
-> 모델 응답 생성
-> 응답 구조 정리
-> 사용자 화면 또는 API 응답으로 반환
```

## 이 단원에서 사용하는 기준

| 구분 | 기준 |
| --- | --- |
| 기본 provider | Gemini |
| 기본 모델 예시 | `gemini-2.5-flash-lite` |
| OpenAI 선택 모델 예시 | `gpt-4.1-mini` |
| 기본 실습 방식 | mock 응답으로 구조 먼저 이해 |
| 실제 호출 여부 | `actual_api_called` 값으로 표시 |

## 핵심 용어

| 용어 | 의미 |
| --- | --- |
| Model | 응답을 생성하는 AI 모델입니다. |
| Provider | 모델을 제공하는 서비스입니다. 예: Gemini, OpenAI |
| Prompt | 모델에게 보내는 지시문이나 질문입니다. |
| Message | `role`과 `content`로 구성된 대화 한 줄입니다. |
| Token | 모델이 입력과 출력을 처리하는 단위입니다. |
| Temperature | 응답의 다양성과 예측 가능성을 조절합니다. |
| Max tokens | 모델이 생성할 수 있는 최대 출력 길이를 제한합니다. |
| Mock | 실제 API를 호출하지 않고 가짜 응답으로 구조를 연습하는 방식입니다. |

## Single-turn과 Multi-turn

Single-turn은 현재 질문 하나만 보내는 방식입니다.

```text
user: FastAPI가 뭐야?
assistant: FastAPI는 Python 웹 API 프레임워크입니다.
```

Multi-turn은 이전 대화 이력까지 함께 보내는 방식입니다.

```text
user: FastAPI가 뭐야?
assistant: FastAPI는 Python 웹 API 프레임워크입니다.
user: 그럼 Swagger는 어떤 역할을 해?
assistant: Swagger는 API 문서를 웹 화면에서 확인하고 테스트하게 해줍니다.
```

중요한 점은 AI가 이전 대화를 자동으로 기억하는 것이 아니라, 우리가 이전 메시지를 다시 API 요청에 포함해야 한다는 것입니다.

## Supabase와 연결되는 지점

이 단원에서는 대화 이력을 메모리 리스트나 mock 데이터로 다룹니다. 다음 단원부터는 이 대화 이력을 Supabase 테이블에 저장하는 흐름으로 확장합니다.
