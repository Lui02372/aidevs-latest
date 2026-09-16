# 02 EC2 생성과 보안 그룹

AWS Console 화면의 문구는 시점과 계정에 따라 조금 다를 수 있습니다. 버튼 이름이
다르면 같은 의미의 `Launch instance`, `Instances`, `Security groups` 메뉴를
찾습니다.

## 1. Region 확인

수업에서 정한 Region을 선택합니다. 생성 후 다른 Region으로 이동하면 인스턴스가
보이지 않는 것처럼 느낄 수 있으므로 화면 상단의 Region을 기록합니다.

```text
사용 Region: ____________________
```

## 2. 인스턴스 생성

1. AWS Console에서 EC2를 엽니다.
2. `Instances`를 선택합니다.
3. `Launch instances`를 선택합니다.
4. 배포할 프로젝트에 맞는 이름을 지정합니다. 아래 프로젝트별 설정표를 참고합니다.
5. 최신 Amazon Linux 2023 x86_64 AMI를 선택합니다. 계정 정책이나 Instance Type 제약으로
   사용할 수 없다면 Ubuntu Server 24.04 LTS x86_64를 선택합니다.
6. 05·06 공통 실습 사양인 `t3.small`을 선택합니다.
7. 새 Key Pair를 만들거나 강사가 지정한 Key Pair를 선택합니다. multi-agent-course Name  . 
8. Root EBS의 `Delete on termination` 설정을 확인합니다.
9. Public IPv4가 할당되는 네트워크 설정인지 확인합니다.

> AMI ID를 문서나 다른 Region의 예제에서 복사하지 않습니다. `ami-...` ID는 Region마다
> 다르고, 새 Image가 배포되면서 기존 ID를 더 이상 사용할 수 없을 수 있습니다. EC2 생성
> 화면의 `Quick Start`에서 현재 Region에 표시되는 Amazon Linux 또는 Ubuntu를 직접
> 선택합니다. `AMI가 유효하지 않습니다` 오류가 나면 기존 Launch Template이나 최근 설정에
> 남아 있는 고정 AMI ID를 제거하고 새 Instance 생성 화면에서 다시 선택합니다.

### 프로젝트별 권장 설정

이 문서는 여러 배포 실습에서 공통으로 사용합니다. 예제 이름을 그대로 입력하지 말고 현재
배포하는 프로젝트에 맞게 선택합니다.

| 배포 프로젝트 | EC2 이름 | 권장 Instance Type | Root EBS | 공개 Port |
| --- | --- | --- | --- | --- |
| `01_simple-multi-llm-compose` | `multi-agent-simple-compose` | `t3.small` | `16 GiB gp3` | `8501` |
| `05_weather-mcp-deployment-project` | `weather-mcp-deployment` | `t3.small` | `16 GiB gp3` | `8501` |
| `06_weather-mcp-stateful-deployment` | 05 Instance 재사용 | `t3.small` | 기존 `16 GiB gp3` 재사용 | `8501` |

`05_weather-mcp-deployment-project`는 Ollama·PostgreSQL·Redis 없이 Frontend, Backend,
Weather MCP 세 Container를 실행한 뒤 같은 Instance에서 06의 PostgreSQL·Redis까지
추가하므로 처음부터 `t3.small`을 사용합니다. `t3.micro`는 선택하지 않습니다. 계정의 비용
한도와 강사의 지시가 있다면 그 값을 우선하며, 안정적인 반복 Build가 필요하면
`t3.medium`을 선택할 수 있습니다.

AMI를 Ubuntu로 바꾸면 Application 구조와 Compose 파일은 바뀌지 않습니다. 다만 SSH
사용자와 Docker 설치 명령이 다릅니다.

| AMI | 기본 SSH 사용자 | Package 명령 |
| --- | --- | --- |
| Amazon Linux 2023 | `ec2-user` | `dnf` 또는 `yum` |
| Ubuntu Server 24.04 LTS | `ubuntu` | `apt` |

Ubuntu를 선택한 수강생은 다음 문서의 Ubuntu 설치 절차를 사용하고 GitHub Secret
`AWS_USER`에도 `ubuntu`를 입력합니다.

## 3. Key Pair

Key 파일은 다시 내려받기 어려우므로 안전한 로컬 폴더에 저장합니다.

금지:

- Git 저장소에 Commit
- 메신저·공용 Drive 공유
- README에 Key 내용 붙여넣기
- EC2 서버 내부에 Private Key 업로드

Windows 예시 경로:

```text
C:\Users\<사용자>\.ssh\multi-agent-course.pem
```

실제 사용자 이름으로 바꾸고 Key 파일 경로를 문서나 Git에 저장하지 않습니다.

## 4. Security Group

### VPC를 새로 만들어야 하나요?

입문 실습에서는 별도의 VPC를 설계하지 않고 현재 Region의 `default VPC`를 사용합니다.
EC2 `Network settings`의 VPC 목록에 `(default)`가 표시되면 새 VPC를 만들지 않습니다.
해당 VPC의 기본 Public Subnet을 선택하고 `Auto-assign public IP`를 `Enable`로 설정합니다.

VPC 목록이 비어 있거나 `(default)` VPC가 없다면 다음 순서로 기본 VPC를 먼저 만듭니다.

```text
VPC Console
→ Your VPCs
→ Actions
→ Create default VPC
```

