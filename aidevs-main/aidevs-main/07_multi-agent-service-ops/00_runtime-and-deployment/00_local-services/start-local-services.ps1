$ErrorActionPreference = "Stop"

function Start-IfMissing {
    param(
        [string]$Name,
        [scriptblock]$CreateCommand
    )

    $existingName = docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
    if ($existingName -eq $Name) {
        docker start $Name | Out-Null
        Write-Output "$Name started"
        return
    }

    & $CreateCommand
    Write-Output "$Name created"
}

Start-IfMissing "aidevs-pgvector" {
    docker run -d `
        --name aidevs-pgvector `
        -p 5433:5432 `
        -e POSTGRES_DB=agent_db `
        -e POSTGRES_USER=agent_user `
        -e POSTGRES_PASSWORD=agent_pwd `
        -v aidevs-pgvector-data:/var/lib/postgresql/data `
        pgvector/pgvector:pg16 | Out-Null
}

Start-IfMissing "aidevs-redis" {
    docker run -d `
        --name aidevs-redis `
        -p 6379:6379 `
        -v aidevs-redis-data:/data `
        redis:7 `
        redis-server --appendonly yes | Out-Null
}

Start-IfMissing "aidevs-ollama" {
    docker run -d `
        --name aidevs-ollama `
        -p 11434:11434 `
        -v aidevs-ollama-data:/root/.ollama `
        ollama/ollama:latest | Out-Null
}

Write-Output "Waiting for PostgreSQL..."
$postgresReady = $false
for ($attempt = 1; $attempt -le 15; $attempt++) {
    docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $postgresReady = $true
        break
    }
    Start-Sleep -Seconds 2
}
if (-not $postgresReady) {
    throw "PostgreSQL did not become ready. Run: docker logs aidevs-pgvector"
}

docker exec aidevs-pgvector psql -U agent_user -d agent_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
docker exec aidevs-redis redis-cli PING

Write-Output "Waiting for Ollama..."
$ollamaReady = $false
for ($attempt = 1; $attempt -le 15; $attempt++) {
    docker exec aidevs-ollama ollama list 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        $ollamaReady = $true
        break
    }
    Start-Sleep -Seconds 2
}
if (-not $ollamaReady) {
    throw "Ollama did not become ready. Run: docker logs aidevs-ollama"
}

Write-Output "Checking Ollama models..."
$modelList = docker exec aidevs-ollama ollama list
if ($modelList -notmatch "llama3\.2") {
    docker exec aidevs-ollama ollama pull llama3.2
}
if ($modelList -notmatch "gemma3:4b") {
    docker exec aidevs-ollama ollama pull gemma3:4b
}

docker exec aidevs-ollama ollama list
docker ps --filter "name=aidevs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
