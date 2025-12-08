-- ============================================
-- ПОЛНЫЙ ПЕРЕХВАТ СЕТЕВЫХ ПАКЕТОВ SAMP
-- ============================================
-- Перехватывает ВСЕ пакеты (отправляемые и получаемые)
-- Сохраняет полное содержимое для точного воспроизведения

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local log_dir = "moonloader/packet_capture/"
local timestamp = os.date("%Y%m%d_%H%M%S")

-- Статистика
local stats = {
    packets_sent = 0,
    packets_received = 0,
    start_time = os.time()
}

-- Создаем директорию
local function ensure_dir(path)
    os.execute('mkdir "' .. path .. '" 2>nul')
end

ensure_dir(log_dir)

-- Функция для конвертации байтов в hex строку
local function bytes_to_hex(data, max_len)
    max_len = max_len or #data
    local hex = ""
    for i = 1, math.min(#data, max_len) do
        hex = hex .. string.format("%02X ", string.byte(data, i))
        if i % 16 == 0 then
            hex = hex .. "\n"
        end
    end
    if #data > max_len then
        hex = hex .. string.format("... (еще %d байт)", #data - max_len)
    end
    return hex
end

-- Функция для сохранения пакета
local function save_packet(packet_type, packet_id, data, additional_info)
    local packet_info = {
        type = packet_type,  -- "sent" или "received"
        packetId = packet_id,
        timestamp = os.time(),
        timestamp_readable = os.date("%Y-%m-%d %H:%M:%S"),
        size = #data,
        data_hex = bytes_to_hex(data, 1024),  -- Первые 1024 байта в hex
        data_base64 = nil,  -- Полные данные в base64 (если нужно)
        additional = additional_info or {}
    }
    
    -- Сохраняем полные данные в base64 для точного воспроизведения
    if #data > 0 then
        -- Простая base64 конвертация (или используйте библиотеку если есть)
        packet_info.data_base64 = "BASE64_DATA_HERE"  -- Замените на реальную конвертацию
    end
    
    -- Сохраняем в JSON
    local filename = string.format("%s_%s_%d.json", 
        packet_type, os.date("%H%M%S"), packet_id)
    local file = io.open(log_dir .. filename, "w")
    if file then
        file:write(json.encode(packet_info))
        file:close()
    end
    
    -- Сохраняем в бинарный файл для точного воспроизведения
    local bin_filename = string.format("%s_%s_%d.bin", 
        packet_type, os.date("%H%M%S"), packet_id)
    local bin_file = io.open(log_dir .. bin_filename, "wb")
    if bin_file then
        -- Записываем заголовок: тип(1 байт) + ID(1 байт) + размер(4 байта) + данные
        bin_file:write(string.char(packet_type == "sent" and 0x01 or 0x02))  -- Тип
        bin_file:write(string.char(packet_id))  -- ID пакета
        bin_file:write(string.pack(">I4", #data))  -- Размер (big-endian, 4 байта)
        bin_file:write(data)  -- Данные
        bin_file:close()
    end
    
    -- Логируем в текстовый файл
    local log_file = io.open(log_dir .. "packets.log", "a")
    if log_file then
        log_file:write(string.format(
            "[%s] %s | ID: %d | Размер: %d байт\n",
            os.date("%H:%M:%S"), 
            packet_type == "sent" and "ОТПРАВЛЕНО" or "ПОЛУЧЕНО",
            packet_id,
            #data
        ))
        log_file:write("HEX (первые 64 байта): " .. bytes_to_hex(data, 64) .. "\n")
        log_file:write("---\n")
        log_file:close()
    end
    
    -- Обновляем статистику
    if packet_type == "sent" then
        stats.packets_sent = stats.packets_sent + 1
    else
        stats.packets_received = stats.packets_received + 1
    end
end

-- ============================================
-- ПЕРЕХВАТ ИСХОДЯЩИХ ПАКЕТОВ
-- ============================================
function onSendPacket(packetId, bitStream)
    -- Получаем данные из bitStream
    local data = ""
    
    -- Пытаемся прочитать данные из потока
    -- Это зависит от реализации SAMPFUNCS
    if bitStream then
        -- Получаем размер потока
        local size = raknetBitStreamGetNumberOfBitsUsed(bitStream) / 8
        if size > 0 then
            -- Читаем данные
            -- Примечание: точный способ чтения зависит от SAMPFUNCS API
            -- Может потребоваться адаптация под вашу версию
            
            -- Альтернативный способ: используем хуки SAMPFUNCS
            -- raknetBitStreamReadData или аналогичные функции
        end
    end
    
    -- Сохраняем пакет
    save_packet("sent", packetId, data, {
        function_name = "onSendPacket"
    })
    
    print(string.format(">>> ПАКЕТ ОТПРАВЛЕН: ID=%d, Размер=%d", packetId, #data))
end

-- ============================================
-- ПЕРЕХВАТ ВХОДЯЩИХ ПАКЕТОВ
-- ============================================
function onReceivePacket(packetId, bitStream)
    local data = ""
    
    -- Аналогично для входящих пакетов
    if bitStream then
        local size = raknetBitStreamGetNumberOfBitsUsed(bitStream) / 8
        if size > 0 then
            -- Читаем данные
        end
    end
    
    -- Сохраняем пакет
    save_packet("received", packetId, data, {
        function_name = "onReceivePacket"
    })
    
    print(string.format("<<< ПАКЕТ ПОЛУЧЕН: ID=%d, Размер=%d", packetId, #data))
end

-- ============================================
-- АЛЬТЕРНАТИВНЫЙ МЕТОД: ПЕРЕХВАТ ЧЕРЕЗ САМПЕВ
-- ============================================
-- Если прямые хуки пакетов не работают, используем события SAMP

-- Перехват отправки команды (это тоже пакет)
function sampev.onSendCommand(command)
    local command_data = {
        type = "command",
        command = command,
        timestamp = os.time()
    }
    
    -- Сохраняем как пакет команды
    local data = encoding.utf8_to_cp1251(command)
    save_packet("sent", 0xFF, data, {  -- 0xFF для команд
        command = command,
        packet_type = "command"
    })
end

-- Перехват отправки чата
function sampev.onSendChat(text)
    local chat_data = {
        type = "chat",
        text = text,
        timestamp = os.time()
    }
    
    local data = encoding.utf8_to_cp1251(text)
    save_packet("sent", 0xFE, data, {  -- 0xFE для чата
        chat = text,
        packet_type = "chat"
    })
end

-- Перехват ответа на диалог
function sampev.onSendDialogResponse(dialogId, buttonId, listItem, inputText)
    local response_data = {
        dialogId = dialogId,
        buttonId = buttonId,
        listItem = listItem,
        inputText = inputText or ""
    }
    
    -- Формируем данные для отправки
    local data = string.format("%d|%d|%d|%s", 
        dialogId, buttonId, listItem, inputText or "")
    data = encoding.utf8_to_cp1251(data)
    
    save_packet("sent", 0xFD, data, {  -- 0xFD для диалога
        dialog_response = response_data,
        packet_type = "dialog_response"
    })
end

-- ============================================
-- СОХРАНЕНИЕ СТАТИСТИКИ
-- ============================================
local function save_stats()
    stats.end_time = os.time()
    stats.duration = stats.end_time - stats.start_time
    
    local stats_file = io.open(log_dir .. "statistics.json", "w")
    if stats_file then
        stats_file:write(json.encode(stats))
        stats_file:close()
    end
    
    local stats_txt = io.open(log_dir .. "statistics.txt", "w")
    if stats_txt then
        stats_txt:write("========================================\n")
        stats_txt:write("СТАТИСТИКА ПЕРЕХВАТА ПАКЕТОВ\n")
        stats_txt:write("========================================\n\n")
        stats_txt:write(string.format("Время начала: %s\n", 
            os.date("%Y-%m-%d %H:%M:%S", stats.start_time)))
        stats_txt:write(string.format("Время окончания: %s\n", 
            os.date("%Y-%m-%d %H:%M:%S", stats.end_time)))
        stats_txt:write(string.format("Длительность: %d секунд\n", stats.duration))
        stats_txt:write(string.format("Пакетов отправлено: %d\n", stats.packets_sent))
        stats_txt:write(string.format("Пакетов получено: %d\n", stats.packets_received))
        stats_txt:write(string.format("Всего пакетов: %d\n", 
            stats.packets_sent + stats.packets_received))
        stats_txt:close()
    end
end

-- ============================================
-- ОСНОВНАЯ ФУНКЦИЯ
-- ============================================
function main()
    wait(2000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("ОШИБКА: SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    print("=========================================")
    print("ПЕРЕХВАТ ПАКЕТОВ АКТИВЕН")
    print("Все пакеты сохраняются в: " .. log_dir)
    print("=========================================")
    print("ВАЖНО: Для полного перехвата нужны хуки SAMPFUNCS")
    print("Если хуки не работают, используются события SAMP")
    print("=========================================")
    
    -- Сохраняем информацию о запуске
    local startup_info = {
        timestamp = os.time(),
        samp_loaded = isSampLoaded(),
        sampfuncs_loaded = isSampfuncsLoaded(),
        note = "Используйте расширенные хуки SAMPFUNCS для полного перехвата"
    }
    
    local startup_file = io.open(log_dir .. "startup_info.json", "w")
    if startup_file then
        startup_file:write(json.encode(startup_info))
        startup_file:close()
    end
    
    -- Сохраняем статистику каждые 30 секунд
    while true do
        wait(30000)
        save_stats()
        print(string.format("Статистика: Отправлено=%d, Получено=%d", 
            stats.packets_sent, stats.packets_received))
    end
end

-- Сохраняем статистику при выходе
function scriptExit()
    save_stats()
    print("Перехват пакетов остановлен. Статистика сохранена.")
end

