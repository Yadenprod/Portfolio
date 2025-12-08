@echo off
echo Запуск проекта Mobile Legends Cases
echo ==================================
echo.

if not exist "D:\XPL\xampp-control.exe" (
    echo Ошибка: XAMPP не установлен. Пожалуйста, следуйте инструкции по установке:
    type ИНСТРУКЦИЯ_УСТАНОВКИ.txt
    pause
    exit /b
)

echo Запускаем XAMPP Control Panel...
start "" "D:\XPL\xampp-control.exe"
echo.
echo Не забудьте активировать Apache и MySQL в панели управления XAMPP!
echo.
echo После запуска Apache и MySQL, вы можете открыть сайт по адресу:
echo - http://mobile-legends.local/
echo.
echo Для доступа к админ-панели:
echo - http://mobile-legends.local/admin/
echo   Логин: admin
echo   Пароль: 12345
echo.
pause 