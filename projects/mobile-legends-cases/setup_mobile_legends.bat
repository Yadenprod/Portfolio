@echo off
echo Настройка проекта Mobile Legends Cases
echo =====================================

REM Проверяем, установлен ли XAMPP
if not exist "D:\XPL" (
    echo Ошибка: XAMPP не установлен в директории D:\XPL
    echo Пожалуйста, установите XAMPP перед запуском этого скрипта
    pause
    exit /b
)

echo [1/5] Копирование файла конфигурации виртуального хоста...
copy ml_apache_vhost.conf "D:\XPL\apache\conf\extra\httpd-vhosts.conf"

echo [2/5] Настройка hosts файла...
echo.
echo ВАЖНО: Для полной настройки требуются права администратора
echo Пожалуйста, добавьте следующую строку в ваш hosts файл (C:\Windows\System32\drivers\etc\hosts):
echo.
echo 127.0.0.1 mobile-legends.local
echo.
pause

echo [3/5] Создание базы данных и импорт структуры...
echo Запускаем MySQL...
start /b "MySQL" "D:\XPL\mysql\bin\mysqld.exe" --defaults-file="D:\XPL\mysql\bin\my.ini" --standalone --console
timeout /t 5

echo Создаем базу данных...
"D:\XPL\mysql\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS mobile_legends_cases CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

echo Импортируем структуру CMS...
"D:\XPL\mysql\bin\mysql.exe" -u root mobile_legends_cases < "D:\ML\html\cms.sql"

echo Импортируем структуру Mobile Legends...
"D:\XPL\mysql\bin\mysql.exe" -u root mobile_legends_cases < "D:\ML\mobile_legends_tables.sql"

echo [4/5] Настройка завершена!
echo.
echo [5/5] Запуск XAMPP...
start "" "D:\XPL\xampp-control.exe"

echo.
echo ===================================
echo Настройка проекта завершена!
echo.
echo Для доступа к сайту:
echo - Запустите Apache и MySQL в панели управления XAMPP
echo - Откройте http://mobile-legends.local/ в браузере
echo - Для доступа к админ-панели: http://mobile-legends.local/admin/
echo.
echo Логин: admin
echo Пароль: 12345
echo ===================================
echo.

pause 