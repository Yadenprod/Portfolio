# Скрипт установки Python
Write-Host "🎵 Установка Python для CS2 Sound Assistant..." -ForegroundColor Green

# Скачиваем Python
$url = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$output = "python-installer.exe"

Write-Host "📥 Скачивание Python 3.11.9..." -ForegroundColor Yellow
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "✅ Python скачан успешно!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка скачивания: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Устанавливаем Python
Write-Host "🔧 Установка Python..." -ForegroundColor Yellow
try {
    Start-Process -FilePath $output -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Write-Host "✅ Python установлен успешно!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ошибка установки: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Удаляем установщик
Remove-Item $output -Force

Write-Host "🎉 Python установлен! Перезапустите PowerShell для применения изменений." -ForegroundColor Green
Write-Host "💡 После перезапуска выполните: python --version" -ForegroundColor Cyan
