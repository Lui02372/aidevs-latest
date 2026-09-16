# 02_prompt-input-and-response

사용자 프롬프트를 입력받고 mock 응답을 생성하는 기본 흐름을 학습합니다.

이 챕터에서는 프롬프트 문장 자체와 화면 표시 흐름을 먼저 다룹니다. 실제 LLM API 호출, 토큰 비용, 모델 파라미터는 `02_supabase-ai-backend`에서 이미 학습한 내용을 바탕으로 하고, 여기서는 응답을 화면에 잘 보여주는 역할에 집중합니다.

## 학습 목표

- 빈 질문을 검증할 수 있습니다.
- mock 응답 생성 함수를 화면 코드와 분리할 수 있습니다.
- 응답 템플릿을 사용해 assistant 메시지를 만들 수 있습니다.
- 옵션에 따라 응답 문구가 달라지는 화면을 만들 수 있습니다.
- 응답 생성 중 로딩 상태나 안내 문구를 표시할 수 있습니다.

## 예제 파일

```text
01_prompt-validation.py
02_mock-ai-response.py
03_response-template.py
04_prompt-options.py
```

## 실행 예시

```powershell
cd C:\aidev\03_supabase-ai-frontend
.\.venv\Scripts\Activate.ps1
streamlit run .\05_ai-chatbot-interface\02_prompt-input-and-response\02_mock-ai-response.py
```

## 확인할 내용

- 빈 질문을 처리할 수 있는가?
- 응답 생성 함수를 화면 코드와 분리할 수 있는가?
- 옵션에 따라 응답 방식이 달라지는가?
- 응답 생성 중 사용자에게 로딩 상태 또는 안내 문구를 보여줄 수 있는가?

## 이후 과정과 연결

이 폴더의 mock 응답 함수는 이후 백엔드 chat API 호출 함수로 바꿀 수 있습니다. 실제 Gemini/OpenAI 호출은 프론트엔드가 아니라 FastAPI 백엔드에서 처리합니다.
