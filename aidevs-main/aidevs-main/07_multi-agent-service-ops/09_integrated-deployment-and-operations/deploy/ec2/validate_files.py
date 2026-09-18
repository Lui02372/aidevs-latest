"""Offline structural validation; does not claim Docker/EC2 execution."""
import ast
from pathlib import Path

import yaml

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
for path in here.glob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"))
compose = yaml.safe_load((here / "compose.yaml").read_text(encoding="utf-8"))
assert set(compose["services"]) == {"api", "worker", "frontend", "mcp", "redis"}
for service in compose["services"].values():
    for port in service.get("ports", []):
        assert port.startswith("127.0.0.1:")
workflow = yaml.safe_load((here.parent / "github/ec2-ci-cd.yml").read_text(encoding="utf-8"))
assert workflow["jobs"]["deploy"]["needs"] == "verify"
assert workflow["env"]["COURSE"] == "aidevs-main/aidevs-main/07_multi-agent-service-ops"
git_root = root.parents[2]
installed = git_root / ".github/workflows/09-ec2-ci-cd.yml"
assert installed.read_bytes() == (here.parent / "github/ec2-ci-cd.yml").read_bytes()
print("Python syntax, YAML structure, private bindings, installed workflow match: PASS")
