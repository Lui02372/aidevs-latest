# AWS 계정과 비용 관리 가이드

AWS는 07~08 과정에서 배포와 운영 실습을 위해 사용합니다. AWS는 실제 비용이 발생할 수 있으므로, 계정 생성보다 먼저 비용 관리 기준을 이해해야 합니다.

공식 문서:

- [AWS 계정 생성](https://aws.amazon.com/free/)
- [AWS CLI 설치](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)

## 1. 언제 필요한가

AWS는 아래 과정에서 사용합니다.

| 과정 | 사용 목적 |
| --- | --- |
| 07_multi-agent-service-ops | 컨테이너 서비스 배포, 로그 확인, 운영 자동화 |
| 08_multi-agent-service-mini-project | 최종 서비스 배포와 장애 복구 결과 검증 |

01~06 과정만 진행할 때는 AWS 계정이 없어도 됩니다.

## 2. 계정 생성 전 주의

AWS는 무료 사용량이 있더라도 사용 방식에 따라 비용이 발생할 수 있습니다.

반드시 아래 기준을 지킵니다.

```text
실습 전 예산 알림을 설정합니다.
사용하지 않는 리소스는 바로 삭제합니다.
Access Key를 GitHub나 문서에 올리지 않습니다.
실습 리전은 수업에서 정한 리전을 사용합니다.
개인 결제 카드 사용 시 비용 알림 메일을 자주 확인합니다.
```

## 3. 계정 생성

1. [AWS Free Tier](https://aws.amazon.com/free/) 페이지에 접속합니다.
2. `Create a Free Account`를 선택합니다.
3. 이메일, 계정 이름, 비밀번호를 입력합니다.
4. 결제 수단을 등록합니다.
5. 전화번호 인증을 진행합니다.
6. Support Plan은 기본 또는 무료에 해당하는 항목을 선택합니다.

계정 생성 후에는 루트 계정으로 계속 작업하지 않는 것이 좋습니다. 가능하면 IAM 사용자 또는 IAM Identity Center 기반으로 실습 계정을 분리합니다.

## 4. MFA 설정

MFA는 로그인할 때 비밀번호 외에 인증 앱의 숫자 코드를 한 번 더 확인하는 보안 방식입니다.

진행 순서:

```text
1. AWS Console 로그인
2. 우측 상단 계정 이름 클릭
3. Security credentials 선택
4. Multi-factor authentication 설정
5. Google Authenticator, Microsoft Authenticator 같은 앱 연결
```

## 5. 예산 알림 설정

실습 전 반드시 예산 알림을 설정합니다.

추천 기준:

```text
월 예산: 5달러 또는 수업에서 정한 금액
알림: 50%, 80%, 100%
알림 이메일: 자주 확인하는 이메일
```

진행 순서:

```text
1. AWS Console에서 Billing and Cost Management 검색
2. Budgets 선택
3. Create budget 선택
4. Cost budget 선택
5. 월 예산 금액 입력
6. 알림 기준과 이메일 입력
7. 생성
```

## 6. AWS CLI 설치와 확인

AWS CLI는 PowerShell에서 AWS를 제어하는 명령어 도구입니다.

공식 문서의 Windows 설치 안내를 따라 설치합니다.

설치 후 PowerShell을 새로 열고 확인합니다.

```powershell
aws --version
```

정상 예시:

```text
aws-cli/2.x.x Python/3.x Windows/...
```

## 7. AWS 자격 증명 설정

수업에서 AWS CLI를 사용하는 경우 아래 명령을 사용할 수 있습니다.

```powershell
aws configure
```

입력 항목:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

주의:

```text
Access Key와 Secret Access Key는 비밀번호처럼 다룹니다.
GitHub Actions에는 repository secrets로 등록합니다.
.env, README, 코드 파일에 직접 적지 않습니다.
```

## 8. 실습 후 정리

AWS 실습 후에는 반드시 사용한 리소스를 정리합니다.

확인할 항목:

```text
[ ] 실행 중인 서비스가 남아 있지 않은가?
[ ] 컨테이너 서비스나 서버리스 서비스가 계속 실행 중이지 않은가?
[ ] 로드 밸런서가 남아 있지 않은가?
[ ] ECR 이미지나 로그가 과도하게 쌓이지 않았는가?
[ ] CloudWatch 로그 보존 기간이 너무 길지 않은가?
[ ] 비용 대시보드에서 예상 비용을 확인했는가?
```

## 9. 체크리스트

```text
[ ] AWS 계정을 만들었다.
[ ] MFA를 설정했다.
[ ] 예산 알림을 설정했다.
[ ] AWS CLI를 설치했다.
[ ] aws --version이 동작한다.
[ ] Access Key를 문서나 GitHub에 올리지 않는 기준을 이해했다.
[ ] 실습 후 리소스를 삭제해야 한다는 것을 이해했다.
```
