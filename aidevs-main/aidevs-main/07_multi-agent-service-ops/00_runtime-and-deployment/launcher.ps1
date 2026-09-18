[CmdletBinding()]
param(
    [string]$Target,
    [ValidateSet('menu','list','guide','init','setup','test','start','switch','open','status','stop','check','logs')]
    [string]$Action = 'menu',
    [string]$Python = 'python',
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-LocalPath([string]$Relative) {
    $path = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot $Relative))
    $prefix = $PSScriptRoot.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $path.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path must stay inside runtime folder: $Relative"
    }
    return $path
}

function Invoke-Target($Entry, [string]$Operation) {
    $directory = Get-LocalPath $Entry.directory
    if (-not (Test-Path -LiteralPath $directory -PathType Container)) { throw "Missing directory: $directory" }
    if ($Operation -eq 'guide') {
        $guide = Get-LocalPath $Entry.guide
        if (-not (Test-Path -LiteralPath $guide -PathType Leaf)) { throw "Missing guide: $guide" }
        if ($DryRun) { Write-Host "Open: $guide" } else { Invoke-Item -LiteralPath $guide }
        return
    }
    if ($Entry.compose.Count -eq 0) {
        throw "Target $($Entry.id) is a guide. Use -Action guide. CI/CD runs on GitHub, not on this PC."
    }
    if ($Operation -eq 'open') {
        if (-not $Entry.url) { throw 'This target has no frontend. Use status instead.' }
        if ($DryRun) { Write-Host "Open: $($Entry.url)" } else { Start-Process $Entry.url }
        return
    }
    if ($Operation -in @('setup','test')) {
        $group = $Entry.pythonGroup
        if ($Operation -eq 'setup') {
            if ($DryRun) { Write-Host "setup-python.ps1 -Group $group -Python $Python"; return }
            & (Join-Path $PSScriptRoot 'setup-python.ps1') -Group $group -Python $Python
            return
        }
        if ($Entry.id -eq '00') { throw '00 has no backend tests. Use check/status instead.' }
        $exe = Get-LocalPath ".venvs/$group/Scripts/python.exe"
        $testDirectory = Join-Path $directory 'backend'
        if ($DryRun) { Write-Host "$exe -m pytest $testDirectory -q"; return }
        if (-not (Test-Path -LiteralPath $exe)) { throw 'Run -Action setup first.' }
        & $exe -m pytest $testDirectory -q -p no:cacheprovider
        if ($LASTEXITCODE -ne 0) { throw "Tests failed ($LASTEXITCODE)." }
        return
    }
    if ($Operation -eq 'init') {
        $destination = Join-Path $directory '.env'
        if (Test-Path -LiteralPath $destination) { Write-Host 'Existing .env preserved.'; return }
        $source = Get-LocalPath $Entry.envExample
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing env example: $source" }
        if ($DryRun) { Write-Host "Copy example to: $destination"; return }
        Copy-Item -LiteralPath $source -Destination $destination
        Write-Host "Created $destination - set an OpenAI or Gemini key before using the app."
        return
    }
    $files = @($Entry.compose)
    if ($Operation -eq 'stop') { [array]::Reverse($files) }
    Push-Location -LiteralPath $directory
    try {
        if (-not $DryRun) {
            if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker CLI not found. Install/start Docker Desktop; see ConnectGuide.md.' }
            & docker info --format '{{.ServerVersion}}'
            if ($LASTEXITCODE -ne 0) { throw 'Docker daemon is unavailable. Start Docker Desktop.' }
        }
        if ($Operation -eq 'start') {
            Invoke-Target $Entry 'init'
            # Validate both infrastructure and application before starting either.
            foreach ($file in $files) {
                $composePath = Get-LocalPath ($Entry.directory + '/' + $file)
                if (-not (Test-Path -LiteralPath $composePath -PathType Leaf)) { throw "Missing Compose file: $file" }
                Write-Host "[$($Entry.id)] docker compose -f $file config --quiet"
                if (-not $DryRun) {
                    & docker compose -f $file config --quiet
                    if ($LASTEXITCODE -ne 0) { throw "Compose validation failed: $file" }
                }
            }
        }
        foreach ($file in $files) {
            $composePath = Get-LocalPath ($Entry.directory + '/' + $file)
            if (-not (Test-Path -LiteralPath $composePath -PathType Leaf)) { throw "Missing Compose file: $file" }
            $arguments = @('compose', '-f', $file)
            switch ($Operation) {
                'start'  { $arguments += @('up', '-d', '--build', '--wait', '--wait-timeout', '180') }
                'status' { $arguments += @('ps', '--all') }
                'stop'   { $arguments += 'stop' }
                'check'  { $arguments += @('config', '--quiet') }
                'logs'   { $arguments += @('logs', '--tail', '80') }
            }
            Write-Host "[$($Entry.id)] docker $($arguments -join ' ')"
            if (-not $DryRun) {
                & docker @arguments
                if ($LASTEXITCODE -ne 0) { throw "Docker failed ($LASTEXITCODE). Check -Action logs and $($Entry.guide)." }
            }
        }
        if ($Operation -eq 'start' -and $Entry.url) {
            Write-Host "Frontend: $($Entry.url)"
            if ($Entry.PSObject.Properties.Name -contains 'backendUrl') {
                Write-Host "Backend API: $($Entry.backendUrl)/docs"
                Write-Host "Readiness: $($Entry.backendUrl)/health/ready"
            }
        }
    } finally { Pop-Location }
}

try {
    $config = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'launcher.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($config.version -ne 1) { throw 'Unsupported launcher.json version.' }
    if ($Action -in @('menu','list')) {
        $config.targets | Select-Object id, title, @{Name='servers';Expression={ $_.services -join ' + ' }} | Format-Table -AutoSize | Out-Host
        if ($Action -eq 'list') { exit 0 }
        Write-Host 'Run one application at a time (shared ports 8000 / 8501).'
        $Target = Read-Host 'Target ID (or q to quit)'
        if ($Target -eq 'q') { exit 0 }
        $Action = Read-Host 'Action: switch / start / open / status / stop / logs / guide / init / setup / test / check (Enter = switch app or open guide)'
        if (-not $Action) {
            $chosen = @($config.targets | Where-Object { $_.id -eq $Target })
            if ($chosen.Count -ne 1) { throw "Unknown target: $Target" }
            if ($chosen[0].compose.Count -eq 0) { $Action = 'guide' }
            elseif ($chosen[0].url) { $Action = 'switch' }
            else { $Action = 'start' }
        }
        if ($Action -notin @('guide','init','setup','test','start','switch','open','status','stop','check','logs')) { throw 'Unknown action.' }
    }
    $entries = @($config.targets | Where-Object { $_.id -eq $Target })
    if ($entries.Count -ne 1) { throw "Unknown or duplicate target: $Target. Use -Action list." }
    if ($Action -eq 'switch') {
        $selected = $entries[0]
        if (-not $selected.url -or $selected.compose.Count -eq 0) { throw 'Switch requires an application target: 01, 01-2, 01-3, 05, 06 or 07.' }
        Invoke-Target $selected 'init'
        Invoke-Target $selected 'check'
        Write-Host 'Switch: stopping the other configured local application stacks; database volumes are preserved.'
        foreach ($other in $config.targets) {
            if ($other.id -ne $selected.id -and $other.url -and $other.compose.Count -gt 0) {
                Invoke-Target $other 'stop'
            }
        }
        Invoke-Target $selected 'start'
    } else {
        Invoke-Target $entries[0] $Action
    }
    exit 0
} catch {
    Write-Error $_ -ErrorAction Continue
    exit 1
}
