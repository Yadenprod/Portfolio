-- Упрощенная версия MoonLoader скрипта
-- Автоматически определяет путь к корню игры
-- Файлы обмена сохраняются в корне игры (на уровень выше moonloader)
--
-- ЛОГИКА РАБОТЫ (как в Python боте):
-- 1. Скрипт читает данные игры (позиция игрока, чекпоинты) и сохраняет в bot_shared_data.txt
-- 2. Python бот читает эти данные, вычисляет направление и отправляет команды в bot_commands.txt
-- 3. Скрипт читает команды и применяет их ТОЛЬКО когда бот включен
-- 4. Когда бот выключен - скрипт НЕ ТРОГАЕТ клавиши, игрок управляет нормально

-- Кодировка не используется - все сообщения на английском для надежности

-- Получаем путь к папке moonloader
local moonloader_dir = getWorkingDirectory()

-- Поднимаемся на уровень выше (к корню игры, где gta_sa.exe)
-- Убираем последнюю папку из пути
local game_dir = string.match(moonloader_dir, "(.+)\\[^\\]+$") or moonloader_dir

-- Сохраняем файлы обмена в корне игры (Python бот ищет их там)
local DATA_FILE = game_dir .. "\\bot_shared_data.txt"
local COMMAND_FILE = game_dir .. "\\bot_commands.txt"

-- Константы для типов чекпоинтов
local CHECKPOINT_TYPE_NONE = 0
local CHECKPOINT_TYPE_RED = 1
local CHECKPOINT_TYPE_YELLOW = 2
local CHECKPOINT_TYPE_PINK = 3
local CHECKPOINT_TYPE_GREEN = 4
local CHECKPOINT_TYPE_WHITE = 5
local CHECKPOINT_TYPE_ORANGE = 6
local CHECKPOINT_TYPE_PURPLE = 7

-- Константы для команд управления
local COMMAND_NONE = 0
local COMMAND_FORWARD = 1  -- W
local COMMAND_LEFT = 2     -- A
local COMMAND_RIGHT = 3    -- D

-- Структура данных для обмена
local game_data = {
    player_x = 0.0,
    player_y = 0.0,
    player_z = 0.0,
    player_angle = 0.0,
    checkpoint_x = 0.0,
    checkpoint_y = 0.0,
    checkpoint_z = 0.0,
    checkpoint_type = CHECKPOINT_TYPE_NONE,
    checkpoint_id = 0,
    checkpoint_distance = 0.0,
    bot_enabled = false,
    bot_command = COMMAND_NONE
}

-- Флаг инициализации
local script_loaded = false
local init_done = false
local init_wait = 0

-- Безопасная отправка сообщения в чат
function safeChatMessage(text, color)
    color = color or -1
    if sampAddChatMessage then
        -- Пытаемся отправить сообщение
        local success, err = pcall(function()
            sampAddChatMessage(text, color)
        end)
        if not success then
            -- Если не удалось отправить в чат, выводим в консоль
            print("[Boat Bot] " .. text)
        end
    else
        -- Если функция недоступна, выводим в консоль
        print("[Boat Bot] " .. text)
    end
end

-- Функция определения типа чекпоинта по цвету
function getCheckpointTypeByColor(color)
    if color == 0xFF0000 or color == 0xC30202 then  -- Красный
        return CHECKPOINT_TYPE_RED
    elseif color == 0xFFFF00 or color == 0xFDED00 then  -- Желтый
        return CHECKPOINT_TYPE_YELLOW
    elseif color == 0xFF00FF or color == 0xFF00FA then  -- Розовый
        return CHECKPOINT_TYPE_PINK
    elseif color == 0x00FF00 or color == 0x0B9A00 then  -- Зеленый
        return CHECKPOINT_TYPE_GREEN
    elseif color == 0xFFFFFF then  -- Белый
        return CHECKPOINT_TYPE_WHITE
    elseif color == 0xFF6800 then  -- Оранжевый
        return CHECKPOINT_TYPE_ORANGE
    elseif color == 0x6A05B8 then  -- Фиолетовый
        return CHECKPOINT_TYPE_PURPLE
    end
    return CHECKPOINT_TYPE_NONE
end

