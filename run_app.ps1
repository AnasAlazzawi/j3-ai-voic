#!/usr/bin/env pwsh

Write-Host "🤖 Telegram AI Voice Assistant Bot Launcher" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan
Set-Location "C:\Users\ONYX-STORE\Downloads\New folder (7)"

Write-Host "Choose an option:" -ForegroundColor Yellow
Write-Host "1. Start Main Bot (main.py)" -ForegroundColor White
Write-Host "2. Test TTS Only (text_to_speech.py)" -ForegroundColor White
Write-Host "3. Test Simple Example (simple_example.py)" -ForegroundColor White
Write-Host "4. Exit" -ForegroundColor White

$choice = Read-Host "Enter your choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🚀 Starting Main Telegram Bot..." -ForegroundColor Green
        Write-Host "Press Ctrl+C to stop the bot" -ForegroundColor Yellow
        & "C:/Users/ONYX-STORE/Downloads/New folder (7)/.venv/Scripts/python.exe" "main.py"
    }
    "2" {
        Write-Host "� Testing TTS functionality..." -ForegroundColor Green
        & "C:/Users/ONYX-STORE/Downloads/New folder (7)/.venv/Scripts/python.exe" "text_to_speech.py"
    }
    "3" {
        Write-Host "� Testing Simple Example..." -ForegroundColor Green
        & "C:/Users/ONYX-STORE/Downloads/New folder (7)/.venv/Scripts/python.exe" "simple_example.py"
    }
    "4" {
        Write-Host "👋 Goodbye!" -ForegroundColor Cyan
        exit
    }
    default {
        Write-Host "❌ Invalid choice. Please try again." -ForegroundColor Red
    }
}

Write-Host "Application finished." -ForegroundColor Green
Read-Host "Press Enter to exit"
