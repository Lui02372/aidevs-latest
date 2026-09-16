# Token Cost Safety Guide

LLM API는 사용량에 따라 비용이 발생할 수 있습니다.

이 문서는 실제 Gemini/OpenAI API를 호출하기 전에 확인해야 하는 안전 기준을 정리합니다.

## token이란?

Token은 모델이 텍스트를 처리하는 단위입니다. 정확히 글자 수나 단어 수와 같지는 않지만, 초보 단계에서는 “모델이 읽고 쓰는 조각”이라고 이해하면 됩니다.

```text
입력 token:
  사용자 질문, system prompt, 이전 대화 이력, 참고 문서

출력 token:
  모델이 생성한 답변
```

입력과 출력이 길어질수록 비용이 늘어날 수 있습니다.

## 비용이 늘어나는 상황

```text
긴 질문을 보낼 때
긴 문서를 통째로 보낼 때
이전 대화 이력을 계속 누적해서 보낼 때
max_tokens를 너무 크게 설정할 때
반복문 안에서 실제 API를 여러 번 호출할 때
```

## API key 안전 기준

```text
API key는 코드에 직접 적지 않습니다.
API key는 .env 파일이나 환경 변수로 관리합니다.
.env 파일은 GitHub에 올리지 않습니다.
your-... 형태의 placeholder key는 실제 key로 보지 않습니다.
화면 공유 중에는 API key가 보이지 않도록 주의합니다.
```

## 실제 호출 전 체크리스트

```text
1. 이 예제가 mock인지 실제 호출인지 확인했습니다.
2. actual_api_called 값이 어떤 의미인지 확인했습니다.
3. API key가 .env에만 저장되어 있습니다.
4. 무료 한도와 결제 상태를 확인했습니다.
5. 반복문에서 실제 API를 여러 번 호출하지 않습니다.
6. max_tokens를 필요한 만큼만 설정했습니다.
```

## 과제 제출 기준

과제 제출 시 실제 API key를 포함하면 안 됩니다.

제출 코드에는 다음과 같은 구조를 권장합니다.

```python
response = {
    "provider": "gemini",
    "model": "gemini-2.5-flash-lite",
    "actual_api_called": False,
    "answer": "mock 응답입니다.",
}
```

실제 호출 코드를 작성하더라도 key가 없으면 안내 메시지를 출력하고 안전하게 종료하도록 만듭니다.
