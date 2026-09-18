"""Read-only EC2 inventory. Never print passwords or full connection URLs."""
import json
import subprocess
from urllib.parse import urlsplit

names = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"], text=True).splitlines()
for name in names:
    item = json.loads(subprocess.check_output(["docker", "inspect", name], text=True))[0]
    env = dict(v.split("=", 1) for v in item["Config"].get("Env", []) if "=" in v)
    print(json.dumps({
        "name": name,
        "networks": list(item["NetworkSettings"]["Networks"]),
        "compose_directory": item["Config"].get("Labels", {}).get("com.docker.compose.project.working_dir"),
        "database": env.get("POSTGRES_DB"),
        "database_user": env.get("POSTGRES_USER"),
        "configured_key_names": [k for k in env if k.endswith("API_KEY") and env[k]],
        "mounts": [{"type": m["Type"], "destination": m["Destination"]} for m in item["Mounts"]],
    }))
    if env.get("DATABASE_URL"):
        url = urlsplit(env["DATABASE_URL"])
        print(json.dumps({"db_host": url.hostname, "db_port": url.port, "db_name": url.path, "db_user": url.username}))
