# 03 EC2 연결 가이드

먼저 [EC2 생성](../02_create-ec2.md)에서 서버를 만들고
[설치 안내](../03_install-and-transfer.md)에 따라 Docker와 Compose를 설치합니다.
03은 서버 연결 실습이므로 launcher의 guide 메뉴로 열고 접속은 PowerShell에서 진행합니다.

## 1. 접속 정보 기록

| 항목 | 어디서 찾나요? |
| --- | --- |
| Public IPv4 / DNS | AWS EC2 → Instances → 선택 → Details |
| 사용자 | Ubuntu AMI: ubuntu / Amazon Linux: ec2-user |
| PEM 파일 | 인스턴스 생성 때 내려받은 개인 키, Git 저장소 밖에 보관 |
| Region | AWS 콘솔 오른쪽 위 |
| Instance ID | i-로 시작하는 값, 07 SSM 배포에서 사용 |

## 2. Windows PowerShell → EC2 Linux

아래 값 세 개를 실제 값으로 바꿉니다. 명령을 실행하는 위치는 Windows입니다.

~~~powershell
$ec2Address = 'EC2의_PUBLIC_IP_또는_DNS'
$ec2User = 'ubuntu'
$keyPath = 'C:\Users\사용자\.ssh\수업용키.pem'
Test-NetConnection $ec2Address -Port 22
ssh -i $keyPath "$ec2User@$ec2Address"
~~~

서버의 호스트 키 지문을 신뢰할 수 있는 경로로 확인한 뒤 최초 접속을 수락합니다.
접속 후 프롬프트가 ubuntu@... 또는 ec2-user@...로 바뀌면 이제 Linux 명령을 사용합니다.

~~~bash
whoami
pwd
docker version
docker compose version
exit
~~~

exit하면 Windows PowerShell로 돌아옵니다.
Permission denied(publickey)는 사용자/PEM을, Timeout은 Public IP·라우팅·22번 보안그룹을 봅니다.
보안그룹의 SSH는 내 IP만 허용하고, PostgreSQL 5432/5433은 인터넷에 공개하지 않습니다.
Windows 개인 키 권한 오류는 [기존 설치 안내](../03_install-and-transfer.md)의 icacls 절을 따릅니다.

## 3. 수동 배포 먼저 확인

[배포 및 검증](../04_deploy-and-verify.md)에 따라 01 full-stack을 먼저 실행합니다.
서버 .env는 서버에서 만들며 로컬 키 파일·가상환경을 통째로 전송하지 않습니다.
아래는 **EC2 bash, 01 소스를 업로드한 폴더**에서 실행합니다.

~~~bash
cd ~/aidevs-runtime/01_simple-multi-llm-compose
docker compose -f compose.full-stack.yml up -d --build --wait
docker compose -f compose.full-stack.yml ps
curl --fail http://127.0.0.1:8000/health/ready
docker compose -f compose.full-stack.yml exec database psql -U agent_user -d agent_db
~~~

DB명/사용자가 다르면 서버 .env 값으로 변경합니다. psql은 \q로 종료합니다.
여기까지 성공한 후 CI/CD로 같은 일을 자동화합니다.

## 4. 브라우저 접속: SSH 터널

특히 07 앱은 EC2의 127.0.0.1에만 바인딩되어 있습니다.
로컬 앱을 먼저 중지한 뒤 **새 Windows PowerShell**에서 연결합니다.

~~~powershell
ssh -i $keyPath -N -L 8501:127.0.0.1:8501 -L 8000:127.0.0.1:8000 "$ec2User@$ec2Address"
~~~

새 터미널에서는 앞의 $keyPath/$ec2User/$ec2Address를 다시 설정합니다.
이 창을 켜 둔 채 Windows 브라우저에서 http://localhost:8501 을 엽니다.
터널 종료는 Ctrl+C입니다. 서버의 8501을 인터넷 전체에 열 필요가 없습니다.
SSH를 쓰지 않는 SSM 전용 환경은 Session Manager 포트 포워딩 경로를 별도로 구성해야 합니다.

## 5. CI/CD로 넘기기

[02 CI](../../02_github-actions-ci/doc/ConnectGuide.md)가 성공했고 EC2 수동 실행도 성공했다면
[04 CD](../../04_github-actions-aws-deploy/doc/ConnectGuide.md)로 이동합니다.
내 PC SSH 성공만으로 GitHub Runner SSH 성공이 보장되지는 않습니다.
Runner의 네트워크 위치가 다르기 때문입니다.

실습이 끝나면 [리소스 정리](../06_cleanup.md)에서 EC2·EBS·Elastic IP 등을 확인합니다.
