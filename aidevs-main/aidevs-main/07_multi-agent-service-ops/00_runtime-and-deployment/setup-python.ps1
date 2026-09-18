[CmdletBinding()]
param(
    [ValidateSet('all','compose','weather')][string]$Group = 'all',
    [string]$Python = 'python'
)
$ErrorActionPreference = 'Stop'
if ($Python -eq 'python' -and -not (Get-Command python -ErrorAction SilentlyContinue)) {
    $existing = @('compose','weather') | ForEach-Object {
        Join-Path $PSScriptRoot ".venvs/$_/Scripts/python.exe"
    } | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($existing) { $Python = $existing }
    else { throw 'Python not found. Pass an installed Python 3.11+ executable with -Python.' }
}
$groups = if ($Group -eq 'all') { @('compose','weather') } else { @($Group) }
& $Python -c 'import sys; assert sys.version_info >= (3, 11), "Python 3.11+ required"'
if ($LASTEXITCODE -ne 0) { throw 'Pass an installed Python 3.11+ executable with -Python.' }
foreach ($name in $groups) {
    $venv = Join-Path $PSScriptRoot ".venvs/$name"
    $exe = Join-Path $venv 'Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $exe)) {
        & $Python -m venv $venv
        if ($LASTEXITCODE -ne 0) { throw "venv failed: $name" }
    }
    & $exe -m pip install -r (Join-Path $PSScriptRoot "requirements-$name.txt")
    if ($LASTEXITCODE -ne 0) { throw "pip install failed: $name" }
    & $exe -m pip check
    if ($LASTEXITCODE -ne 0) { throw "Dependency conflict: $name" }
    Write-Host "Ready: $exe"
}
