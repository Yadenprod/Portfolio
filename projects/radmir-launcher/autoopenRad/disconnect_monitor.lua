-- ============================================================================
-- Скрипт: Radmir Disconnect Logger (FIXED ENCODING)
-- Автор: -4 (помощник)
-- Версия: 1.2
-- Описание: Логирует отключения от сервера Radmir RP в текстовый файл.
--           Исправлена проблема с кодировкой русского текста в чате.
-- ============================================================================

script_name("Radmir Disconnect Logger")
script_version("1.2")
script_author("-4 (помощник)")

-- Путь к файлу логов. Файл будет создан в той же папке, что и сам скрипт.
local SCRIPT_DIR = thisScript().path:match("^(.*[/\\])") or "" -- Получаем директорию скрипта
local LOG_FILE_PATH = SCRIPT_DIR .. "radmir_disconnect_logs.txt"

-- Переменная для отслеживания предыдущего состояния подключения
local wasConnected = false

-- Функция для безопасного вывода кириллицы в SAMP чат
function samp_print_chat(message)
    -- Проверяем, доступна ли библиотека encoding (обычно есть в Moonloader 0.26+)
    if encoding then
        -- Конвертируем UTF-8 строку в Windows-1251 (CP1251), которую SAMP чат обычно ожидает
        sampAddChatMessage(encoding.encode(message, "CP1251"), -1)
    else
        -- Fallback для старых версий Moonloader или если encoding недоступен
        sampAddChatMessage(message, -1)
        print("[Radmir Disconnect Logger] WARNING: 'encoding' library not found. Cyrillic might be garbled in chat.")
    end
end

function main()
    -- Дожидаемся загрузки SAMP
    while not isSampLoaded() do
        wait(100)
    end
    samp_print_chat(" {FF00FF}[Radmir Disconnect Logger] {FFFFFF}Скрипт загружен! Проверка подключения...")
    samp_print_chat(" {FF00FF}[Radmir Disconnect Logger] {FFFFFF}Логи будут сохраняться в: {FFFF00}" .. LOG_FILE_PATH)
    print("[Radmir Disconnect Logger] Script loaded. Log file: " .. LOG_FILE_PATH) -- Вывод в moonloader.log всегда UTF-8

    -- Инициализируем wasConnected один раз после загрузки SAMP
    wasConnected = isSampConnected()
    samp_print_chat(string.format(" {FF00FF}[Radmir Disconnect Logger] {FFFFFF}Начальное состояние подключения: %s", tostring(wasConnected)))

    while true do
        wait(200) -- Проверяем состояние каждые 0.2 секунды

        local isCurrentlyConnected = isSampConnected()
        -- local currentTimestamp = os.date("%H:%M:%S") -- Отключим вывод времени для moonloader.log, чтобы не спамить сильно.
                -- print(string.format("[Radmir Disconnect Logger DEBUG] %s - isSampConnected: %s, wasConnected: %s", currentTimestamp, tostring(isCurrentlyConnected), tostring(wasConnected)))

        -- Логика обнаружения отключения
        if wasConnected and not isCurrentlyConnected then
            -- Мы были подключены, а теперь нет - значит, произошло отключение
            logDisconnect()
            samp_print_chat(" {FF00FF}[Radmir Disconnect Logger] {FF0000}!!! ОБНАРУЖЕНО ОТКЛЮЧЕНИЕ ОТ СЕРВЕРА !!! Информация записана в лог.")
            print("[Radmir Disconnect Logger] Disconnect detected and logged.")
        elseif not wasConnected and isCurrentlyConnected then
            -- Мы были отключены, а теперь подключились (например, после реконнекта)
            samp_print_chat(" {FF00FF}[Radmir Disconnect Logger] {00FF00}Вы подключились к серверу Radmir RP.")
            print("[Radmir Disconnect Logger] Reconnect detected.")
        end

        -- Обновляем состояние подключения для следующей итерации
        wasConnected = isCurrentlyConnected
    end
end

-- Функция для записи информации об отключении в файл
function logDisconnect()
    local timestamp = os.date("%Y-%m-%d %H:%M:%S") -- Получаем текущую дату и время
    local logMessage = string.format("[%s] Отключение от сервера Radmir RP.", timestamp)

    -- Открываем файл для добавления записи ("a" - append)
    local file = io.open(LOG_FILE_PATH, "a")
    if file then
        file:write(logMessage .. "\n")
        file:close()
        print("[Radmir Disconnect Logger] Successfully wrote to log file: " .. logMessage)
    else
        samp_print_chat(" {FF00FF}[Radmir Disconnect Logger] {FF0000}ОШИБКА: Не удалось записать лог в файл: {FFFF00}" .. LOG_FILE_PATH)
        print("[Radmir Disconnect Logger] ERROR: Failed to write to log file: " .. LOG_FILE_PATH)
    end
end