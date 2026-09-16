# Message Format Guide

LLM API는 보통 메시지 목록을 사용해 대화를 표현합니다.

메시지 한 개는 대체로 `role`과 `content`로 구성됩니다.

```python
{"role": "user", "content": "FastAPI가 뭐야?"}
```

## role의 의미

| role | 의미 |
| --- | --- |
| `system` | AI의 역할, 말투, 규칙을 정합니다. |
| `user` | 사용자의 질문이나 요청입니다. |
| `assistant` | AI가 이전에 답한 내용입니다. |

## Single-turn 메시지 예시

```python
messages = [
    {
        "role": "system",
        "content": "너는 Python 백엔드를 쉽게 설명하는 튜터입니다.",
    },
    {
        "role": "user",
        "content": "FastAPI가 뭐야?",
    },
]
```

## Multi-turn 메시지 예시

```python
messages = [
    {
        "role": "system",
        "content": "너는 Python 백엔드를 쉽게 설명하는 튜터입니다.",
    },
    {
        "role": "user",
        "content": "FastAPI가 뭐야?",
    },
    {
        "role": "assistant",
        "content": "FastAPI는 Python으로 API 서버를 만들 때 사용하는 웹 프레임워크입니다.",
    },
    {
        "role": "user",
        "content": "그럼 Pydantic은 왜 같이 써?",
    },
]
```

## Provider별 메시지 형식 차이

LLM provider마다 내부 메시지 형식은 조금씩 다를 수 있습니다. 예를 들어 어떤 API에서는 이전 AI 응답을 `assistant`가 아니라 `model` 역할로 표현하는 경우가 있습니다.

따라서 실습에서는 다음처럼 구분합니다.

```text
먼저 이해할 공통 구조:
  system / user / assistant

실제 provider에 보낼 때:
  provider가 요구하는 SDK 또는 API 형식으로 변환
```

처음에는 공통 구조로 이해하고, 실제 provider에 보낼 때 SDK가 요구하는 형식으로 변환한다고 생각하면 쉽습니다.

## 저장 관점

Supabase에 대화 이력을 저장할 때는 최소한 다음 정보가 있으면 좋습니다.

```text
conversation_id
role
content
model
created_at
```

나중에 사용자별 대화 이력을 조회하려면 `user_id`도 함께 저장합니다.
