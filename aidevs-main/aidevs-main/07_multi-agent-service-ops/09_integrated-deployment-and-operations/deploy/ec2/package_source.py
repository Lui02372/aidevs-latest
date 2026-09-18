"""Create a small allowlisted deployment archive, excluding all runtime credentials."""
import hashlib
from pathlib import Path
import tarfile

root = Path(__file__).resolve().parents[3]
output = root / ".deploy-artifacts"
output.mkdir(exist_ok=True)
archive = output / "source.tar.gz"
with tarfile.open(archive, "w:gz") as tar:
    for name in ("requirements.txt", ".dockerignore", "shared", "08_multi-ai-agent-service", "09_integrated-deployment-and-operations"):
        entry = root / name
        for path in ([entry] if entry.is_file() else sorted(entry.rglob("*"))):
            if not path.is_file():
                continue
            if any(part in {"__pycache__", ".pytest_cache", ".git", ".venv"} for part in path.parts):
                continue
            if path.name == ".env" or path.name.endswith((".env", ".pem", ".key", ".pyc", ".local")):
                continue
            tar.add(path, arcname=path.relative_to(root), recursive=False)
release = hashlib.sha1(archive.read_bytes()).hexdigest()
(output / "release-id.txt").write_text(release, encoding="ascii")
print(f"Source archive ready: {archive.stat().st_size} bytes; manual release {release}")
