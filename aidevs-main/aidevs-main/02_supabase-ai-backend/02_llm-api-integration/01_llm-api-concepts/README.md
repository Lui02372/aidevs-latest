# 01_llm-api-concepts

이 단원은 LLM API를 실제로 호출하기 전에 필요한 기본 개념을 정리하는 설명 전용 문서입니다.

이 폴더에서는 Python 파일을 실행하지 않습니다. 실제 Python 실행은 `03_single-turn-call`부터 진행합니다.

## 이 단원의 위치

```text
01_llm-api-concepts:
  LLM API 요청/응답 구조, message, prompt, token, parameter 개념을 문서로 이해합니다.

02_api-key-and-billing:
  API key 발급 위치, 비용/결제 확인, .env 작성, 보안 기준을 문서로 확인합니다.

03_single-turn-call:
  mock 예제를 먼저 실행한 뒤, Gemini API key가 준비된 경우 실제 단일 질문 호출을 실행합니다.

04_multi-turn-call:
  이전 대화 이력을 포함한 messages 구조를 Python 예제로 확인합니다.
```

## LLM API란 무엇인가요?

LLM API는 Python 코드나 FastAPI 서버가 Gemini, OpenAI 같은 모델 서비스에 요청을 보내고 응답을 받는 방식입니다.

```text
사용자 입력
-> Python 코드 또는 FastAPI endpoint
-> LLM API 요청
-> 모델 응답
-> 서비스 응답으로 가공
-> 사용자 화면에 표시
```

웹 서비스 입장에서는 LLM도 외부 API 중 하나입니다. 다만 일반 API와 달리 자연어 입력을 받고 자연어 또는 구조화된 텍스트를 생성한다는 특징이 있습니다.

## Prompt, Message, Response

```text
Prompt:
  모델에게 전달하는 지시문 또는 질문입니다.

Message:
  role과 content를 함께 가진 대화 단위입니다.

Response:
  모델이 생성해서 돌려주는 결과입니다.
```

간단한 질문 하나만 보내는 경우에는 prompt라는 표현을 많이 씁니다. 대화형 API에서는 보통 여러 message를 목록으로 묶어 보냅니다.

## Message 구조

LLM API는 보통 아래와 같은 메시지 구조를 사용합니다.

```json
[
  {
    "role": "system",
    "content": "당신은 Python과 FastAPI를 쉽게 설명하는 학습 도우미입니다."
  },
  {
    "role": "user",
    "content": "FastAPI에서 GET과 POST의 차이를 설명해 주세요."
  }
]
```

## Role의 의미

| role | 의미 | 예시 |
| --- | --- | --- |
| `system` | 모델이 따라야 할 기본 역할과 규칙 | 한국어로 답하기, 초보자 기준으로 설명하기 |
| `user` | 사용자가 입력한 질문이나 요청 | GET과 POST의 차이를 설명해 주세요 |
| `assistant` | 이전에 모델이 답변했던 내용 | 이전 답변을 대화 이력으로 다시 전달 |

`system` 메시지는 답변의 방향을 정합니다. 실제 서비스에서는 말투, 금지 사항, 출력 형식 같은 규칙을 여기에 넣을 수 있습니다.

`user` 메시지는 사용자가 실제로 입력한 질문입니다. Streamlit 입력창, 웹 화면, FastAPI 요청 Body에서 받은 값이 여기에 해당합니다.

`assistant` 메시지는 멀티턴 대화에서 이전 모델 답변을 다시 전달할 때 사용합니다.

## Single-turn과 Multi-turn

```text
Single-turn:
  현재 질문 하나를 중심으로 응답을 생성합니다.

Multi-turn:
  이전 사용자 질문과 모델 답변을 함께 보내서 대화 흐름을 이어 갑니다.
```

Single-turn 예시:

```text
user:
  FastAPI에서 GET과 POST의 차이를 설명해 주세요.
```

Multi-turn 예시:

```text
user:
  FastAPI에서 GET과 POST의 차이를 설명해 주세요.

assistant:
  GET은 조회, POST는 생성에 사용합니다.

user:
  그럼 PUT과 DELETE도 이어서 설명해 주세요.
```

멀티턴 대화에서는 이전 대화를 모두 계속 보낼 수 있지만, 대화가 길어질수록 token 사용량과 비용이 늘어날 수 있습니다.

## Context란 무엇인가요?

Context는 모델이 답변을 만들 때 참고해야 하는 배경 정보입니다.

