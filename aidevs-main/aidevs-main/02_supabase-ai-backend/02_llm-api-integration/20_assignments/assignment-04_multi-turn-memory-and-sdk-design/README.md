# Assignment 04. Multi-turn memory and SDK design

AI 챗봇은 사용자의 이전 질문과 AI의 이전 답변을 참고해야 자연스럽게 이어지는 답변을 만들 수 있습니다.

이 과제에서는 대화 이력을 리스트로 관리하고, 최근 메시지를 LLM 요청 구조로 변환하는 코드를 작성합니다. 실제 호출은 필수가 아니지만, Gemini SDK의 `contents` 구조로 바꾸기 쉬운 형태를 함께 설계합니다.

## 제출 목표

- `Message` 구조를 `role`, `content` 중심으로 설계합니다.
- 사용자 메시지와 AI 메시지를 순서대로 저장합니다.
- 최근 대화만 잘라서 LLM 요청에 사용합니다.
- 이후 Supabase에 저장하기 쉬운 형태로 대화 이력을 정리합니다.
- Gemini SDK에서는 이전 AI 답변을 `role="model"` 형태로 보낼 수 있음을 README에 정리합니다.

## 제출 파일

```text
starter.py 또는 main.py
README.md
```

## 실행 예시

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\20_assignments\assignment-04_multi-turn-memory-and-sdk-design\starter.py
```

## 완성 기준

1. 대화 이력이 시간 순서대로 저장됩니다.
2. 최근 메시지만 골라 요청에 사용할 수 있습니다.
3. 마지막 사용자 질문을 기준으로 mock 응답을 생성합니다.
4. README에 Supabase 저장 시 필요한 컬럼 예시를 정리합니다.
5. README에 `04_multi-turn-call/02_gemini_sdk_multi_turn_small.py`와 `04_multi-turn-call/03_gemini_sdk_multi_turn.py`로 확장하는 기준을 정리합니다.
