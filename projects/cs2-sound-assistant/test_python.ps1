# Тест Python
Write-Host "🔍 Проверка установки Python..." -ForegroundColor Yellow

# Попробуем разные команды
$commands = @("python", "py", "python3")

foreach ($cmd in $commands) {
    Write-Host "Пробуем: $cmd --version" -ForegroundColor Cyan
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ $cmd работает: $result" -ForegroundColor Green
            break
        }
    } catch {
        Write-Host "❌ $cmd не работает" -ForegroundColor Red
    }
}

# Проверим переменную PATH
Write-Host "`n🔍 Проверка переменной PATH..." -ForegroundColor Yellow
$pythonPaths = $env:PATH -split ';' | Where-Object { $_ -like '*python*' }
foreach ($path in $pythonPaths) {
    Write-Host "Найден путь: $path" -ForegroundColor Cyan
}
