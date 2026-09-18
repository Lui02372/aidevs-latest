# 현재 구성 검증 — 2026-09-16

사용자 요청에 따라 Bedrock을 런타임·화면·환경 설정에서 제외했습니다.
기본 provider는 OpenAI이며 Gemini를 선택할 수 있습니다. EC2·GitHub OIDC·S3·SSM 배포는 유지합니다.
폴더와 workflow 파일 경로의 기존 bedrock 명칭은 경로 호환성을 위해 유지했습니다.

| 검사 | 결과 | 근거 |
| --- | --- | --- |
| Backend 자동 테스트 | PASS | pytest 11개 통과 |
| OpenAI·Gemini 요청 구성 | PASS | Fake client로 resource·skill 전달과 응답 처리 검증 |
| 기본 provider·입력 검증 | PASS | 기본 openai, 제외된 bedrock 요청은 422 |
| MCP·Cache·실패·저장 계약 | PASS | 실제 in-process MCP HTTP resource 왕복과 기존 회귀 테스트 |
| Python·YAML·IAM JSON | PASS | AST·YAML 파싱·IAM 예시 JSON 파싱 |
| 실제 Compose 설정 검사 | PASS | Infrastructure·Application config --quiet 성공 |
| PostgreSQL 설정 보존 | PASS | 변경 전후 .env의 DB 사용자·비밀번호·DB·URL 동일 |
| 실제 LLM 호출 | 미실행 | 현재 OpenAI·Gemini API 키가 모두 비어 있음 |
| 화면·Docker 이미지 빌드·EC2 배포 | 미실행 | 이번 변경에서는 수행하지 않음 |

검증 명령:

```powershell
.\.venv\Scripts\python.exe -m pytest backend -q -p no:cacheprovider
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.application.yml config --quiet
```

Starlette/httpx와 AnyIO의 deprecation 경고 2개가 있었으며 테스트 실패는 없습니다.
이전 구성의 검증 문서는 로컬 .local/docs-before-removing-bedrock에 보존했습니다.
실제 LLM 사용은 선택한 provider의 API 키를 .env에 넣고 Backend를 재시작한 뒤 확인합니다.
