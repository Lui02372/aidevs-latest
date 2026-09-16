# GitHub Actions 가이드

GitHub Actions는 GitHub에 코드를 올렸을 때 자동으로 테스트, 빌드, 배포 같은 작업을 실행하는 기능입니다. 07~08 과정에서는 FastAPI 서비스 테스트, Docker 이미지 빌드, AWS 배포 흐름을 이해하기 위해 사용합니다.

공식 문서:

- [GitHub Actions 문서](https://docs.github.com/actions)
- [GitHub Actions secrets 사용](https://docs.github.com/actions/security-guides/using-secrets-in-github-actions)

## 1. 언제 필요한가

| 과정 | 사용 목적 |
| --- | --- |
| 07_multi-agent-service-ops | 테스트 자동화, Docker 빌드, AWS 배포 파이프라인 |
| 08_multi-agent-service-mini-project | 최종 프로젝트 배포와 결과 검증 |

01~06 과정에서는 GitHub Actions를 반드시 몰라도 되지만, GitHub에 코드를 올리는 흐름은 01 과정에서 먼저 익힙니다.

## 2. 기본 개념

GitHub Actions는 저장소 안의 아래 위치에 workflow 파일을 둡니다.

```text
.github/workflows/ci.yml
```

workflow 파일은 보통 다음 일을 합니다.

```text
1. GitHub 저장소의 코드를 가져옵니다.
2. Python 또는 Node.js 같은 실행 환경을 준비합니다.
3. requirements.txt 또는 package.json 기준으로 패키지를 설치합니다.
4. 테스트를 실행합니다.
5. 필요하면 Docker 이미지를 만들거나 배포를 진행합니다.
```

## 3. 가장 작은 Python 테스트 workflow 예시

```yaml
name: Python CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          python -m pytest tests -q
```

처음에는 이 정도 구조만 이해하면 됩니다.

## 4. Secrets는 언제 쓰는가

API Key, AWS Access Key, Supabase Service Role Key처럼 공개되면 안 되는 값은 GitHub Actions 파일에 직접 적지 않습니다.

대신 GitHub 저장소의 `Settings -> Secrets and variables -> Actions`에 등록합니다.

예:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
OPENAI_API_KEY
GEMINI_API_KEY
```

workflow에서는 다음처럼 사용합니다.

```yaml
env:
  AWS_REGION: ${{ secrets.AWS_REGION }}
```

중요:

```text
secret 값을 echo로 출력하지 않습니다.
오류 로그에 secret이 찍히지 않도록 주의합니다.
실습이 끝난 뒤 더 이상 쓰지 않는 secret은 삭제합니다.
```

## 5. 실행 결과 확인

1. GitHub 저장소로 이동합니다.
2. 상단의 `Actions` 탭을 클릭합니다.
3. 실행된 workflow를 선택합니다.
4. 실패한 단계가 있으면 빨간 표시가 난 step을 클릭합니다.
5. 로그의 마지막 오류 메시지를 확인합니다.

초보자는 실패 로그 전체를 한 번에 이해하려고 하기보다, 실패한 step 이름과 마지막 오류 메시지를 먼저 보면 됩니다.

## 6. 자주 나는 오류

| 오류 | 확인할 것 |
| --- | --- |
| `requirements.txt not found` | workflow 실행 위치와 파일 위치가 맞는가 |
| `ModuleNotFoundError` | 패키지 설치 단계가 빠지지 않았는가 |
| `pytest: command not found` | `pytest`가 requirements에 들어 있는가 |
| `secret not found` | GitHub 저장소 secrets에 정확한 이름으로 등록했는가 |
| AWS 권한 오류 | IAM 권한, region, Access Key가 맞는가 |

## 7. 체크리스트

```text
[ ] .github/workflows 폴더의 의미를 이해했다.
[ ] push 또는 pull_request 때 workflow가 실행되는 것을 이해했다.
[ ] 테스트 자동화 workflow의 기본 흐름을 이해했다.
[ ] secret 값을 workflow 파일에 직접 적지 않는다는 것을 이해했다.
[ ] Actions 탭에서 실행 로그를 확인할 수 있다.
```
