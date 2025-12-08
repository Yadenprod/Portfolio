# PowerShell script to configure Sandboxie for RADMIR Launcher
# Run as Administrator!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sandboxie Configuration for RADMIR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Administrator rights required!" -ForegroundColor Red
    pause
    exit 1
}

# Find Sandboxie.ini
$sandboxieIni = "$env:WINDIR\Sandboxie.ini"

if (-not (Test-Path $sandboxieIni)) {
    Write-Host "[ERROR] Sandboxie.ini not found at: $sandboxieIni" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "[OK] Found: $sandboxieIni" -ForegroundColor Green
Write-Host ""

# Backup
$backupPath = "$sandboxieIni.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $sandboxieIni $backupPath -Force
Write-Host "[OK] Backup: $backupPath" -ForegroundColor Green
Write-Host ""

# Read config
try {
    $config = Get-Content $sandboxieIni -Raw -Encoding Unicode
} catch {
    try {
        $config = Get-Content $sandboxieIni -Raw -Encoding UTF8
    } catch {
        $config = Get-Content $sandboxieIni -Raw
    }
}

Write-Host "Configuring sandboxes for RADMIR..." -ForegroundColor Cyan
Write-Host ""

# Settings to add for each sandbox
$settings = @"

# RADMIR Launcher settings
DropAdminRights=n
BlockNetworkFiles=n
OpenWinClass=*
OpenPipePath=*
OpenConfPath=*
ClosedFilePath=!<BlockNetworkFiles>,!<WinSxsFiles>
ClosedKeyPath=!<InternetExplorer>,!<WindowsMediaPlayer>
ReadFilePath=%ProgramFiles%\Radic\RADMIR LAUNCHER\*
OpenFilePath=%ProgramFiles%\Radic\RADMIR LAUNCHER\*
"@

# Configure each sandbox
1..6 | ForEach-Object {
    $boxName = "okno$_"
    Write-Host "Configuring: $boxName" -ForegroundColor Yellow
    
    # Check if section exists
    if ($config -notmatch "(?m)^\[$boxName\]") {
        $config += "`r`n[$boxName]`r`n"
        Write-Host "  -> Created section" -ForegroundColor Cyan
    }
    
    # Find section and add settings
    if ($config -match "(?ms)(\[$boxName\].*?)(?=\[|$)") {
        $section = $Matches[1]
        
        # Remove old RADMIR settings if any
        $section = $section -replace "(?m)^# RADMIR Launcher settings.*?(?=\[|$)", ""
        
        # Add new settings
        if ($section -notmatch "# RADMIR Launcher settings") {
            # Find the end of the section
            $config = $config -replace "(\[$boxName\][^\[]*?)(?=\[|$)", "`$1$settings`r`n"
            Write-Host "  [OK] Added RADMIR settings" -ForegroundColor Green
        } else {
            Write-Host "  [OK] Already configured" -ForegroundColor Green
        }
    }
    
    Write-Host ""
}

# Save
try {
    $config | Set-Content $sandboxieIni -Encoding Unicode -Force
    Write-Host "[SUCCESS] Configuration saved!" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to save: $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Restart Sandboxie Control" -ForegroundColor White
Write-Host "2. Test: python test_single_account.py" -ForegroundColor White
Write-Host ""

$restart = Read-Host "Restart Sandboxie Control now? (y/n)"

if ($restart -eq "y" -or $restart -eq "Y") {
    Write-Host ""
    Write-Host "Restarting..." -ForegroundColor Yellow
    
    Get-Process | Where-Object {$_.Name -like "*Sandboxie*" -or $_.Name -like "*SbieCtrl*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    $sbieCtrlPaths = @(
        "C:\Program Files\Sandboxie\SbieCtrl.exe",
        "C:\Program Files (x86)\Sandboxie\SbieCtrl.exe"
    )
    
    foreach ($path in $sbieCtrlPaths) {
        if (Test-Path $path) {
            Start-Process $path
            Write-Host "[OK] Sandboxie Control started" -ForegroundColor Green
            break
        }
    }
}

Write-Host ""
Write-Host "Done! Press Enter to exit..." -ForegroundColor Green
pause

