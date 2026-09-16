r"""03_project_structure starter backend 테스트 파일입니다.

실행:
    cd C:\aidev\04_supabase-ai-mini-project\03_project_structure\backend
    C:\aidev\04_supabase-ai-mini-project\.venv\Scripts\Activate.ps1
    python -m pytest tests -q

이 starter는 아직 로그 API를 구현하지 않은 상태입니다.
따라서 첫 테스트는 backend가 켜질 수 있는지 확인하는 /health부터 시작합니다.
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    """GET /health가 200 OK와 status=ok를 반환하는지 확인합니다."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
