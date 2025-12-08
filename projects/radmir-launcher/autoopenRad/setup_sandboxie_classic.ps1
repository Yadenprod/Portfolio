# PowerShell script for Sandboxie Classic setup
# Run as Administrator!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sandboxie Classic Setup" -ForegroundColor Cyan
Write-Host "for RADMIR automation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: Administrator rights required!" -ForegroundColor Red
    Write-Host "Run this script as Administrator" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "[OK] Administrator rights: granted" -ForegroundColor Green
Write-Host ""

# Find Sandboxie config file
$sandboxieIniPaths = @(
    "$env:WINDIR\Sandboxie.ini",
    "C:\Windows\Sandboxie.ini",
    "$env:ProgramData\Sandboxie\Sandboxie.ini",
    "C:\Program Files\Sandboxie\Sandboxie.ini"
)

$sandboxieIni = $null
foreach ($path in $sandboxieIniPaths) {
    if (Test-Path $path) {
        $sandboxieIni = $path
        Write-Host "[OK] Found config file: $path" -ForegroundColor Green
        break
    }
}

if (-not $sandboxieIni) {
    Write-Host "[ERROR] Sandboxie.ini not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Checked paths:" -ForegroundColor Yellow
    foreach ($path in $sandboxieIniPaths) {
        Write-Host "  - $path" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Make sure Sandboxie Classic is installed" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host ""

# Create backup
$backupPath = "$sandboxieIni.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
try {
    Copy-Item $sandboxieIni $backupPath -Force
    Write-Host "[OK] Backup created:" -ForegroundColor Green
    Write-Host "  $backupPath" -ForegroundColor Gray
} catch {
    Write-Host "[WARN] Could not create backup: $_" -ForegroundColor Yellow
}

Write-Host ""

# Read configuration
Write-Host "Reading Sandboxie configuration..." -ForegroundColor Cyan

try {
    $config = Get-Content $sandboxieIni -Raw -Encoding Unicode
} catch {
    try {
        $config = Get-Content $sandboxieIni -Raw -Encoding UTF8
    } catch {
        $config = Get-Content $sandboxieIni -Raw
    }
}

Write-Host "[OK] Configuration loaded" -ForegroundColor Green
Write-Host ""

# Configure 6 sandboxes
Write-Host "Configuring sandboxes..." -ForegroundColor Cyan
Write-Host ""

$boxesConfigured = 0
$boxesCreated = 0

1..6 | ForEach-Object {
    $boxName = "okno$_"
    Write-Host "Processing sandbox: $boxName" -ForegroundColor Yellow
    
    # Check if section exists
    if ($config -notmatch "(?m)^\[$boxName\]") {
        Write-Host "  -> Creating new section [$boxName]" -ForegroundColor Cyan
        $config += "`r`n[$boxName]`r`n"
        $boxesCreated++
    }
    
    # Check and add DropAdminRights=n
    $sectionPattern = "(?ms)\[$boxName\].*?(?=\[|$)"
    if ($config -match $sectionPattern) {
        $section = $Matches[0]
        
        if ($section -notmatch "DropAdminRights") {
            # Add DropAdminRights to section
            $config = $config -replace "(\[$boxName\])", "`$1`r`nDropAdminRights=n"
            Write-Host "  [OK] Added: DropAdminRights=n" -ForegroundColor Green
            $boxesConfigured++
        } elseif ($section -match "DropAdminRights=y") {
            # Change y to n
            $config = $config -replace "(\[$boxName\][^\[]*?)DropAdminRights=y", "`$1DropAdminRights=n"
            Write-Host "  [OK] Changed: DropAdminRights=y -> DropAdminRights=n" -ForegroundColor Green
            $boxesConfigured++
        } else {
            Write-Host "  [OK] Already configured" -ForegroundColor Green
        }
    }
    
    Write-Host ""
}

# Save changes
Write-Host "Saving configuration..." -ForegroundColor Cyan

try {
    $config | Set-Content $sandboxieIni -Encoding Unicode -Force
    Write-Host "[OK] Configuration saved" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Save failed: $_" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Results:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sandboxes created: $boxesCreated" -ForegroundColor $(if ($boxesCreated -gt 0) { "Green" } else { "Gray" })
Write-Host "Sandboxes configured: $boxesConfigured" -ForegroundColor $(if ($boxesConfigured -gt 0) { "Green" } else { "Gray" })
Write-Host ""

if ($boxesCreated -gt 0 -or $boxesConfigured -gt 0) {
    Write-Host "[SUCCESS] Setup completed!" -ForegroundColor Green
} else {
    Write-Host "[INFO] All sandboxes were already configured" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. Restart Sandboxie Control" -ForegroundColor White
Write-Host "2. Check that sandboxes okno1-okno6 are visible" -ForegroundColor White
Write-Host "3. Run: python check_environment.py" -ForegroundColor White
Write-Host "4. Run: python test_single_account.py" -ForegroundColor White
Write-Host ""

# Offer to restart Sandboxie
$restart = Read-Host "Restart Sandboxie Control now? (y/n)"

if ($restart -eq "y" -or $restart -eq "Y") {
    Write-Host ""
    Write-Host "Restarting Sandboxie Control..." -ForegroundColor Yellow
    
    # Close all Sandboxie processes
    Get-Process | Where-Object {$_.Name -like "*Sandboxie*" -or $_.Name -like "*SbieCtrl*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    # Find and start SbieCtrl.exe
    $sbieCtrlPaths = @(
        "C:\Program Files\Sandboxie\SbieCtrl.exe",
        "C:\Program Files (x86)\Sandboxie\SbieCtrl.exe"
    )
    
    $found = $false
    foreach ($path in $sbieCtrlPaths) {
        if (Test-Path $path) {
            Start-Process $path
            Write-Host "[OK] Sandboxie Control started" -ForegroundColor Green
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "[WARN] Could not find SbieCtrl.exe" -ForegroundColor Yellow
        Write-Host "Start Sandboxie Control manually" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Done! Press Enter to exit..." -ForegroundColor Green
pause
