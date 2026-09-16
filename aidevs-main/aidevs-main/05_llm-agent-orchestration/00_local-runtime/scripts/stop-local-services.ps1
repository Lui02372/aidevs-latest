$ErrorActionPreference = "Stop"

$containerNames = @(
    "aidevs-ollama",
    "aidevs-pgvector",
    "aidevs-redis"
)

foreach ($containerName in $containerNames) {
    $running = docker ps --filter "name=^/$containerName$" --format "{{.Names}}"
    if ($running -eq $containerName) {
        docker stop $containerName | Out-Null
        Write-Output "$containerName stopped"
    }
}

Write-Output "Containers and volumes were preserved."
