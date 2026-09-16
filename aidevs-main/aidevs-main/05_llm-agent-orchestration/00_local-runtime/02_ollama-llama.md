# Docker Ollama와 Llama

## 실행

첫 실행입니다. Image 다운로드와 모델 실행은 다른 서비스보다 오래 걸릴 수 있습니다.

```powershell
docker run -d `
  --name aidevs-ollama `
  -p 11434:11434 `
  -v aidevs-ollama-data:/root/.ollama `
  ollama/ollama
```

다음 수업부터는 같은 `docker run` 명령을 반복하지 않고 기존 Container를
시작합니다.

```powershell
docker start aidevs-ollama
docker ps --filter "name=aidevs-ollama"
docker logs --tail 30 aidevs-ollama
```

## 모델 준비

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
docker exec -it aidevs-ollama ollama list
```

모델 파일은 크기가 크고 내려받는 데 시간이 걸릴 수 있습니다. 수업에서는 먼저
`ollama list`로 이미 받은 모델을 확인하고 필요한 모델만 받습니다. 실행이 느리면
현재 사용량도 확인할 수 있습니다.

```powershell
docker stats aidevs-ollama
```

확인을 마치면 `Ctrl+C`로 `docker stats` 화면만 종료합니다. Container는 계속
실행됩니다.

모델명은 PC 사양과 수업 시점에 따라 변경할 수 있도록 `.env`의 `OLLAMA_MODEL`에서 관리합니다.

## API 확인

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri http://127.0.0.1:11434/api/chat `
  -ContentType "application/json" `
  -Body '{"model":"llama3.2","messages":[{"role":"user","content":"부산 여행을 한 문장으로 소개해 주세요."}],"stream":false}'
```

## 학습 포인트

- GPT·Gemini는 Cloud API이고 Ollama/Llama는 Local 실행입니다.
- 모델 파일은 Docker Volume에 저장합니다.
- Structured Output과 Tool Calling 지원은 선택한 모델에 따라 확인해야 합니다.
- 로컬 실행이라고 해서 입력 검증과 권한 검사가 불필요한 것은 아닙니다.

## 종료와 재시작

```powershell
docker stop aidevs-ollama
docker start aidevs-ollama
```

중지해도 `aidevs-ollama-data` Volume의 다운로드 모델은 유지됩니다.
