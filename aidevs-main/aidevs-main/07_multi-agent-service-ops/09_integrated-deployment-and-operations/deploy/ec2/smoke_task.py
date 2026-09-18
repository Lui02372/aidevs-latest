"""Submit one real learning task. Keeps its history for the learner to inspect."""
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen
from uuid import uuid4

base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:18000"
payload = {"user_id": "ec2-learning", "request": "서울 1일 대중교통 여행을 계획해 주세요. 예산은 10만원이며 날씨도 확인해 주세요.", "idempotency_key": "ec2-smoke-" + uuid4().hex}
request = Request(base + "/api/tasks", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
with urlopen(request, timeout=15) as response:
    task = json.load(response)
print(json.dumps({"task_id": task["task_id"], "status": task["status"], "user_id": task["user_id"]}))
