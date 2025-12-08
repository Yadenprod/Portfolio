@echo off
echo 🎵 Установка виртуального аудио устройства для CS2 Sound Assistant
echo.
echo Этот скрипт поможет установить виртуальное аудио устройство
echo для захвата системного звука из CS2
echo.

echo 📋 Варианты решения:
echo.
echo 1. Установить VB-Cable Virtual Audio Device (рекомендуется)
echo 2. Использовать встроенные возможности Windows
echo 3. Настроить существующие драйверы
echo.

echo 🔧 Попробуем установить VB-Cable...
echo.

echo 📥 Скачивание VB-Cable...
powershell -Command "Invoke-WebRequest -Uri 'https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack43.zip' -OutFile 'VBCABLE_Driver_Pack43.zip'"

if exist "VBCABLE_Driver_Pack43.zip" (
    echo ✅ Файл скачан успешно
    echo.
    echo 📦 Распаковка архива...
    powershell -Command "Expand-Archive -Path 'VBCABLE_Driver_Pack43.zip' -DestinationPath 'VBCABLE_Driver_Pack43' -Force"
    
    if exist "VBCABLE_Driver_Pack43" (
        echo ✅ Архив распакован
        echo.
        echo 🔧 Запуск установщика...
        echo Пожалуйста, следуйте инструкциям установщика
        echo.
        start "" "VBCABLE_Driver_Pack43\VBCABLE_Setup_x64.exe"
    ) else (
        echo ❌ Ошибка распаковки
    )
) else (
    echo ❌ Ошибка скачивания
    echo.
    echo 💡 Альтернативное решение:
    echo 1. Скачайте VB-Cable вручную с сайта: https://vb-audio.com/Cable/
    echo 2. Установите драйвер
    echo 3. Перезагрузите компьютер
    echo 4. Запустите систему снова
)

echo.
echo После установки VB-Cable:
echo 1. Перезагрузите компьютер
echo 2. Запустите CS2
echo 3. Запустите систему: run_system.bat
echo.

pause
