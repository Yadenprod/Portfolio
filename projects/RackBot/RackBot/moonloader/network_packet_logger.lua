-- ============================================
-- ЛОГГЕР СЕТЕВЫХ ПАКЕТОВ
-- ============================================
-- Перехватывает сетевые пакеты SAMP (если доступно через SAMPFUNCS)

require "lib.moonloader"
local encoding = require 'encoding'
encoding.default = 'CP1251'

local log_dir = "moonloader/packet_logs/"

local function ensure_dir(path)
    os.execute('mkdir "' .. path .. '" 2>nul')
end

ensure_dir(log_dir)

local function hex_dump(data)
    local hex = ""
    for i = 1, math.min(#data, 256) do
        hex = hex .. string.format("%02X ", string.byte(data, i))
        if i % 16 == 0 then
            hex = hex .. "\n"
        end
    end
    return hex
end

print("=========================================")
print("ЛОГГЕР ПАКЕТОВ ЗАПУЩЕН")
print("Логирование сетевых пакетов...")
print("=========================================")

-- Перехват исходящих пакетов (если доступно)
function onSendPacket(packetId, bitStream)
    local packet_data = {
        type = "packet_sent",
        packetId = packetId,
        timestamp = os.time(),
        size = 0  -- Размер пакета если доступно
    }
    
    local file = io.open(log_dir .. "packets_sent.log", "a")
    if file then
        file:write(string.format("[%s] ПАКЕТ ОТПРАВЛЕН: ID=%d\n", 
            os.date("%H:%M:%S"), packetId))
        file:close()
    end
    
    print(string.format(">>> ПАКЕТ ОТПРАВЛЕН: ID=%d", packetId))
end

-- Перехват входящих пакетов (если доступно)
function onReceivePacket(packetId, bitStream)
    local packet_data = {
        type = "packet_received",
        packetId = packetId,
        timestamp = os.time(),
        size = 0
    }
    
    local file = io.open(log_dir .. "packets_received.log", "a")
    if file then
        file:write(string.format("[%s] ПАКЕТ ПОЛУЧЕН: ID=%d\n", 
            os.date("%H:%M:%S"), packetId))
        file:close()
    end
    
    print(string.format("<<< ПАКЕТ ПОЛУЧЕН: ID=%d", packetId))
end

function main()
    wait(2000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("ОШИБКА: SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    print("Логгер пакетов активен")
    print("Примечание: Перехват пакетов зависит от возможностей SAMPFUNCS")
    
    while true do
        wait(1000)
    end
end

