# Lab 04. Multi-turn mock to Gemini SDK

Multi-turn 호출은 이전 대화 내용을 함께 보내서 AI가 문맥을 이어가도록 만드는 구조입니다.

이 실습에서는 대화 이력을 리스트로 관리하고, 최근 메시지를 LLM 요청에 포함하는 흐름을 연습합니다. 실제 서비스에서는 이 대화 이력이 Supabase에 저장되고, Gemini SDK 호출에 전달됩니다.

## 학습 목표

- `user`, `assistant` 메시지를 순서대로 저장합니다.
- 최근 대화만 잘라서 요청 메시지로 구성합니다.
- 대화 이력을 Supabase 저장 대상 데이터로 바라봅니다.
- Gemini SDK로 확장할 때 `assistant` 역할이 Gemini의 `model` 역할로 변환될 수 있음을 이해합니다.

## 실행

```powershell
cd C:\aidev\02_supabase-ai-backend
.\.venv\Scripts\Activate.ps1
python .\02_llm-api-integration\10_labs\lab-04_multi-turn-mock-to-gemini-sdk\starter.py
```

## Gemini SDK 확장 기준

```text
현재 lab:
  conversation 리스트
  -> 최근 메시지 선택
  -> mock 응답 생성

실제 프로젝트:
  Supabase 대화 이력 조회
  -> Gemini SDK가 받을 수 있는 contents 구조로 변환
  -> 04_multi-turn-call/02_gemini_sdk_multi_turn_small.py로 최소 호출 확인
  -> 04_multi-turn-call/03_gemini_sdk_multi_turn.py로 오류 안내 포함 구현 확인
```