생성 후 EC2 `Launch instances` 화면으로 돌아가 새로고침합니다. 직접 CIDR, Route Table,
Internet Gateway, NAT Gateway를 구성하는 Custom VPC는 네트워크 전용 심화 실습에서
다룹니다. 특히 이 프로젝트에는 비용이 추가되는 NAT Gateway가 필요하지 않습니다.

서울 Region에서 default VPC가 없다는 안내가 표시되면 `새 VPC를 생성`이 아니라 `새 기본
VPC를 생성`을 선택합니다. 생성 후 EC2 화면에서 VPC 항목에 `(default)`가 표시되는지
확인합니다.

다음 네 항목을 확인합니다.

```text
[ ] VPC 이름 또는 ID 옆에 default가 표시됨
[ ] 선택한 Subnet이 Public IPv4 할당을 지원함
[ ] Auto-assign public IP가 Enable
[ ] 새 Security Group을 이 VPC 안에 생성함
```

다음 두 Inbound Rule만 사용합니다.

| Type | Port | Source | 목적 |
| --- | ---: | --- | --- |
| SSH | 22 | My IP | 관리자 접속 |
| Custom TCP | 8501 | My IP | Streamlit 화면 |

`My IP`는 현재 Browser가 사용하는 Public IP를 AWS가 자동 입력하는 편의 기능입니다.
`Custom`은 허용할 IP 또는 CIDR을 직접 입력한다는 뜻이며 특정 노트북을 식별하는 기능은
아닙니다. 예를 들어 `My IP`가 `203.0.113.10/32`이면 해당 Public IP 하나를 허용합니다.
같은 공유기를 사용하는 다른 기기도 같은 Public IP로 접속할 수 있으며, 네트워크가 바뀌면
두 Rule의 Source를 현재 `My IP`로 갱신합니다.

다음 Rule은 만들지 않습니다.

```text
22    0.0.0.0/0
8000  0.0.0.0/0
```

IP가 변경되어 SSH 접속이 안 되면 SSH Rule의 Source를 현재 `My IP`로
갱신합니다. 문제 해결을 위해 22번 포트를 전체 인터넷에 열지 않습니다.

## 5. Storage 구성

| 항목 | 권장값 |
| --- | --- |
| Volume 수 | 1개 |
| Size | `16 GiB` |
| Volume type | `gp3` |
| IOPS·Throughput | 기본값 |
| Encryption | 계정 기본 설정 사용 |
| Delete on termination | Enable |

별도 EBS Volume은 만들지 않습니다. Database Volume은 없지만 운영체제, Docker Image 세 개,
Build Cache와 Log 공간이 필요하므로 기본 8 GiB보다 16 GiB를 권장합니다.

EC2 생성 화면의 `File systems`는 EFS 같은 공유 파일 시스템을 연결하는 별도 항목입니다.
이번 프로젝트에서는 `None`으로 두고 `Add file system`을 선택하지 않습니다. Ubuntu Root
파일 시스템은 AMI가 자동 구성하므로 직접 포맷하거나 Mount하지 않습니다.

## 6. 고급 세부 정보

이번 실습에서는 시작 Script나 AWS Service 권한을 사용하지 않으므로 대부분 기본값을
유지합니다.

| 항목 | 설정 |
| --- | --- |
| IAM instance profile | None |
| Shutdown behavior | Stop |
| Stop protection | Disable |
| Termination protection | 수업 중 실수 방지가 필요하면 Enable, 아니면 기본값 |
| Detailed CloudWatch monitoring | Disable |
| Tenancy | Shared 또는 Default |
| Elastic inference·Nitro Enclave | Disable |
| Capacity reservation | None 또는 Open |
| Instance metadata access | Enable |
| Metadata version | V2 only 권장 |
| Allow tags in metadata | Disable |
| User data | 비워 둠 |

`Detailed CloudWatch monitoring`은 추가 비용이 발생할 수 있어 이번 실습에서는 켜지
않습니다. User data로 Docker를 자동 설치하지 않는 이유는 첫 배포에서 수강생이 SSH 접속과
설치 과정을 직접 확인하기 위해서입니다. `Termination protection`을 켰다면 마지막 정리
단계에서 먼저 해제해야 Instance를 Terminate할 수 있습니다.

T 계열 Instance의 Credit specification을 선택할 수 있다면 비용 한도를 우선합니다.
`Unlimited`는 지속적으로 기준 성능을 초과할 때 추가 비용이 발생할 수 있습니다. 강사의
별도 지시가 없다면 `Standard`를 선택하고, 선택 항목이 보이지 않으면 기본값을 유지합니다.
이 항목은 `Advanced details → Credit specification`에 있으며 Console에 표시되지 않으면
Instance 생성을 중단하지 말고 기본값으로 진행합니다.

## 7. 생성 후 기록

```text
Instance ID: ____________________
Public IPv4: ____________________
Public DNS:  ____________________
Security Group ID: ______________
Root Volume ID: __________________
```

민감한 Secret은 아니지만 제출 문서에는 계정 식별 정보가 과도하게 노출되지
않도록 일부를 마스킹합니다.

## 8. 접속 전 확인

```text
[ ] Instance 상태가 running
[ ] Status check가 통과
[ ] Public IPv4가 있음
[ ] SSH Source가 My IP
[ ] 8501 Source가 My IP
[ ] 8000 Inbound Rule이 없음
```

## 공식 문서

- [EC2 Security Group 생성](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-security-group.html)
- [Security Group Rule 변경](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/changing-security-group.html)


