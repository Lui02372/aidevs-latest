# 06 리소스 정리

리소스 정리는 AWS 실습의 필수 완료 항목입니다.

> 이 문서는 모든 AWS 실습을 끝냈을 때 사용하는 최종 정리 절차입니다.
> `05_weather-mcp-deployment-project`를 마치고 바로
> `06_weather-mcp-stateful-deployment`를 진행한다면 EC2를 Terminate하지 않습니다.
> 05 Application Container만 중지하고, EC2·Security Group·Key Pair·Docker를 06에서
> 재사용합니다. 06까지 마치고 보존할 데이터를 확인한 뒤 이 문서의 Terminate 절차를
> 수행합니다.

## 1. EC2 내부 Container 정리

```bash
cd ~/simple-compose
docker compose -f compose.full-stack.yml down
docker compose -f compose.full-stack.yml ps
```

`postgres_data` Volume에는 실습 메모와 Chat 이력이 남아 있습니다. EC2 Terminate 전에
실제 데이터가 들어 있지 않은지 확인하고, Root EBS와 함께 제거되는 구성이 맞는지
확인합니다.

교육용 Image도 제거하려면 현재 Image를 먼저 확인합니다.

```bash
docker images
```

이번 예제에서 만든 Image임을 확인한 뒤에만 제거합니다.

## 2. 필요한 결과 보관

종료 전에 다음 자료만 로컬 문서에 기록합니다.

- Frontend 정상 화면
- Backend Health 결과
- `docker compose -f compose.full-stack.yml ps`
- 장애 전후 로그 일부
- 배운 점

실제 개인정보·SSH Key·계정 ID 전체는 제출물에 포함하지 않습니다.

## 3. EC2 Terminate

AWS Console:

1. EC2 `Instances`를 엽니다.
2. 본인이 만든 `multi-agent-simple-compose`를 선택합니다.
3. Instance ID를 다시 확인합니다.
4. `Instance state`에서 `Terminate instance`를 선택합니다.
5. 영구 삭제임을 이해한 뒤 확인합니다.
6. 상태가 `shutting-down` 또는 `terminated`로 바뀌는지 확인합니다.

`Stop`만 선택하면 인스턴스 사용 비용은 멈출 수 있지만 EBS 같은 저장 리소스
비용은 남을 수 있습니다. 실습이 완전히 끝났다면 교육 정책에 따라 Terminate하고
연결 리소스를 확인합니다.

## 4. EBS 확인

1. EC2 Console의 `Volumes`를 엽니다.
2. 기록해 둔 Root Volume ID를 찾습니다.
3. `Delete on termination`이 적용되어 삭제됐는지 확인합니다.
4. 남아 있는 Volume을 발견하면 다른 인스턴스가 사용 중인지 먼저 확인합니다.
5. 삭제 대상이 확실하지 않으면 임의 삭제하지 말고 강사에게 확인합니다.

## 5. 추가 리소스 확인

이번 실습에서는 만들지 않아야 하지만 다음 항목을 확인합니다.

```text
[ ] Elastic IP 없음
[ ] Snapshot 없음
[ ] Load Balancer 없음
[ ] NAT Gateway 없음
[ ] RDS 없음
[ ] ElastiCache 없음
```

## 6. Security Group

본 실습에서 만든 Security Group이 다른 인스턴스에서 사용되지 않는지 확인한 뒤
교육 정책에 따라 삭제합니다.

Key Pair는 다음 수업에서 재사용할지 강사 정책에 따라 결정합니다. 로컬 Private
Key 파일을 Git에 Commit하지 않습니다.

## 7. 최종 체크

```text
[ ] Compose를 종료했다.
[ ] EC2를 Terminate했다.
[ ] Root EBS 삭제 여부를 확인했다.
[ ] Elastic IP와 Snapshot이 없음을 확인했다.
[ ] Security Group 사용 여부를 확인했다.
[ ] AWS Console Region을 다시 확인했다.
[ ] 비용·사용량 화면을 확인했다.
```

## 공식 문서

- [EC2 Instance 종료](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html)
- [EC2 중지 후에도 남을 수 있는 비용](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/how-ec2-instance-stop-start-works.html)


