# Apply Worlds Further git overrides to a local CurseForge instance.
# Does not change CurseForge addons. Does not touch saves/ or minecraftinstance.json.
param(
  [string]$Instance = $env:WORLD_FURTHER_INSTANCE,
  [switch]$DryRun,
  [switch]$SkipOptions,
  [switch]$SkipJars
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Overrides = Join-Path $RepoRoot "overrides"

if (-not (Test-Path (Join-Path $Overrides "config"))) {
  throw "Missing $Overrides\config — run this from a clone of worlds-further."
}

function Test-IsInstance([string]$Path) {
  return (Test-Path (Join-Path $Path "mods")) -and (Test-Path (Join-Path $Path "config"))
}

if (-not $Instance) {
  $roots = @(
    (Join-Path $env:USERPROFILE "curseforge\minecraft\Instances"),
    (Join-Path $env:USERPROFILE "Documents\curseforge\minecraft\Instances")
  ) | Where-Object { Test-Path $_ }
  $names = @("Worlds further", "Worlds Further", "WorldsFurther", "Ejomilishy")
  $hits = @()
  foreach ($root in $roots) {
    foreach ($name in $names) {
      $p = Join-Path $root $name
      if (Test-Path $p -and (Test-IsInstance $p)) { $hits += $p }
    }
  }
  if ($hits.Count -eq 1) { $Instance = $hits[0] }
  elseif ($hits.Count -gt 1) { throw "Multiple instances:`n$($hits -join "`n")`nPass -Instance PATH" }
  else { throw "No Worlds Further instance found. Pass -Instance PATH" }
}

$Instance = (Resolve-Path $Instance).Path
if (-not (Test-IsInstance $Instance)) {
  throw "Not a CurseForge instance (need mods\ and config\): $Instance"
}

Write-Host "Repo:     $RepoRoot"
Write-Host "Instance: $Instance"
if ($DryRun) { Write-Host "Mode:     dry-run" }

function Copy-Tree($From, $To) {
  if ($DryRun) {
    Write-Host "Would copy $From -> $To"
    return
  }
  New-Item -ItemType Directory -Force -Path $To | Out-Null
  Copy-Item -Path (Join-Path $From "*") -Destination $To -Recurse -Force
}

Copy-Tree (Join-Path $Overrides "config") (Join-Path $Instance "config")
if (Test-Path (Join-Path $Overrides "datapacks")) {
  Copy-Tree (Join-Path $Overrides "datapacks") (Join-Path $Instance "datapacks")
}
if (Test-Path (Join-Path $Overrides "defaultconfigs")) {
  Copy-Tree (Join-Path $Overrides "defaultconfigs") (Join-Path $Instance "defaultconfigs")
}
$shaderSrc = Join-Path $Overrides "shaderpacks"
$shaderDst = Join-Path $Instance "shaderpacks"
if (Test-Path $shaderSrc) {
  if ($DryRun) { Write-Host "Would copy shader *.txt -> $shaderDst" }
  else {
    New-Item -ItemType Directory -Force -Path $shaderDst | Out-Null
    Copy-Item (Join-Path $shaderSrc "*.txt") -Destination $shaderDst -Force
  }
}
if (-not $SkipOptions -and (Test-Path (Join-Path $Overrides "options.txt"))) {
  if ($DryRun) { Write-Host "Would copy options.txt" }
  else { Copy-Item (Join-Path $Overrides "options.txt") (Join-Path $Instance "options.txt") -Force }
}
foreach ($f in @("README.md", "CHANGELOG.md")) {
  $src = Join-Path $Overrides $f
  if (Test-Path $src) {
    if ($DryRun) { Write-Host "Would copy $f" }
    else { Copy-Item $src (Join-Path $Instance $f) -Force }
  }
}
if (-not $SkipJars -and (Test-Path (Join-Path $Overrides "mods"))) {
  $modDst = Join-Path $Instance "mods"
  if ($DryRun) { Write-Host "Would copy overrides\mods\*.jar -> $modDst" }
  else {
    New-Item -ItemType Directory -Force -Path $modDst | Out-Null
    Copy-Item (Join-Path $Overrides "mods\*.jar") -Destination $modDst -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "Done. Fully quit and relaunch CurseForge Minecraft so configs reload."
Write-Host "Addon list (manifest.json) is not applied — update mods in the CurseForge app."
