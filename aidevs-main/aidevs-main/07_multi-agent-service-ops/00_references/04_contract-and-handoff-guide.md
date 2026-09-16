# Agent Contract와 Handoff

## Contract

각 Agent는 다음을 문서와 Pydantic Schema로 정의합니다.

- 역할
- 입력
- 출력
- 허용 Tool
- 금지 행동
- 실패 형식

## Handoff

Handoff는 전체 대화 복사가 아니라 다음 담당자에게 필요한 최소 Context와 책임을
전달하는 작업입니다.

금지 항목:

- API Key와 Secret
- 필요하지 않은 개인정보
- 다른 사용자의 데이터
- 이미지 원본과 큰 Base64 데이터

