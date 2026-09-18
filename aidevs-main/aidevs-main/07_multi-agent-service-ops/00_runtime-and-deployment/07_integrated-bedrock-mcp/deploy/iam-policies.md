# 07 IAM 정책 템플릿

`ACCOUNT_ID`, `REGION`, `BUCKET`, `INSTANCE_ID`, `OWNER/REPO`는
본인 계정 값으로 바꾼 뒤 IAM 콘솔에서 정책 검증을 수행합니다. 템플릿 자체는 적용하지 않습니다.
중국/GovCloud 등 별도 partition은 ARN과 OIDC 설정도 해당 환경에 맞춰야 합니다.

## EC2 역할

IAM → Roles → Create role → AWS service → EC2로 만들면 다음 trust를 사용합니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

`AmazonSSMManagedInstanceCore` 관리형 정책을 연결합니다. 아래 inline policy를 추가하고
EC2 → Actions → Security → Modify IAM role에서 이 역할을 선택합니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::BUCKET/weather-07/*"
    }
  ]
}
```

S3에 고객 관리 KMS 암호화를 선택하면 해당 KMS decrypt 권한도 별도로 필요합니다.

## GitHub OIDC 배포 역할 trust

먼저 IAM → Identity providers에서 `token.actions.githubusercontent.com` provider를
등록합니다. Audience는 `sts.amazonaws.com`입니다.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:OWNER/REPO:environment:production"
        }
      }
    }
  ]
}
```

Environment를 사용하는 Job의 sub는 branch 형식이 아닙니다. 따라서 GitHub production
Environment에서도 허용 branch를 main으로 제한해야 합니다. workflow의 if만 의존하지 마세요.

## GitHub 배포 역할 permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::BUCKET/weather-07/*"
    },
    {
      "Effect": "Allow",
      "Action": "ssm:SendCommand",
      "Resource": [
        "arn:aws:ssm:REGION::document/AWS-RunShellScript",
        "arn:aws:ec2:REGION:ACCOUNT_ID:instance/INSTANCE_ID"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "ssm:GetCommandInvocation",
      "Resource": "*"
    }
  ]
}
```

GetCommandInvocation은 resource-level 제한을 지원하지 않아 `*`를 사용합니다.
SendCommand 권한은 대상 EC2에서 root 명령 실행 권한이므로 이 배포 역할의 trust와
production 승인을 엄격히 관리합니다. EC2 배포에는 AdministratorAccess가 필요하지 않습니다.
S3 bucket policy에서 다른 계정의 쓰기를 허용하지 않습니다.

## 수동 검증

EC2에서 `aws sts get-caller-identity`를 실행해 Instance Profile 역할 ARN을 확인합니다.
SSM 콘솔에서 EC2 Online과 GitHub OIDC Step 성공을 각각 확인합니다.
LLM은 서버 .env의 OpenAI 또는 Gemini API 키로 인증하며 이 IAM 역할을 사용하지 않습니다.

참고: [SSM IAM actions](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awssystemsmanager.html),
[GitHub OIDC AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).
