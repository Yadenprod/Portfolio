@echo off
echo =======================================
echo 🚀 Установка сервера для Telegram Casino
echo =======================================

echo.
echo 📦 Установка зависимостей Node.js...
npm install

echo.
echo ✅ Зависимости установлены!
echo.
echo 🚀 Запуск сервера и клиента...
echo.
echo 📋 Инструкции:
echo 1. Сервер запустится на http://localhost:3000
echo 2. Клиент запустится на http://localhost:5173
echo 3. WebSocket будет доступен на ws://localhost:3000/ws
echo.
echo 🔧 Для запуска в будущем используйте:
echo    npm run start
echo.

pause
npm run start
