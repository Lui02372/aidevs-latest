"""Auto Healing Workflow backend API.

실행 방법:
    cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure\backend
    uvicorn app.main:app --reload

이 파일은 FastAPI 애플리케이션의 시작점입니다.
초보자는 먼저 /health 주소가 정상 동작하는지 확인한 뒤,
/incidents API로 장애 이벤트를 보내면서 Agent 흐름을 확장하면 됩니다.
"""

from fastapi import FastAPI

from .routers.incidents import router as incident_router


app = FastAPI(title="Auto Healing Workflow API")


@app.get("/health")
def health_check() -> dict[str, str]:
    """서비스가 살아 있는지 확인하는 가장 단순한 Health Check API입니다."""

    return {"status": "ok", "service": "auto-healing-backend"}


app.include_router(incident_router)
