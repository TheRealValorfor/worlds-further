# Windows wrapper around the cross-platform Python script.
# Usage: .\scripts\apply-to-instance.ps1 [--instance PATH] [--dry-run] [--skip-options] [--skip-jars]
$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "apply-to-instance.py"
$py = $null
foreach ($cmd in @("py", "python3", "python")) {
  $found = Get-Command $cmd -ErrorAction SilentlyContinue
  if ($found) { $py = $found.Source; break }
}
if (-not $py) {
  Write-Error "Python 3 is required. Install it from https://www.python.org/downloads/ then retry."
}
& $py $script @args
exit $LASTEXITCODE
