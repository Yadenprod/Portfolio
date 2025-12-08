@echo off
chcp 65001 >nul
title RADMIR Multi-Account Launcher
color 0A

echo.
echo ============================================================
echo    RADMIR Multi-Account Launcher
echo    Автоматизация запуска через Sandboxie
echo ============================================================
echo.
echo Проверка прав администратора...

:: Проверка прав администратора
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Запущено с правами администратора
    echo.
) else (
    echo [ОШИБКА] Требуются права администратора!
    echo.
    echo Пожалуйста, запустите этот файл от имени администратора:
    echo 1. Щелкните правой кнопкой мыши по файлу
    echo 2. Выберите "Запуск от имени администратора"
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"

echo Запуск программы...
echo.

python main.py

if %errorLevel% neq 0 (
    echo.
    echo [ОШИБКА] Программа завершилась с ошибкой!
    echo Проверьте файл radmir_automation.log для деталей.
    echo.
)

pause

