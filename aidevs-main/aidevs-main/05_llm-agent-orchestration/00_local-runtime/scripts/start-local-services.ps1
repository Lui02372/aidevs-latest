$ErrorActionPreference = "Stop"

function Start-IfMissing {
    param(
        [string]$Name,
        [scriptblock]$CreateCommand
    )

    $existing = docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
    if ($existing -eq $Name) {
        docker start $Name | Out-Null
        Write-Output "$Name started"
        return
    }

    & $CreateCommand
    Write-Output "$Name created"
}

Start-IfMissing "aidevs-ollama" {
    docker run -d `
        --name aidevs-ollama `
        -p 11434:11434 `
        -v aidevs-ollama-data:/root/.ollama `
        ollama/ollama | Out-Null
}

Start-IfMissing "aidevs-pgvector" {
    docker run -d `
        --name aidevs-pgvector `
        -p 5433:5432 `
        -e POSTGRES_DB=agent_db `
        -e POSTGRES_USER=agent_user `
        -e POSTGRES_PASSWORD=agent_password `
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

docker ps --filter "name=aidevs-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
