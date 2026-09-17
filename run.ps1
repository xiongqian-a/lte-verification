$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & $python.Source -X utf8 .\run_official_suite.py @args
    exit $LASTEXITCODE
}

$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    & $pyLauncher.Source -3 -X utf8 .\run_official_suite.py @args
    exit $LASTEXITCODE
}

& "$PSScriptRoot\bootstrap.ps1" @args
exit $LASTEXITCODE
