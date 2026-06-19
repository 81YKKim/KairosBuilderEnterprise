param(
    [string]$ProjectName = "Kairos Ultimate Enterprise X"
)

$Root = "C:\KairosBuilderEnterprise"
$ConfigPath = Join-Path $Root "builder\config\Config.json"
$StatePath = Join-Path $Root "builder\state\State.json"
$RegistryPath = Join-Path $Root "projects\ProjectRegistry.json"
$LogDir = Join-Path $Root "builder\logs"

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogPath = Join-Path $LogDir "Builder_$Timestamp.log"

function Write-Log {
    param([string]$Message)
    $Line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $Message"
    Write-Host $Line
    Add-Content -Path $LogPath -Value $Line
}

Write-Log "========================================"
Write-Log "Kairos Builder Enterprise v1.0"
Write-Log "========================================"

$Config = Get-Content $ConfigPath | ConvertFrom-Json
$State = Get-Content $StatePath | ConvertFrom-Json
$Registry = Get-Content $RegistryPath | ConvertFrom-Json

$Project = $Registry.projects | Where-Object { $_.name -eq $ProjectName -and $_.enabled -eq $true } | Select-Object -First 1

if (-not $Project) {
    Write-Log "ERROR: Project not found or disabled: $ProjectName"
    exit 1
}

Write-Log "Project: $($Project.name)"
Write-Log "Repo Path: $($Project.repo_path)"

if (-not (Test-Path $Project.repo_path)) {
    Write-Log "ERROR: Repository path does not exist."
    exit 1
}

Push-Location $Project.repo_path

Write-Log "Checking Git status..."

git rev-parse --is-inside-work-tree *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Log "ERROR: Not a Git repository."
    Pop-Location
    exit 1
}

$CommitHash = git rev-parse HEAD
Write-Log "Latest Commit: $CommitHash"

$Status = git status --porcelain

if ($Status) {
    Write-Log "WARNING: Working tree has changes."
    $Status | ForEach-Object { Write-Log "CHANGE: $_" }
} else {
    Write-Log "Working tree clean."
}

Pop-Location

$State.last_commit = $CommitHash
$State.status = "checked"
$State | ConvertTo-Json -Depth 10 | Set-Content -Path $StatePath -Encoding UTF8

Write-Log "State updated."
Write-Log "Builder check completed."

exit 0
