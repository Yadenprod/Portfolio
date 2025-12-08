# PowerShell скрипт для запуска автоматического обновления прокси
# Обновляет прокси каждые 5 минут из GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " АВТОМАТИЧЕСКОЕ ОБНОВЛЕНИЕ ПРОКСИ" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Запуск в режиме демона..." -ForegroundColor Yellow
Write-Host "Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host ""

# Запускаем Python скрипт
python download_proxies.py --daemon

Write-Host ""
Write-Host "Обновление прокси остановлено." -ForegroundColor Red
Read-Host "Нажмите Enter для выхода"

