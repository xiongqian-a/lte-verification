$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot
python -X utf8 .\run_official_suite.py @args
exit $LASTEXITCODE
