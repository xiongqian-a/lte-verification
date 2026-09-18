$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

Set-Location -LiteralPath $PSScriptRoot

function Refresh-ProcessPath {
    $values = @(
        $env:Path
        [Environment]::GetEnvironmentVariable("Path", "User")
        [Environment]::GetEnvironmentVariable("Path", "Machine")
    )
    $seen = @{}
    $segments = New-Object System.Collections.Generic.List[string]
    foreach ($value in $values) {
        if ([string]::IsNullOrWhiteSpace($value)) {
            continue
        }
        foreach ($segment in $value.Split(";")) {
            if ([string]::IsNullOrWhiteSpace($segment)) {
                continue
            }
            $key = $segment.Trim().ToLowerInvariant()
            if (-not $seen.ContainsKey($key)) {
                $seen[$key] = $true
                $segments.Add($segment.Trim())
            }
        }
    }
    $env:Path = $segments -join ";"
}

function Test-PythonCandidate {
    param(
        [Parameter(Mandatory = $true)][string]$Command,
        [string[]]$LaunchArgs = @()
    )
    try {
        $version = (& $Command @LaunchArgs --version 2>&1 | Out-String).Trim()
    } catch {
        return $null
    }
    if ($version -match "Python\s+3\.(\d+)") {
        $minor = [int]$Matches[1]
        if ($minor -ge 10) {
            return [pscustomobject]@{
                Command = $Command
                LaunchArgs = $LaunchArgs
                Version = $version
            }
        }
    }
    return $null
}

function Find-Python {
    Refresh-ProcessPath

    foreach ($name in @("python", "python3", "py")) {
        $command = Get-Command $name -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($command) {
            $launchArgs = if ($name -eq "py") { @("-3") } else { @() }
            $candidate = Test-PythonCandidate -Command $command.Source -LaunchArgs $launchArgs
            if ($candidate) {
                return $candidate
            }
        }
    }

    $patterns = @(
        (Join-Path $env:LOCALAPPDATA "Programs\Python\Python*\python.exe")
        (Join-Path $env:ProgramFiles "Python*\python.exe")
    )
    if (${env:ProgramFiles(x86)}) {
        $patterns += Join-Path ${env:ProgramFiles(x86)} "Python*\python.exe"
    }
    foreach ($pattern in $patterns) {
        $matches = Get-ChildItem -Path $pattern -File -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending
        foreach ($match in $matches) {
            $candidate = Test-PythonCandidate -Command $match.FullName
            if ($candidate) {
                return $candidate
            }
        }
    }
    return $null
}

function Install-Python {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "Python 3.10+ is missing and winget is unavailable. Install Python 3.10+ from https://www.python.org/downloads/windows/ and rerun bootstrap.ps1."
    }
    Write-Host "Python 3.10+ is missing; installing the current Python 3 user package with winget..."
    & $winget.Source install --id Python.Python.3.12 -e --scope user `
        --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        throw "winget could not install Python. Install Python 3.10+ manually and rerun bootstrap.ps1."
    }
}

$python = Find-Python
if (-not $python) {
    Install-Python
    $python = Find-Python
}
if (-not $python) {
    throw "Python installation was reported successfully, but no usable Python 3.10+ interpreter could be located. Install Python manually and rerun bootstrap.ps1."
}

Write-Host "Using $($python.Version)"
$entryPoint = ".\run_official_suite.py"
$runnerArgs = @($args)
if ($runnerArgs.Count -gt 0) {
    switch ($runnerArgs[0]) {
        "--colleague-replay" {
            $entryPoint = ".\runners\colleague_replay_verification.py"
            $runnerArgs = @($runnerArgs | Select-Object -Skip 1)
        }
        "--doctor" {
            $entryPoint = ".\runners\environment_doctor.py"
            $runnerArgs = @($runnerArgs | Select-Object -Skip 1)
        }
        "--verify-standards" {
            $entryPoint = ".\runners\verify_standards_bundle.py"
            $runnerArgs = @($runnerArgs | Select-Object -Skip 1)
        }
    }
}
$launchArgs = @($python.LaunchArgs) + @("-X", "utf8", $entryPoint) + $runnerArgs
& $python.Command @launchArgs
exit $LASTEXITCODE
