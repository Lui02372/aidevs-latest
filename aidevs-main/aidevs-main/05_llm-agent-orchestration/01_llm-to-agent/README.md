# 01 LLM to Agent

## 학습 목표

- 일반 LLM, 고정 Workflow, Agent를 구분합니다.
- LLM이 필요한 판단과 Python 규칙을 구분합니다.
- Agent가 항상 더 좋은 선택은 아니라는 점을 설명합니다.
- 작은 Python 판단 함수를 Backend API와 Frontend 메뉴로 연결할 수 있습니다.

## 이번 단원의 핵심 구분

```text
LLM       입력을 보고 텍스트나 구조화 결과를 생성
Workflow  사람이 정한 고정 순서와 규칙으로 실행
Agent     현재 상태를 보고 다음 행동을 선택하고 결과를 관찰
```

`01_concept_example.py`의 의미 기반 Mock Router는 LLM 판단을 흉내 내는 중간
예제이며 완성된 Agent 전체가 아닙니다. 이후 Tool, 상태, 반복 제한을 추가하면서
Agent 구조로 확장합니다.

## 실행

### 필수 개념 예제

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\07_multimodal_travel_example.py
```

### 선택형 실제 Provider 예제

```powershell
python .\03_optional_openai_example.py
python .\04_real_provider_call.py
python .\05_openai_image_analysis.py .\travel.jpg
python .\06_openai_tts.py
```

`01`, `02`, `07`은 API Key 없이 개념을 확인합니다. `04`는 아직 완성된
Backend를 구현하는 실습이 아니라 Backend Provider API를 연결한 뒤 다시 실행하는
비교 예제입니다. 이 예제는 GPT·Gemini·Ollama/Llama를 같은 입력으로
호출합니다. 설정하지 않은
Provider의 실패도 정상적인 비교 결과로 관찰합니다.

## 예제

| 파일 | 내용 |
| --- | --- |
| `01_concept_example.py` | 고정 규칙과 의미 기반 분류 비교 |
| `02_travel_example.py` | 여행 문의를 작업 유형으로 분류 |
| `03_optional_openai_example.py` | 선택형 OpenAI Responses API 호출 |
| `04_real_provider_call.py` | Backend를 통한 GPT·Gemini·Ollama 비교 |
| `05_openai_image_analysis.py` | 이미지 입력과 Pydantic 분석 |
| `06_openai_tts.py` | 여행 안내문 MP3 생성 |
| `07_multimodal_travel_example.py` | 이미지 분석과 Agent·TTS의 역할 구분 |

`05`, `06`은 실제 OpenAI API 호출이므로 `OPENAI_API_KEY`가 필요합니다.
`07`은 이미지 원본을 Agent State에 저장하지 않는 연결 원칙을 설명하는
로컬 예제입니다.

## 세 Provider의 역할

| Provider | 이 과정에서의 역할 |
| --- | --- |
| Gemini | 이전 과정에서 사용한 Cloud LLM 기준점 |
| OpenAI GPT | Responses API와 이미지 분석·TTS 선택 확장 |
| Ollama/Llama | Docker 기반 Local LLM과 Cloud·Local 비교 |

실제 Provider 비교는 `Gemini → GPT → Ollama/Llama` 순서로 진행합니다. Provider가
바뀌어도 요청과 응답 계약은 유지하고, 응답 내용·모델·지연·실패를 비교합니다.

## Mini Agent 01 연결

단위 예제를 실행한 뒤 `C:\mini_agent_st\mini_agent_01_llm`에서 같은 기능을
Backend와 Frontend로 연결합니다.

```text
01_concept_example.py
→ LLM·Workflow·Agent 비교 메뉴

02_travel_example.py
→ 여행 요청 분류 메뉴
→ 정보 부족과 추가 질문 메뉴

03_optional_openai_example.py
→ 실제 LLM 호출 메뉴

04_real_provider_call.py
→ Provider 비교 메뉴
```

이미지 분석과 TTS 서비스 연결은 Structured Output을 학습한 뒤
`mini_agent_01_llm`의 `1-5 이미지 분석`, `1-6 음성 생성` 화면에서 진행합니다.

## 확인 질문

1. 이 문제는 조건문만으로 충분한가요?
2. 잘못 분류되었을 때 위험은 무엇인가요?
3. confidence가 낮으면 어떤 경로로 보내야 하나요?
