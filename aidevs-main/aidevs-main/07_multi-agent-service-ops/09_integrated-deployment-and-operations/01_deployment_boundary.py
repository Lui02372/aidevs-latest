"""
[시나리오]
개발자는 08에서 Backend, Worker, Frontend를 각각 실행했습니다. 운영 환경에서는 세
Process의 책임과 의존성을 먼저 구분해야 장애 범위를 찾을 수 있습니다. 이 예제는 서비스
구성 요소가 어떤 Port와 저장소를 사용하는지 출력합니다. Docker 실행 전 배포 경계를 배웁니다.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Service:
    name: str
    command: str
    depends_on: tuple[str, ...]
    public_port: int | None = None


SERVICES = (
    Service("api", "uvicorn backend:app --host 0.0.0.0 --port 8000", ("redis", "postgres"), 8000),
    Service("worker", "python worker.py", ("redis", "postgres")),
    Service("frontend", "streamlit run frontend.py --server.port 8501", ("api",), 8501),
    Service("mcp", "python mcp_server.py", (), 8010),
)


if __name__ == "__main__":
    print("=== 배포할 Process와 책임 ===")
    for service in SERVICES:
        dependencies = ", ".join(service.depends_on) if service.depends_on else "없음"
        port = str(service.public_port) if service.public_port else "외부 공개 안 함"
        print(f"[{service.name}] 의존성={dependencies}, 공개 Port={port}")
        print(f"  실행 명령: {service.command}")
