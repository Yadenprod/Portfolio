# PowerShell скрипт для автоматического создания песочниц Sandboxie
# Запускать от имени администратора!

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Создание песочниц Sandboxie" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Путь к Sandboxie (может отличаться)
$SanboxiePath = "C:\Program Files\Sandboxie-Plus"
$SandboxieIni = "$env:ProgramData\Sandboxie-Plus\Sandboxie.ini"

# Проверка наличия Sandboxie
if (-not (Test-Path $SanboxiePath)) {
    Write-Host "ОШИБКА: Sandboxie-Plus не найден по пути: $SanboxiePath" -ForegroundColor Red
    Write-Host "Установите Sandboxie-Plus или измените путь в скрипте" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Sandboxie-Plus найден: $SanboxiePath" -ForegroundColor Green
Write-Host ""

# Создаем 20 песочниц
$TotalSandboxes = 20

Write-Host "Создание $TotalSandboxes песочниц..." -ForegroundColor Yellow
Write-Host ""

for ($i = 1; $i -le $TotalSandboxes; $i++) {
    $sandboxName = "okno$i"
    
    Write-Host "Создание песочницы: $sandboxName" -ForegroundColor Cyan
    
    # Конфигурация для песочницы
    $config = @"

[$sandboxName]
Enabled=y
AutoDelete=n
ConfigLevel=10
BoxNameTitle=y
FileRootPath=%ProgramData%\Sandboxie-Plus\Sandbox\%SANDBOX%
Template=Default

"@
    
    # Добавляем конфигурацию в Sandboxie.ini
    try {
        Add-Content -Path $SandboxieIni -Value $config -ErrorAction Stop
        Write-Host "  ✓ $sandboxName создана" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ Ошибка создания $sandboxName : $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Создание завершено!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "ВАЖНО: Перезапустите Sandboxie-Plus чтобы изменения вступили в силу!" -ForegroundColor Yellow
Write-Host ""

# Спрашиваем, перезапустить ли Sandboxie
$restart = Read-Host "Перезапустить Sandboxie-Plus сейчас? (y/n)"

if ($restart -eq "y" -or $restart -eq "Y" -or $restart -eq "д" -or $restart -eq "Д") {
    Write-Host ""
    Write-Host "Перезапуск Sandboxie-Plus..." -ForegroundColor Yellow
    
    # Закрываем Sandboxie
    Stop-Process -Name "SandMan" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    
    # Запускаем снова
    Start-Process "$SanboxiePath\SandMan.exe"
    
    Write-Host "✓ Sandboxie-Plus перезапущен" -ForegroundColor Green
}

Write-Host ""
Write-Host "Готово! Теперь можно запускать main.py" -ForegroundColor Green
pause

