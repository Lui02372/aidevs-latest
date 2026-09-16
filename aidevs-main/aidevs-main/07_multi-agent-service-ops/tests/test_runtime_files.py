from pathlib import Path


ROOT = Path(__file__).parents[1]


def test_local_services_use_course_ports() -> None:
    compose = (ROOT / "00_runtime-and-deployment" / "00_local-services" / "docker-compose.yml").read_text(encoding="utf-8")
    assert '"6380:6379"' in compose
    assert '"5434:5432"' in compose
    assert '"11435:11434"' in compose


def test_simple_compose_has_optional_ollama_profile() -> None:
    compose = (ROOT / "00_runtime-and-deployment" / "01_simple-multi-llm-compose" / "compose.yml").read_text(encoding="utf-8")
    assert 'profiles: ["ollama"]' in compose
    assert "ollama_data:" in compose


def test_no_assignment_or_starter_directories() -> None:
    forbidden = {"20_assignments", "starter", "solution"}
    found = {path.name for path in ROOT.rglob("*") if path.is_dir() and path.name in forbidden}
    assert found == set()
