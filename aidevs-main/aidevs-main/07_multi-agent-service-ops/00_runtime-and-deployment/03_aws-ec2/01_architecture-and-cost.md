# 01 아키텍처와 비용 범위

## 학습 아키텍처

```text
Internet → TCP 8501 → EC2 Security Group
                         │
                         ▼
EC2 Linux(Ubuntu Server 24.04 LTS 권장)
├─ frontend :8501 → Host :8501
├─ backend  :8000 → 선택한 실제 LLM API HTTPS
├─ redis    :6379, 외부 비공개
└─ database :5432, 외부 비공개
              └─ postgres_data Volume
```

외부 Browser는 Frontend만 접속합니다. 나머지 서비스는 Docker 내부 Network에서
서비스 이름으로 통신합니다.

## AWS 리소스

| 리소스 | 목적 | 실습 종료 처리 |
| --- | --- | --- |
| EC2 | 네 Container 실행 | Terminate |
| Root EBS | OS·Image·Docker Volume | Delete on termination 확인 |
| Security Group | 22·8501 접근 제어 | 다른 곳에서 미사용 시 삭제 |
| Key Pair | SSH 접속 | 교육 정책에 따라 보관·삭제 |

무료 사용 가능 여부와 비용은 계정·Region·시점에 따라 달라질 수 있으므로 AWS Console의
현재 표시를 확인합니다. 특정 Instance Type을 항상 무료라고 문서에 고정하지 않습니다.

```text
AMI           Ubuntu Server 24.04 LTS x86_64 권장
Instance Type t3.small
Storage       16 GiB gp3 Root EBS
Public IP     Frontend 실습을 위해 활성화
Elastic IP    만들지 않음
```

05부터 06까지 같은 EC2를 재사용하므로 처음부터 `t3.small`을 선택합니다. `t3.micro`는 05의
세 Application Container만 실행될 수 있더라도 06에서 PostgreSQL·Redis까지 추가하고 Image를
Build할 때 메모리가 부족할 가능성이 큽니다. 안정적인 수업 진행이 더 중요하면 강사의 승인
후 `t3.medium`을 선택합니다.

Amazon Linux 2023도 Docker Application 구조상 사용할 수 있지만 계정·리전 정책 때문에
선택할 수 없는 경우가 있습니다. 본 실습의 명령과 GitHub Secret 예시는 Ubuntu의 기본 사용자
`ubuntu`를 기준으로 하며, Amazon Linux를 선택한 경우에만 `ec2-user`로 바꿉니다.

## 공식 문서

- [EC2 Instance Lifecycle과 비용](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- [EC2 Free Tier 사용량 확인](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html)

