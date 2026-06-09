# 🚀 SETUP.md — Portable AI Toolkit USB Setup Guide

> **Run everything below as Administrator in PowerShell unless noted otherwise.**

---

## ✅ STEP 1 — Plug In Your USB Drive

1. Plug your **32GB USB drive** into your computer
2. Open **File Explorer** and confirm it shows up as **Drive D:\**
   - If it shows a different letter, right-click the drive → **Change Drive Letter** → assign **D:**

---

## ✅ STEP 2 — Open PowerShell as Administrator

1. Press **Windows + S**, type `PowerShell`
2. Right-click **Windows PowerShell** → **Run as Administrator**
3. Click **Yes** on the UAC prompt
4. You should see: `PS C:\Windows\System32>`

---

## ✅ STEP 3 — Navigate to Your USB Drive

Copy and paste this command into PowerShell (Admin):

```powershell
Set-Location D:\
```

Confirm you're on the drive:

```powershell
Get-Location
```

Expected output: `Path: D:\`

---

## ✅ STEP 4 — Set PowerShell Execution Policy

Allow scripts to run from your USB:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

---

## ✅ STEP 5 — Create the Toolkit Folder Structure on D:\

Copy and paste this entire block into PowerShell (Admin):

```powershell
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\ai-voice-assistant"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\creative-file-manager"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\windows-recovery-tools"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\research-assistant"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\cross-machine-sync"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\scripts"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\config"
New-Item -ItemType Directory -Force -Path "D:\portable-ai-toolkit\docs"
Write-Host "Folder structure created on D:\" -ForegroundColor Green
```

---

## ✅ STEP 6 — Clone the GitHub Repository to D:\

```powershell
Set-Location D:\
git clone https://github.com/glennharlow/portable-ai-toolkit.git
Set-Location D:\portable-ai-toolkit
Write-Host "Repository cloned to D:\portable-ai-toolkit" -ForegroundColor Green
```

> **Don't have Git?** Install it first:
> ```powershell
> winget install --id Git.Git -e --source winget
> ```
> Then close and re-open PowerShell as Admin and re-run Step 6.

---

## ✅ STEP 7 — Install Python

```powershell
python --version
winget install --id Python.Python.3.11 -e --source winget
python --version
```

Expected output: `Python 3.11.x`

---

## ✅ STEP 8 — Install Required Python Packages

```powershell
Set-Location D:\portable-ai-toolkit
python -m pip install --upgrade pip
python -m pip install speechrecognition pyaudio pyttsx3 openai-whisper torch transformers pyyaml watchdog mutagen rich click
Write-Host "Python packages installed" -ForegroundColor Green
```

---

## ✅ STEP 9 — Run the Initialization Script

```powershell
Set-Location D:\portable-ai-toolkit
python scripts\initialize_ai.py
```

---

## ✅ STEP 10 — Test the Setup

```powershell
Set-Location D:\portable-ai-toolkit
python scripts\test_setup.py
```

All tests should return **PASS**.

---

## ✅ STEP 11 — Launch the Voice Assistant

```powershell
Set-Location D:\portable-ai-toolkit
python ai-voice-assistant\main.py
```

Say **"Hey AI"** to activate.

---

## 🔁 Quick Launch (Every Time You Plug In)

```powershell
Set-Location D:\portable-ai-toolkit
python ai-voice-assistant\main.py
```

Or double-click `D:\portable-ai-toolkit\START_HERE.bat`

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---|---|
| USB shows as E:\ or F:\ not D:\ | Right-click drive in File Explorer → Change Drive Letter → set to D: |
| `python` not recognized | Re-open PowerShell as Admin after installing Python |
| `git` not recognized | Re-open PowerShell as Admin after installing Git |
| Execution policy error | Re-run Step 4 |
| `pyaudio` install fails | Run: `pip install pipwin` then `pipwin install pyaudio` |
| Script blocked by antivirus | Temporarily disable real-time protection, run script, re-enable |

---

## 📋 All Commands — Quick Reference

```powershell
# 1. Go to USB
Set-Location D:\

# 2. Allow scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force

# 3. Clone repo
git clone https://github.com/glennharlow/portable-ai-toolkit.git
Set-Location D:\portable-ai-toolkit

# 4. Install packages
python -m pip install --upgrade pip
python -m pip install speechrecognition pyaudio pyttsx3 openai-whisper torch transformers pyyaml watchdog mutagen rich click

# 5. Initialize
python scripts\initialize_ai.py

# 6. Test
python scripts\test_setup.py

# 7. Launch
python ai-voice-assistant\main.py
```

---

*Generated for Glenn's Portable AI Toolkit — glennharlow/portable-ai-toolkit*
