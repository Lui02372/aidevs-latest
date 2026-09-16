# 00 Runtime and Deployment

Multi AI Agent와 Orchestration을 배우기 전 실행 환경을 준비하고, 09에서 사용할 배포
개념을 미리 찾아볼 수 있는 안내서입니다. 첫날에는 Redis·PostgreSQL·Ollama만 준비하고
Docker Image·AWS·CI/CD는 서비스 구조를 이해한 뒤 09에서 진행합니다.

Multi AI Agent는 넣지 않습니다. 이번 목표는 Browser·Backend·실제 LLM·Redis·PostgreSQL이 어디에서 실행되고 어떻게 연결되는지 이해하는 것입니다.

## 이 단원을 언제 진행하나요?

00 전체를 첫날 한 번에 진행하지 않습니다. 초보자는 필요한 시점에 세 구간으로 나누어
진행하는 것이 좋습니다.

| 시점 | 필수 범위 | 완료 기준 |
| --- | --- | --- |
| 과정 시작 전 | Windows·Docker 확인, `00_local-services` | Redis·PostgreSQL이 `healthy` |
| 08 시작 전 | `01_simple-multi-llm-compose` 선택 복습 | Browser→Backend→저장소 연결 확인 |
| 09 진행 중 | Docker·CI·AWS·장애 실습 | Health·배포·복구와 리소스 정리 완료 |

AWS 계정이 없어도 01~09의 로컬 학습은 가능합니다. Ollama도 선택 사항이며 OpenAI나
Gemini 중 하나를 사용할 수 있으면 로컬 Model을 내려받지 않아도 됩니다.

## 시작 전에 확인하세요

```text
[ ] Python 3.11 이상과 Git을 사용할 수 있다.
[ ] Docker Desktop 설치 권한과 관리자 PowerShell 사용 가능 여부를 확인했다.
[ ] OpenAI·Gemini·Ollama 중 사용할 Provider를 하나 정했다.
[ ] AWS 실습 여부와 계정의 Region·예산 정책을 확인했다.
[ ] AWS 실습 종료 후 리소스를 정리할 시간을 확보했다.
```

문제가 생기면 명령을 반복하기 전에 실패 계층을 구분합니다.

```text
명령을 찾지 못함 → 설치·PATH
Container가 시작되지 않음 → Docker·Port·환경 변수
Health 실패 → Backend Log와 저장소 연결
LLM 요청 실패 → Provider Key·Model·Ollama 상태
외부 Browser 접속 실패 → EC2 Public IP·Security Group·Service Port
```

## 학습 순서

| 순서 | 폴더 | 핵심 내용 |
| ---: | --- | --- |
| 00 | `00_local-services` | Redis·PostgreSQL·Ollama 로컬 준비 |
| 01 | `01_simple-multi-llm-compose` | OpenAI·Gemini·Ollama 선택형 Chat과 네 Container |
| 02 | `02_github-actions-ci` | 09 CI/CD를 위한 사전 참고 자료 |
| 03 | `03_aws-ec2` | 09 AWS 배포의 기초가 되는 EC2 수동 실습 |
| 04 | `04_github-actions-aws-deploy` | 09 이후 선택 가능한 EC2 자동 배포 |
| 05 | `05_weather-mcp-deployment-project` | 실제 Weather MCP를 포함한 최소 CI/CD·AWS 배포 프로젝트 |
| 06 | `06_weather-mcp-stateful-deployment` | PostgreSQL·Redis 인프라와 Application 배포 분리 |
| 참고 | `05_local-or-managed-cloud.md` | 로컬·AWS·관리형 Cloud 경로 비교 |
| 연결 | `06_to-integrated-operations.md` | 00 Runtime에서 09 통합 운영으로 연결 |

## 공통 구조

```text
Browser
→ Streamlit
→ FastAPI
   ├─ 실제 OpenAI·Gemini·Ollama 중 명시적으로 선택
   ├─ Redis: 현재 Session
   └─ PostgreSQL: 여행 메모와 전체 Chat 이력
```

Provider 오류를 Mock 성공으로 숨기지 않습니다. 최소 한 개의 실제 Provider만 설정해도 학습할 수 있습니다.

## 두 실행 환경을 구분하세요

| 환경 | 목적 | Redis·PostgreSQL | Ollama |
| --- | --- | --- | --- |
| `00_local-services` | 01~09와 Mini Project 개발 공용 | Host `6379`·`5433` | Host `11434` |
| `01_simple-multi-llm-compose` | Container 연결을 복습하는 독립 서비스 | Compose 내부 `6379`·`5432` | 선택 Profile 내부 `11434` |

두 환경을 동시에 실행할 필요가 없습니다. 00 공용 환경은 과정 개발용이고, 01은 배포할 애플리케이션과 의존성을 하나의 Compose로 묶는 실습입니다.

## 초보자 권장 진행 방식

각 단계에서 실행한 명령, 정상 출력, 첫 오류 문장, 복구 후 데이터 유지 여부를
기록합니다. 명령 실행 자체보다 `docker compose ps`, Health 응답, Container Log를
근거로 현재 상태를 설명할 수 있어야 다음 단계로 넘어갑니다. 전체 운영 순서는
[`LEARNING_SEQUENCE.md`](./LEARNING_SEQUENCE.md)를 참고합니다.

## 다음 단계

00은 실행 기반을 준비합니다. 01부터 역할 분리와 Orchestration을 학습하고, 08에서
관측 가능한 서비스를 만든 뒤 09에서 Docker·AWS·CI/CD·Auto Healing을 통합합니다.
