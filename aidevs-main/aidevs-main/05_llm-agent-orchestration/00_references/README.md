# 00 References

## 읽는 순서

1. [Agent 학습 지도](./01_agent-learning-map.md)
2. [LLM·Workflow·Agent 비교](./02_llm-workflow-agent-comparison.md)
3. [Mock First 가이드](./03_mock-first-guide.md)
4. [API 계약 가이드](./04_api-contract-guide.md)
5. [Agent 보안 기초](./05_agent-security-basics.md)
6. [공통 오류](./06_common-errors.md)
7. [공식 문서](./07_official-docs.md)
8. [Mock에서 실제 연동으로 확장](./08_mock-to-real-matrix.md)
9. [OpenAI 이미지 분석과 TTS](./09_openai-multimodal-guide.md)
10. [선택 참고: LangChain Core](./10_optional-langchain-core/README.md)

Local Docker 환경과 이전 Cloud 서비스의 비교는
[00 Local Runtime](../00_local-runtime/README.md)에서 확인합니다. 실제 설치와
실행 명령은 [과정 SETUP](../SETUP.md)을 기준으로 사용합니다.

## 문서의 역할

- `00_references`는 기술을 선택하고 설계할 때 확인하는 기준입니다.
- 각 단원의 `README.md`는 예제 실행 순서와 Lab을 안내합니다.
- `SETUP.md`와 `00_local-runtime`은 환경 설치와 연결을 안내합니다.
- 라이브러리 API가 예제와 다르면 설치 버전과 공식 문서를 함께 확인합니다.
- LangChain은 선택 자료이며 필수 수업·과제·Mini Agent 단계에는 포함하지 않습니다.

## 가장 중요한 기준

```text
LLM에게는 의미 판단을 맡기고,
Python 코드에는 검증·권한·종료 조건을 맡깁니다.
```

Agent가 추천할 수 있는 것과 시스템이 실제 실행해도 되는 것은 다릅니다.
