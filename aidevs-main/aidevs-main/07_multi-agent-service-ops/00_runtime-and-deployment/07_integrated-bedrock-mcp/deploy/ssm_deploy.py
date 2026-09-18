"""CI의 소스 archive를 S3에서 받아 SSM으로 배포하고 실제 명령 종료까지 확인한다."""
import json
import os
import re
import shlex
import time
import boto3


def main():
    sha = os.environ["GITHUB_SHA"]
    bucket = os.environ["ARTIFACT_BUCKET"]
    instance = os.environ["EC2_INSTANCE_ID"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha): raise ValueError("Invalid commit SHA")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]", bucket): raise ValueError("Invalid bucket")
    if not re.fullmatch(r"i-[0-9a-f]+", instance): raise ValueError("Invalid instance ID")
    root = f"/opt/weather-07/releases/{sha}"
    commands = ["set -eu", f"mkdir -p {root}",
        f"aws s3 cp {shlex.quote(f's3://{bucket}/weather-07/{sha}.tar.gz')} {root}/source.tar.gz",
        f"tar -xzf {root}/source.tar.gz -C {root}", f"bash {root}/deploy/deploy.sh"]
    client = boto3.client("ssm")
    command_id = client.send_command(InstanceIds=[instance], DocumentName="AWS-RunShellScript",
        Parameters={"commands": commands, "executionTimeout": ["1800"]}, TimeoutSeconds=120)["Command"]["CommandId"]
    print(json.dumps({"command_id": command_id, "commit": sha}), flush=True)
    for _ in range(210):
        time.sleep(10)
        try: result = client.get_command_invocation(CommandId=command_id, InstanceId=instance)
        except client.exceptions.InvocationDoesNotExist: continue
        status = result["Status"]
        if status in {"Pending", "InProgress", "Delayed"}: continue
        print("SSM terminal status:", status)
        if status != "Success":
            raise RuntimeError(f"Deployment failed: {status}; inspect SSM command {command_id}")
        return
    raise TimeoutError(f"SSM wait expired; inspect command {command_id} before retrying")


if __name__ == "__main__":
    main()