```text
사용자 질문:
  이 사용자의 최근 메모를 바탕으로 할 일을 정리해 주세요.

context:
  Supabase에서 조회한 최근 메모 목록
  이전 대화 이력
  서비스 로그
  사용자가 선택한 문서 내용
```

이 과정에서는 이후 Supabase에 저장된 사용자 정보, 대화 이력, 메모 데이터를 context로 사용하는 흐름까지 확장합니다.

## Parameter의 의미

LLM API를 호출할 때는 모델 이름 외에도 응답 방식을 조절하는 값이 들어갈 수 있습니다.

| parameter | 의미 | 처음 사용할 때 권장 |
| --- | --- | --- |
| `model` | 사용할 모델 이름 | 수업 기본값 사용 |
| `temperature` | 응답의 다양성 또는 무작위성 | 낮게 시작 |
| `top_p` | 다음 단어 후보를 얼마나 넓게 볼지 조절 | 기본값 유지 |
| `max_tokens` 또는 `maxOutputTokens` | 생성할 수 있는 최대 출력 길이 | 작게 시작 |

`temperature`가 낮으면 더 안정적이고 일관된 답변을 기대할 수 있습니다. 수업 자료 설명, 코드 설명, 요약처럼 정확성이 중요한 경우 낮은 값부터 시작합니다.

`max_tokens` 또는 `maxOutputTokens`가 너무 크면 답변이 길어지고 비용과 응답 시간이 늘어날 수 있습니다.

## Token과 비용

LLM API는 보통 입력과 출력을 token 단위로 처리합니다.

```text
입력 token:
  system 메시지, user 메시지, context, 이전 대화 이력 등 모델에게 보내는 내용

출력 token:
  모델이 생성한 답변
```

입력 context가 길어지거나 출력 답변이 길어질수록 비용이 늘어날 수 있습니다. 그래서 처음에는 짧은 입력과 짧은 출력으로 실습하는 것이 좋습니다.

## Mock 예제를 먼저 사용하는 이유

실제 LLM API를 바로 호출하면 아래 문제가 생길 수 있습니다.

```text
1. API key 설정에서 막힐 수 있습니다.
2. provider 서버 상태나 호출 제한의 영향을 받을 수 있습니다.
3. 실습 중 반복 호출로 비용이 발생할 수 있습니다.
4. API 오류와 내 코드 오류를 구분하기 어려울 수 있습니다.
```

그래서 이 과정은 mock-first 방식으로 진행합니다.

```text
1. mock 응답으로 요청/응답 구조를 먼저 이해합니다.
2. FastAPI endpoint와 화면 연결 흐름을 먼저 완성합니다.
3. 이후 API key와 비용 기준을 확인한 뒤 실제 Gemini 호출로 바꿉니다.
```

## 이 단원에서 꼭 이해할 것

```text
1. LLM API는 외부 API 호출이다.
2. 메시지는 role과 content를 가진다.
3. system 메시지는 모델의 역할과 규칙을 정한다.
4. user 메시지는 실제 사용자 질문이다.
5. assistant 메시지는 이전 모델 답변을 대화 이력으로 보낼 때 사용한다.
6. single-turn은 현재 질문 중심, multi-turn은 이전 대화 포함 방식이다.
7. context가 길어질수록 token과 비용이 늘 수 있다.
8. 실제 호출 전에는 mock 예제로 구조를 먼저 확인한다.
```

## 실제 실행은 어디에서 하나요?

이 단원에서는 개념만 확인합니다. 실제 Python 파일 실행은 아래 단원부터 진행합니다.

```text
03_single-turn-call:
  01_mock_single_turn.py로 비용 없이 단일 질문 흐름을 먼저 확인합니다.
  이후 GEMINI_API_KEY가 준비된 경우 Gemini SDK 호출을 실행합니다.

04_multi-turn-call:
  이전 대화 이력을 포함한 messages 구조를 Python 예제로 확인합니다.

05_fastapi-llm-endpoint:
  FastAPI endpoint에서 LLM 호출 흐름을 연결합니다.
```

## 확인 질문

```text
1. Prompt와 message는 어떻게 다른가요?
2. system, user, assistant role은 각각 어떤 역할을 하나요?
3. single-turn과 multi-turn은 무엇이 다른가요?
4. context가 길어지면 어떤 문제가 생길 수 있나요?
5. temperature와 max_tokens는 응답에 어떤 영향을 줄 수 있나요?
6. 실제 API 호출 전에 mock 예제를 먼저 사용하는 이유는 무엇인가요?
```
