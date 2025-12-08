# Скрипт установки Python 64-бит
Write-Host "🎵 Установка Python 64-бит для CS2 Sound Assistant..." -ForegroundColor Green

# Скачиваем Python 64-бит
$url = "https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe"
$output = "python-64bit-installer.exe"

Write-Host "📥 Скачивание Python 3.13.7 64-бит..." -ForegroundColor Yellow
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "✅ Python 64-бит скачан успешно!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка скачивания: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Устанавливаем Python
Write-Host "🔧 Установка Python 64-бит..." -ForegroundColor Yellow
try {
    Start-Process -FilePath $output -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Write-Host "✅ Python 64-бит установлен успешно!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка установки: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Удаляем установщик
Remove-Item $output -Force

Write-Host "🎉 Python 64-бит установлен! Перезапустите PowerShell для применения изменений." -ForegroundColor Green
Write-Host "💡 После перезапуска выполните: python --version" -ForegroundColor Cyan
Write-Host "📋 Должно показать: Python 3.13.7 (64-bit)" -ForegroundColor Cyan
