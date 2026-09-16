param(
    [string]$Target = "C:\mini_agent_st\mini_agent_05_memory\learning_unit",
    [switch]$Check
)

$source = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$sourceFiles = Get-ChildItem -LiteralPath $source -Recurse -File | Where-Object {
    $_.FullName -notmatch "\\__pycache__\\" -and
    $_.FullName -notmatch "\\30_mcp\\" -and
    $_.Name -ne "sync_learning_unit.ps1"
}

if (-not (Test-Path -LiteralPath $Target)) {
    if ($Check) {
        throw "동기화 대상이 없습니다: $Target"
    }
    New-Item -ItemType Directory -Path $Target | Out-Null
}

$different = @()
foreach ($file in $sourceFiles) {
    $relative = $file.FullName.Substring($source.Length + 1)
    $targetFile = Join-Path $Target $relative
    $same = (Test-Path -LiteralPath $targetFile -PathType Leaf) -and
        ((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash -eq
         (Get-FileHash -LiteralPath $targetFile -Algorithm SHA256).Hash)
    if ($same) {
        continue
    }
    $different += $relative
    if (-not $Check) {
        $targetDirectory = Split-Path -Parent $targetFile
        if (-not (Test-Path -LiteralPath $targetDirectory)) {
            New-Item -ItemType Directory -Path $targetDirectory -Force | Out-Null
        }
        Copy-Item -LiteralPath $file.FullName -Destination $targetFile -Force
    }
}

if ($different.Count -eq 0) {
    Write-Output "learning_unit is synchronized."
    exit 0
}

$different | ForEach-Object { Write-Output "DIFF $_" }
if ($Check) {
    throw "learning_unit 동기화가 필요합니다."
}
Write-Output "Synchronized $($different.Count) file(s)."
