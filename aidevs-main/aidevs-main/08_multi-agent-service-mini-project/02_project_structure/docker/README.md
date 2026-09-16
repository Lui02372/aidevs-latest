# docker

Dockerfile과 docker-compose.yml을 관리하는 폴더입니다.

## 실행

```powershell
cd C:\aidev\08_multi-agent-service-mini-project\02_project_structure
docker compose -f .\docker\docker-compose.yml up --build
```

## 확인

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8801
http://127.0.0.1:8802
```
