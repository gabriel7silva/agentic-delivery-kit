# PACT kit — same steps as `make check`, for a Windows machine without make.
# Adopters never need this file. Exit code is the first failing level.

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
Set-Location $Root

$Py = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "python3" }
$Scripts = Join-Path $Root "automation\scripts"

function Invoke-Level {
    param([string]$Name, [string[]]$Args)
    Write-Host "=== $Name ==="
    & $Py @Args
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL $Name (exit $LASTEXITCODE)"
        exit $LASTEXITCODE
    }
}

Invoke-Level "L0 leaks" @((Join-Path $Scripts "check_leaks.py"))
Invoke-Level "L1 links" @((Join-Path $Scripts "check_links.py"))
Invoke-Level "L1 entry" @((Join-Path $Scripts "entry_points.py"), "--check")
Invoke-Level "L2 schemas" @((Join-Path $Scripts "check_schemas.py"))
Invoke-Level "L2 mapping" @((Join-Path $Scripts "check_mapping.py"))
Invoke-Level "L3 test" @("-m", "pytest", "automation/tests", "-q")
Invoke-Level "L5 canon" @((Join-Path $Scripts "check_canon.py"))
Invoke-Level "L5 adapters" @((Join-Path $Scripts "check_adapters.py"))
Invoke-Level "L6 instance" @((Join-Path $Scripts "check_instance.py"))

Write-Host ""
Write-Host "All checks passed."
