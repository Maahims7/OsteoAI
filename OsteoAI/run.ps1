#!/usr/bin/env powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath
& ".\.venv\Scripts\Activate.ps1"
python app.py
Read-Host "Press Enter to exit"
