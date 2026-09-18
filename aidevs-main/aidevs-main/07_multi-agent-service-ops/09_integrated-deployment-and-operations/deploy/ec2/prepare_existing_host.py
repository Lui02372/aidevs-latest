"""Run on the verified learning EC2. Reuse credentials locally without printing them."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

source = Path(sys.argv[1]).resolve()
base = Path.home() / "multi-agent-09"
shared = base / "shared"
shared.mkdir(parents=True, exist_ok=True, mode=0o700)
backend = "simple-multi-llm-full-stack-backend-1"
database = "simple-multi-llm-full-stack-database-1"
item = json.loads(subprocess.check_output(["docker", "inspect", backend], text=True))[0]
env = dict(v.split("=", 1) for v in item["Config"]["Env"] if "=" in v)
target = shared / "app.env"
if not target.exists():
    config = {
        "DATABASE_URL": env["DATABASE_URL"],
        "REDIS_URL": "redis://redis:6379/0",
        "TRAVEL_MCP_URL": "http://mcp:8010/mcp",
        "OPENAI_API_KEY": env.get("OPENAI_API_KEY", ""),
        "OPENAI_MODEL": env.get("OPENAI_MODEL", "gpt-4.1-mini"),
        "LLM_PROVIDER": "openai", "SUPERVISOR_PROVIDER": "openai",
        "WEATHER_AGENT_PROVIDER": "openai", "PLACE_AGENT_PROVIDER": "openai",
        "BUDGET_AGENT_PROVIDER": "openai", "ITINERARY_AGENT_PROVIDER": "openai",
        "TASK_TTL_SECONDS": "3600", "MAX_ORCHESTRATION_STEPS": "8",
    }
    # Single-quoted dotenv values prevent dollar interpolation. Reject line injection.
    for value in config.values():
        if any(c in value for c in ("\n", "\r", "'")):
            raise SystemExit("Configure app.env manually: unsupported dotenv character")
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write("".join(f"{k}='{v}'\n" for k, v in config.items()))
override = shared / "compose.override.yaml"
if not override.exists():
    shutil.copyfile(source / "09_integrated-deployment-and-operations/deploy/ec2/compose.existing-db.example.yaml", override)
sql = (source / "08_multi-ai-agent-service/schema.sql").read_text()
subprocess.run(["docker", "exec", "-i", database, "psql", "-v", "ON_ERROR_STOP=1", "-U", "agent_user", "-d", "agent_db"], input=sql, text=True, check=True)
print("Existing DB schema prepared; credentials remain only on EC2.")