-- Функция получения активного чекпоинта
function getActiveCheckpoint()
    if sampGetCheckpointCount then
        local checkpoint_count = sampGetCheckpointCount()
        
        if checkpoint_count == 0 then
            return nil, 0.0
        end
        
        local ped = PLAYER_PED
        local player_x, player_y, player_z = getCharCoordinates(ped)
        
        local nearest_checkpoint = nil
        local min_distance = 999999.0
        
        for i = 0, checkpoint_count - 1 do
            local cp = sampGetCheckpointInfo(i)
            if cp and cp.active then
                local dx = cp.x - player_x
                local dy = cp.y - player_y
                local dz = cp.z - player_z
                local distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if distance < min_distance then
                    min_distance = distance
                    nearest_checkpoint = cp
                end
            end
        end
        
        if nearest_checkpoint then
            return nearest_checkpoint, min_distance
        end
    end
    
    return nil, 0.0
end

-- Функция сохранения данных в файл
function saveGameData()
    local file = io.open(DATA_FILE, "w")
    if file then
        file:write(string.format("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d,%d,%.6f,%d,%d",
            game_data.player_x,
            game_data.player_y,
            game_data.player_z,
            game_data.player_angle,
            game_data.checkpoint_x,
            game_data.checkpoint_y,
            game_data.checkpoint_z,
            game_data.checkpoint_type,
            game_data.checkpoint_id,
            game_data.checkpoint_distance,
            game_data.bot_enabled and 1 or 0,
            game_data.bot_command
        ))
        file:close()
        return true
    else
        return false
    end
end

-- Функция загрузки команд от Python бота
function loadBotCommands()
    local file = io.open(COMMAND_FILE, "r")
    if file then
        local line = file:read("*line")
        if line then
            local parts = {}
            for part in line:gmatch("[^,]+") do
                table.insert(parts, part)
            end
            if #parts >= 2 then
                game_data.bot_enabled = tonumber(parts[1]) == 1
                game_data.bot_command = tonumber(parts[2])
            end
        end
        file:close()
    end
end

-- Функция обработки команд управления
-- ВАЖНО: Управляем клавишами ТОЛЬКО когда бот включен и есть команда
function processBotCommand()
    -- Если бот выключен - НЕ ТРОГАЕМ клавиши вообще!
    -- Это позволяет игроку управлять персонажем нормально
    if not game_data.bot_enabled then
        return
    end
    
    -- Обрабатываем команды только когда бот включен
    if game_data.bot_command == COMMAND_FORWARD then
        setGameKeyState(0, 255)  -- KEY_UP (W)
        setGameKeyState(2, 0)    -- KEY_LEFT (A)
        setGameKeyState(3, 0)    -- KEY_RIGHT (D)
    elseif game_data.bot_command == COMMAND_LEFT then
        setGameKeyState(0, 255)  -- KEY_UP (W)
        setGameKeyState(2, 255)  -- KEY_LEFT (A)
        setGameKeyState(3, 0)    -- KEY_RIGHT (D)
    elseif game_data.bot_command == COMMAND_RIGHT then
        setGameKeyState(0, 255)  -- KEY_UP (W)
        setGameKeyState(2, 0)    -- KEY_LEFT (A)
        setGameKeyState(3, 255)  -- KEY_RIGHT (D)
    elseif game_data.bot_command == COMMAND_NONE then
        -- Останавливаем все клавиши только если была команда
        setGameKeyState(0, 0)  -- KEY_UP (W)
        setGameKeyState(2, 0)  -- KEY_LEFT (A)
        setGameKeyState(3, 0)  -- KEY_RIGHT (D)
    end
    
    -- Сбрасываем команду после обработки
    game_data.bot_command = COMMAND_NONE
end

