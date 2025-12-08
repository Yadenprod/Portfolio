# Disable Sandboxie UAC prompts
# Run as Administrator!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Disable Sandboxie UAC Prompts" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check admin
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] Need Administrator!" -ForegroundColor Red
    pause
    exit 1
}

# Find Sandboxie.ini
$sandboxieIni = "$env:WINDIR\Sandboxie.ini"

if (-not (Test-Path $sandboxieIni)) {
    Write-Host "[ERROR] Sandboxie.ini not found!" -ForegroundColor Red
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

Write-Host "Configuring sandboxes to disable UAC prompts..." -ForegroundColor Cyan
Write-Host ""

# Settings to disable prompts
$globalSettings = @"

# Disable UAC prompts
NotifyDirectDiskAccess=n
NotifyInternetAccess=n
NotifyStartRunAccess=n

"@

# Add to GlobalSettings or create it
if ($config -match "(?m)^\[GlobalSettings\]") {
    # GlobalSettings exists, add our settings
    if ($config -notmatch "NotifyDirectDiskAccess") {
        $config = $config -replace "(\[GlobalSettings\][^\[]*?)(?=\[|$)", "`$1$globalSettings`r`n"
        Write-Host "[OK] Added notification settings to GlobalSettings" -ForegroundColor Green
    }
} else {
    # Create GlobalSettings
    $config = "[GlobalSettings]$globalSettings`r`n" + $config
    Write-Host "[OK] Created GlobalSettings with notification settings" -ForegroundColor Green
}

# For each sandbox, add settings
1..6 | ForEach-Object {
    $boxName = "okno$_"
    Write-Host "Configuring: $boxName" -ForegroundColor Yellow
    
    # Ensure section exists
    if ($config -notmatch "(?m)^\[$boxName\]") {
        $config += "`r`n[$boxName]`r`n"
        Write-Host "  -> Created section" -ForegroundColor Cyan
    }
    
    # Add settings to disable admin checks
    $boxSettings = @"
DropAdminRights=n
NotifyDirectDiskAccess=n
NotifyInternetAccess=n
NotifyStartRunAccess=n
"@
    
    if ($config -match "(?ms)(\[$boxName\].*?)(?=\[|$)") {
        $section = $Matches[1]
        
        # Add if not exists
        if ($section -notmatch "NotifyDirectDiskAccess") {
            $config = $config -replace "(\[$boxName\][^\[]*?)(?=\[|$)", "`$1$boxSettings`r`n"
            Write-Host "  [OK] Added settings" -ForegroundColor Green
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
Write-Host "IMPORTANT: Restart Sandboxie Control!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
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
Write-Host "Done! Now UAC prompts should be disabled." -ForegroundColor Green
Write-Host "Test: python test_single_account.py" -ForegroundColor Yellow
Write-Host ""
pause

