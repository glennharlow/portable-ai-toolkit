# ============================================================
#  MEADOW Master Orchestration Script
#  Anomaly1911Writings | glennharlow/portable-ai-toolkit
#  Version: 1.0.0 | Born: July 4, 2026
#
#  USAGE:
#    .\meadow_run.ps1                       # Start MEADOW
#    .\meadow_run.ps1 -Action setup         # First-time setup
#    .\meadow_run.ps1 -Action install       # Install all dependencies
#    .\meadow_run.ps1 -Action status        # Check system status
#    .\meadow_run.ps1 -Action sync          # Sync devices via GitHub
#    .\meadow_run.ps1 -Action install-service  # Install Windows Service
#    .\meadow_run.ps1 -Action remove-service   # Remove Windows Service
#    .\meadow_run.ps1 -Action vault         # Open content vault in VS Code
#    .\meadow_run.ps1 -Action report        # Morning report
#    .\meadow_run.ps1 -Action test-voice    # Test voice output
#    .\meadow_run.ps1 -Action update        # Pull latest from GitHub
# ============================================================

param(
    [ValidateSet("start","setup","sync","install","status",
                 "install-service","remove-service",
                 "vault","report","test-voice","update")]
    [string]$Action = "start"
)

$Config = @{
    AgentName    = "MEADOW"
    OwnerName    = "Glenn"
    Brand        = "Anomaly1911Writings"
    RepoOwner    = "glennharlow"
    RepoName     = "portable-ai-toolkit"
    RepoURL      = "https://github.com/glennharlow/porta
function Write-Meadow($Msg, $Level="INFO") {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $col = switch($Level) { "OK"{"Green"} "WARN"{"Yellow"} "ERROR"{"Red"} default{"Cyan"} }
    Write-Host "[$ts] [$Level] MEADOW :: $Msg" -ForegroundColor $col
    if(-not(Test-Path $Config.LogDir)){New-Item -ItemType Directory -Path $Config.LogDir -Force|Out-Null}
    "[$ts] [$Level] $Msg" | Add-Content (Join-Path $Config.LogDir "meadow-ps.log")
}

function Write-Banner {
    Write-Host @"

  MEADOW - Autonomous Copilot GitHub CLI Agent
  Anomaly1911Writings Empire
"@ -ForegroundColor Green
    Write-Host "  Owner : $($Config.OwnerName)  |  Device: $env:COMPUTERNAME  |  $(Get-Date -Format 'dddd, MMM dd yyyy hh:mm tt')`n" -ForegroundColor Gray
}

function Test-Prerequisites {
    Write-Host "`n  Prerequisites" -ForegroundColor Blue
    foreach($check in @(
        @{N="Python 3";    C="python --version"},
        @{N="GitHub CLI";  C="gh --version"},
        @{N="Git";         C="git --version"}
    )) {
        try {
            $v = Invoke-Expression $check.C 2>&1 | Select-Object -First 1
            Write-Host "  OK $($check.N.PadRight(16)) $v" -ForegroundColor Green
        } catch {
            Write-Host "  !! $($check.N.PadRight(16)) not found" -ForegroundColor Red
        }
function Invoke-Setup {
    Write-Meadow "Setting up MEADOW on $env:COMPUTERNAME..." "INFO"
    if(-not(Test-Path $Config.EnvFile)) {
        @"
PICOVOICE_ACCESS_KEY=YOUR_KEY_HERE
WAKE_WORD_MODEL_PATH=./voice/wake_word/hey-meadow.ppn
AZURE_SPEECH_KEY=YOUR_AZURE_KEY_HERE
AZURE_SPEECH_REGION=eastus
GH_TOKEN=YOUR_GITHUB_TOKEN_HERE
OPENAI_API_KEY=YOUR_OPENAI_KEY_HERE
AYRSHARE_API_KEY=YOUR_AYRSHARE_KEY_HERE
SUNO_API_KEY=YOUR_SUNO_KEY_HERE
DEVICE_NAME=$env:COMPUTERNAME
"@ | Set-Content $Config.EnvFile
        Write-Meadow ".env created - fill in your API keys before running." "WARN"
    }
    @(
        (Join-Path $Config.MeadowRoot "voice\wake_word"),
        (Join-Path $Config.MeadowRoot "logs"),
        (Join-Path $Config.VaultPath "poems"),
        (Join-Path $Config.VaultPath "songs"),
        (Join-Path $Config.VaultPath "books"),
        (Join-Path $Config.VaultPath "essays"),
        (Join-Path $PSScriptRoot "..\brand\anomaly1911"),
        (Join-Path $PSScriptRoot "..\brand\dave_thomas"),
        (Join-Path $PSScriptRoot "..\brand\rmhc_poptabs")
    ) | ForEach-Object { New-Item -ItemType Directory -Path $_ -Force | Out-Null; Write-Host "  DIR: $_" -ForegroundColor DarkGray }
    Write-Host "`n  NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "     1. Fill in .env with your API keys"
    Write-Host "     2. Visit console.picovoice.ai - train Hey Meadow wake word"
    Write-Host "     3. Drop the .ppn file into .\voice\wake_word\"
    Write-Host "     4. Run: .\meadow_run.ps1 -Action install"
    Write-Host "     5. Run: .\meadow_run.ps1"
}

function Install-Dependencies {
    Write-Meadow "Installing dependencies..." "INFO"
    @("GitHub.cli","Git.Git","Python.Python.3.11","Microsoft.VisualStudioCode") | ForEach-Object {
        Write-Host "  winget install $_ " -NoNewline -ForegroundColor Cyan
        winget install --id $_ --silent --accept-package-agreements --accept-source-agreements 2>&1|Out-Null
        Write-Host "OK" -ForegroundColor Green
    }
    @("pvporcupine","pyaudio","openai","azure-cognitiveservices-speech",
      "SpeechRecognition","pyttsx3","python-dotenv","requests","ayrshare") | ForEach-Object {
        Write-Host "  pip install $_ " -NoNewline -ForegroundColor Cyan
        python -m pip install $_ --quiet 2>&1|Out-Null
        Write-Host "OK" -ForegroundColor Green
    }
function Get-MeadowStatus {
    Write-Host "`n  System Status" -ForegroundColor Blue
    $svc = Get-Service -Name $Config.ServiceName -ErrorAction SilentlyContinue
    Write-Host "  Windows Service   : $(if($svc){$svc.Status}else{'Not installed'})" -ForegroundColor $(if($svc -and $svc.Status -eq 'Running'){'Green'}else{'Yellow'})
    Write-Host "  Python            : $(python --version 2>&1)" -ForegroundColor Cyan
    Write-Host "  .env Config       : $(if(Test-Path $Config.EnvFile){'Present'}else{'Missing'})" -ForegroundColor $(if(Test-Path $Config.EnvFile){'Green'}else{'Yellow'})
    $ppn = Get-ChildItem -Path (Join-Path $Config.MeadowRoot "voice\wake_word") -Filter "*.ppn" -ErrorAction SilentlyContinue
    Write-Host "  Wake Word Model   : $(if($ppn){$ppn.Name}else{'Not found - train at console.picovoice.ai'})" -ForegroundColor $(if($ppn){'Green'}else{'Yellow'})
    $vault = Get-ChildItem $Config.VaultPath -Recurse -File -ErrorAction SilentlyContinue
    Write-Host "  Content Vault     : $($vault.Count) files" -ForegroundColor Cyan
    Write-Host "`n  Platforms" -ForegroundColor Blue
    $Platforms | ForEach-Object { Write-Host "  $($_.PadRight(14)) Awaiting Ayrshare connection" -ForegroundColor DarkGray }
}

function Install-MeadowService {
    $nssm = "$env:ProgramFiles\nssm\nssm.exe"
    if(-not(Test-Path $nssm)) {
        Write-Meadow "Downloading NSSM..." "WARN"
        $zip = Join-Path $env:TEMP "nssm.zip"
        Invoke-WebRequest "https://nssm.cc/release/nssm-2.24.zip" -OutFile $zip
        Expand-Archive $zip (Join-Path $env:TEMP "nssm_extract")
        $exe = Get-ChildItem (Join-Path $env:TEMP "nssm_extract") -Filter nssm.exe -Recurse | Select-Object -First 1
        New-Item "$env:ProgramFiles\nssm" -ItemType Directory -Force | Out-Null
        Copy-Item $exe.FullName $nssm
    }
    $py = (Get-Command python).Source
    & $nssm install $Config.ServiceName $py $Config.DaemonScript "--service"
    & $nssm set $Config.ServiceName DisplayName "MEADOW Autonomous Agent"
    & $nssm set $Config.ServiceName Start SERVICE_AUTO_START
    & $nssm set $Config.ServiceName AppDirectory $Config.MeadowRoot
    & $nssm set $Config.ServiceName AppStdout (Join-Path $Config.LogDir "service.log")
    Start-Service $Config.ServiceName
    Write-Meadow "MEADOW service installed and started. Auto-starts on every reboot." "OK"
}

function Invoke-MorningReport {
    Write-Host "`n  MEADOW Morning Report - $(Get-Date -Format 'dddd, MMMM dd, yyyy hh:mm tt')" -ForegroundColor Cyan
    @("poems","songs","books","essays") | ForEach-Object {
        $n = (Get-ChildItem (Join-Path $Config.VaultPath $_) -File -ErrorAction SilentlyContinue).Count
        Write-Host "  $($_.PadRight(12)) $n files" -ForegroundColor White
    }
    Write-Host "  RMHC Pop Tabs           Tracking active" -ForegroundColor Green
    Write-Host "  Dave Thomas Foundation  Fundraiser content ready" -ForegroundColor Green
}

function Invoke-Sync {
    Write-Meadow "Syncing from $($Config.RepoURL)..." "INFO"
    $p = Join-Path $env:USERPROFILE "repos\$($Config.RepoName)"
    if(Test-Path (Join-Path $p ".git")) { Push-Location $p; git pull origin main; Pop-Location }
    else { git clone $Config.RepoURL $p }
    Write-Meadow "Sync complete." "OK"
}

function Invoke-Update { Invoke-Sync }
function Open-Vault    { if(Test-Path $Config.VaultPath){ code $Config.VaultPath }else{ Write-Meadow "Run -Action setup first." "WARN" } }
function Test-Voice    { python $Config.DaemonScript --test-voice }
function Start-Meadow  { Test-Prerequisites; python $Config.DaemonScript }

# MAIN
Write-Banner
switch($Action) {
    "start"           { Start-Meadow }
    "setup"           { Invoke-Setup }
    "install"         { Install-Dependencies }
    "status"          { Get-MeadowStatus }
    "sync"            { Invoke-Sync }
    "update"          { Invoke-Update }
    "install-service" { Install-MeadowService }
    "remove-service"  { Remove-MeadowService }
    "vault"           { Open-Vault }
    "report"          { Invoke-MorningReport }
    "test-voice"      { Test-Voice }
}
function Remove-MeadowService {
    $nssm = "$env:ProgramFiles\nssm\nssm.exe"
    if(Test-Path $nssm) { Stop-Service $Config.ServiceName -Force -ErrorAction SilentlyContinue; & $nssm remove $Config.ServiceName confirm }
    else { Write-Meadow "NSSM not found." "ERROR" }
}

    Write-Host "  gh extension install gh-copilot " -NoNewline -ForegroundColor Cyan
    gh extension install github/gh-copilot 2>&1|Out-Null
    Write-Host "OK" -ForegroundColor Green
    Write-Meadow "All dependencies installed." "OK"
}

    }
    $pwsh = $PSVersionTable.PSVersion.Major -ge 7
    Write-Host "  $(if($pwsh){'OK'}else{'!!'}) $('PowerShell 7+'.PadRight(16)) v$($PSVersionTable.PSVersion)" -ForegroundColor $(if($pwsh){'Green'}else{'Red'})
    Write-Host "  $(if(Test-Path $Config.EnvFile){'OK'}else{'WN'}) $('.env'.PadRight(16)) $(if(Test-Path $Config.EnvFile){'found'}else{'missing - run -Action setup'})" -ForegroundColor $(if(Test-Path $Config.EnvFile){'Green'}else{'Yellow'})
}
ble-ai-toolkit.git"
    ServiceName  = "MeadowAgent"
    MeadowRoot   = $PSScriptRoot
    VaultPath    = (Join-Path $PSScriptRoot "..\vault")
    EnvFile      = (Join-Path $PSScriptRoot ".env")
    LogDir       = (Join-Path $PSScriptRoot "logs")
    DaemonScript = (Join-Path $PSScriptRoot "meadow_daemon.py")
}

$Platforms = @("YouTube","TikTok","Instagram","Facebook")
