$ErrorActionPreference = "Stop"

$containerNames = @(
    "aidevs-pgvector",
    "aidevs-redis",
    "aidevs-ollama"
)

foreach ($containerName in $containerNames) {
    $runningName = docker ps --filter "name=^/$containerName$" --format "{{.Names}}"
    if ($runningName -eq $containerName) {
        docker stop $containerName | Out-Null
        Write-Output "$containerName stopped"
    }
    else {
        Write-Output "$containerName is not running"
    }
}

Write-Output "Named volumes were not removed. Data and Ollama models are preserved."