-- Основной цикл обновления
function main()
    while true do
        wait(0)
        
        -- Инициализация после загрузки (с задержкой для SAMP)
        if not init_done then
            init_wait = init_wait + 1
            if init_wait >= 100 then  -- Ждем ~1 секунду (100 кадров)
                init_done = true
                safeChatMessage("{00FF00}[Boat Bot] Script loaded (simple version)", -1)
                safeChatMessage("{FFFF00}[Boat Bot] MoonLoader: " .. moonloader_dir, -1)
                safeChatMessage("{FFFF00}[Boat Bot] Game dir: " .. game_dir, -1)
                safeChatMessage("{FFFF00}[Boat Bot] Data file: " .. DATA_FILE, -1)
                safeChatMessage("{00FF00}[Boat Bot] Use Insert for pause or /pirs on/off", -1)
                
                -- Проверка создания файла
                local test_file = io.open(DATA_FILE, "w")
                if test_file then
                    test_file:write("test")
                    test_file:close()
                    safeChatMessage("{00FF00}[Boat Bot] File created successfully!", -1)
                else
                    safeChatMessage("{FF0000}[Boat Bot] ERROR: Failed to create file!", -1)
                    safeChatMessage("{FF0000}[Boat Bot] Check path: " .. DATA_FILE, -1)
                end
            end
        end
        
        loadBotCommands()
        
        if game_data.bot_enabled then
            local ped = PLAYER_PED
            if doesCharExist(ped) then
                local x, y, z = getCharCoordinates(ped)
                local heading = getCharHeading(ped)
                
                game_data.player_x = x
                game_data.player_y = y
                game_data.player_z = z
                game_data.player_angle = heading
                
                local checkpoint, distance = getActiveCheckpoint()
                
                if checkpoint then
                    game_data.checkpoint_x = checkpoint.x
                    game_data.checkpoint_y = checkpoint.y
                    game_data.checkpoint_z = checkpoint.z
                    game_data.checkpoint_distance = distance
                    
                    local color = checkpoint.color or 0xFF0000
                    game_data.checkpoint_type = getCheckpointTypeByColor(color)
                    game_data.checkpoint_id = checkpoint.id or 0
                else
                    game_data.checkpoint_x = 0.0
                    game_data.checkpoint_y = 0.0
                    game_data.checkpoint_z = 0.0
                    game_data.checkpoint_type = CHECKPOINT_TYPE_NONE
                    game_data.checkpoint_id = 0
                    game_data.checkpoint_distance = 0.0
                end
                
                processBotCommand()
            end
        end
        -- ВАЖНО: Когда бот выключен - НЕ ТРОГАЕМ клавиши!
        -- Это позволяет игроку управлять персонажем нормально
        
        saveGameData()
    end
end

-- Обработка нажатия Insert для паузы
function onScriptKey(key)
    if key == VK_INSERT then
        game_data.bot_enabled = not game_data.bot_enabled
        if game_data.bot_enabled then
            safeChatMessage("{00FF00}[Boat Bot] Bot enabled", -1)
        else
            safeChatMessage("{FF0000}[Boat Bot] Bot disabled", -1)
            setGameKeyState(0, 0)  -- KEY_UP (W)
            setGameKeyState(2, 0)  -- KEY_LEFT (A)
            setGameKeyState(3, 0)  -- KEY_RIGHT (D)
        end
    end
end

-- Обработка команды /pirs в чате
function cmd_pirs(arg)
    arg = arg or ""
    arg = string.lower(arg)
    
    if arg == "on" or arg == "" then
        game_data.bot_enabled = true
        safeChatMessage("{00FF00}[Boat Bot] Bot enabled. Use /pirs off to disable", -1)
    elseif arg == "off" then
        game_data.bot_enabled = false
        safeChatMessage("{FF0000}[Boat Bot] Bot disabled. Use /pirs on to enable", -1)
        setGameKeyState(0, 0)  -- KEY_UP (W)
        setGameKeyState(2, 0)  -- KEY_LEFT (A)
        setGameKeyState(3, 0)  -- KEY_RIGHT (D)
    else
        safeChatMessage("{FFFF00}[Boat Bot] Usage: /pirs [on|off]", -1)
        safeChatMessage("{FFFF00}[Boat Bot] Examples: /pirs on, /pirs off", -1)
    end
end

-- Инициализация
function onScriptLoad()
    script_loaded = true
    init_done = false
    init_wait = 0
    
    -- Регистрируем команду /pirs
    if sampRegisterChatCommand then
        sampRegisterChatCommand("pirs", cmd_pirs)
        sampRegisterChatCommand("bot", cmd_pirs)  -- Альтернативная команда
    end
end

function onScriptExit()
    setGameKeyState(0, 0)  -- KEY_UP (W)
    setGameKeyState(2, 0)  -- KEY_LEFT (A)
    setGameKeyState(3, 0)  -- KEY_RIGHT (D)
    safeChatMessage("{FF0000}[Boat Bot] Script unloaded", -1)
end

