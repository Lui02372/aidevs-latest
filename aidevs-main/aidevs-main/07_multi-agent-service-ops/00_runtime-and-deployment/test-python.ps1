[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$config = Get-Content (Join-Path $PSScriptRoot 'launcher.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$failed = @()
foreach ($target in $config.targets) {
    if ($target.id -eq '00' -or $target.compose.Count -eq 0) { continue }
    $exe = Join-Path $PSScriptRoot ".venvs/$($target.pythonGroup)/Scripts/python.exe"
    if (-not (Test-Path -LiteralPath $exe)) { throw "Missing environment. Run setup-python.ps1 first." }
    Write-Host "Testing $($target.id): $($target.directory)"
    & $exe -m pytest (Join-Path $PSScriptRoot "$($target.directory)/backend") -q -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { $failed += $target.id }
}
if ($failed.Count) { throw "Failed targets: $($failed -join ', ')" }
Write-Host 'All six backend test suites passed.'
