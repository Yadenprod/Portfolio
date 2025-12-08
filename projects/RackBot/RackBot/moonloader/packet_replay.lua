-- ============================================
-- ВОСПРОИЗВЕДЕНИЕ ЗАХВАЧЕННЫХ ПАКЕТОВ
-- ============================================
-- Используйте этот скрипт для воспроизведения
-- захваченных пакетов для тестирования

require "lib.moonloader"
local encoding = require 'encoding'
encoding.default = 'CP1251'

local packets_file = "moonloader/advanced_packet_capture/all_packets.log"
local replay_speed = 1.0  -- Множитель скорости (1.0 = реальное время)

-- Загружаем пакеты из файла
local function load_packets()
    local packets = {}
    local file = io.open(packets_file, "rb")
    
    if not file then
        print("ОШИБКА: Файл с пакетами не найден!")
        return packets
    end
    
    print("Загрузка пакетов...")
    
    while true do
        -- Читаем заголовок пакета
        local direction_byte = file:read(1)
        if not direction_byte then
            break
        end
        
        local direction = (string.byte(direction_byte) == 0x01) and "outgoing" or "incoming"
        local packet_id_byte = file:read(1)
        local packet_id = string.byte(packet_id_byte)
        
        -- Читаем размер (4 байта, big-endian)
        local size_bytes = file:read(4)
        local size = 0
        if size_bytes then
            size = string.byte(size_bytes, 1) * 16777216 +  -- 2^24
                   string.byte(size_bytes, 2) * 65536 +      -- 2^16
                   string.byte(size_bytes, 3) * 256 +       -- 2^8
                   string.byte(size_bytes, 4)
        end
        
        -- Читаем timestamp (8 байт)
        local timestamp_bytes = file:read(8)
        local timestamp = 0
        if timestamp_bytes then
            -- Упрощенное чтение timestamp
            timestamp = string.byte(timestamp_bytes, 1)
        end
        
        -- Читаем данные
        local data = file:read(size)
        
        if data then
            table.insert(packets, {
                direction = direction,
                packet_id = packet_id,
                size = size,
                timestamp = timestamp,
                data = data
            })
        end
    end
    
    file:close()
    print(string.format("Загружено пакетов: %d", #packets))
    return packets
end

-- Воспроизводим пакет
local function replay_packet(packet, index, total)
    print(string.format("[%d/%d] Воспроизведение %s пакета ID=0x%02X (%d байт)",
        index, total,
        packet.direction == "outgoing" and "исходящего" or "входящего",
        packet.packet_id,
        packet.size
    ))
    
    if packet.direction == "outgoing" then
        -- Отправляем пакет
        -- sendPacket(packet.packet_id, packet.data)
        -- Примечание: Требует реализации функции отправки пакетов
    else
        -- Входящие пакеты обычно не воспроизводятся
        print("  (входящий пакет пропущен)")
    end
end

function main()
    wait(2000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("ОШИБКА: SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    print("=========================================")
    print("ВОСПРОИЗВЕДЕНИЕ ПАКЕТОВ")
    print("=========================================")
    
    local packets = load_packets()
    
    if #packets == 0 then
        print("Нет пакетов для воспроизведения!")
        return
    end
    
    print(string.format("Начинаю воспроизведение %d пакетов...", #packets))
    print("Нажмите любую клавишу для остановки")
    
    -- Фильтруем только исходящие пакеты для воспроизведения
    local outgoing_packets = {}
    for _, packet in ipairs(packets) do
        if packet.direction == "outgoing" then
            table.insert(outgoing_packets, packet)
        end
    end
    
    print(string.format("Исходящих пакетов для воспроизведения: %d", #outgoing_packets))
    
    -- Воспроизводим пакеты
    for i, packet in ipairs(outgoing_packets) do
        replay_packet(packet, i, #outgoing_packets)
        
        -- Задержка между пакетами (можно настроить)
        wait(100 * replay_speed)
    end
    
    print("Воспроизведение завершено!")
end

