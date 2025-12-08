-- MoonLoader скрипт для бота плавания на лодке
-- Устанавливается в: GTA San Andreas/moonloader/boat_bot_ml.lua
-- Требует: MoonLoader, SAMPFUNCS

local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

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

-- Путь к файлам обмена данными
-- getWorkingDirectory() возвращает путь к папке moonloader
-- Нужно подняться на уровень выше (к корню игры)
local moonloader_dir = getWorkingDirectory()
local game_dir = string.match(moonloader_dir, "(.+)\\[^\\]+$") or moonloader_dir  -- Убираем последнюю папку
-- Альтернатива: используем абсолютный путь к папке Python бота
-- Или сохраняем в корень игры (где gta_sa.exe)
local DATA_FILE = game_dir .. "\\bot_shared_data.txt"
local COMMAND_FILE = game_dir .. "\\bot_commands.txt"

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

-- Для отладки: выводим пути в консоль
function printPaths()
    safeChatMessage("{FFFF00}[Boat Bot] MoonLoader dir: " .. moonloader_dir, -1)
    safeChatMessage("{FFFF00}[Boat Bot] Game dir: " .. game_dir, -1)
    safeChatMessage("{FFFF00}[Boat Bot] Data file: " .. DATA_FILE, -1)
    safeChatMessage("{FFFF00}[Boat Bot] Command file: " .. COMMAND_FILE, -1)
end

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

-- История чекпоинтов для отслеживания
local checkpoint_history = {}
local last_checkpoint_id = -1

-- Функция получения цвета чекпоинта (через SAMPFUNCS)
function getCheckpointColor(checkpoint)
    -- В SAMPFUNCS можно получить цвет чекпоинта
    -- Если API недоступен, используем альтернативный метод
    if checkpoint.color then
        return checkpoint.color
    end
    -- Альтернатива: определяем по типу чекпоинта
    return 0xFF0000  -- По умолчанию красный
end

-- Функция определения типа чекпоинта по цвету
function getCheckpointTypeByColor(color)
    -- RGB цвета чекпоинтов
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
    -- Метод 1: Через SAMPFUNCS API (если доступен)
    if sampGetCheckpointCount then
        local checkpoint_count = sampGetCheckpointCount()
        
        if checkpoint_count == 0 then
            return nil, 0.0
        end
        
        -- Получаем позицию игрока
        local ped = PLAYER_PED
        local player_x, player_y, player_z = getCharCoordinates(ped)
        
        local nearest_checkpoint = nil
        local min_distance = 999999.0
        
        -- Ищем ближайший активный чекпоинт
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
    
    -- Метод 2: Через игровые функции (альтернатива)
    -- Используем функции игры для получения чекпоинтов
    -- Это может потребовать дополнительных исследований памяти
    
    return nil, 0.0
end

-- Функция получения всех видимых чекпоинтов (для выбора нужного)
function getAllVisibleCheckpoints()
    local checkpoints = {}
    
    if sampGetCheckpointCount then
        local checkpoint_count = sampGetCheckpointCount()
        local ped = PLAYER_PED
        local player_x, player_y, player_z = getCharCoordinates(ped)
        
        for i = 0, checkpoint_count - 1 do
            local cp = sampGetCheckpointInfo(i)
            if cp and cp.active then
                local dx = cp.x - player_x
                local dy = cp.y - player_y
                local dz = cp.z - player_z
                local distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                table.insert(checkpoints, {
                    x = cp.x,
                    y = cp.y,
                    z = cp.z,
                    color = getCheckpointColor(cp),
                    type = getCheckpointTypeByColor(getCheckpointColor(cp)),
                    distance = distance,
                    id = cp.id or i
                })
            end
        end
    end
    
    -- Сортируем по расстоянию
    table.sort(checkpoints, function(a, b) return a.distance < b.distance end)
    
    return checkpoints
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
function processBotCommand()
    if not game_data.bot_enabled then
        return
    end
    
    if game_data.bot_command == COMMAND_FORWARD then
        -- Вперед (W)
        setGameKeyState(0, 255)  -- KEY_UP
        -- Отпускаем повороты
        setGameKeyState(3, 0)  -- KEY_LEFT
        setGameKeyState(4, 0)  -- KEY_RIGHT
    elseif game_data.bot_command == COMMAND_LEFT then
        -- Влево (A) + вперед
        setGameKeyState(0, 255)  -- KEY_UP
        setGameKeyState(3, 255)  -- KEY_LEFT
        setGameKeyState(4, 0)    -- KEY_RIGHT
    elseif game_data.bot_command == COMMAND_RIGHT then
        -- Вправо (D) + вперед
        setGameKeyState(0, 255)  -- KEY_UP
        setGameKeyState(3, 0)    -- KEY_LEFT
        setGameKeyState(4, 255)  -- KEY_RIGHT
    elseif game_data.bot_command == COMMAND_NONE then
        -- Остановка
        setGameKeyState(0, 0)  -- KEY_UP
        setGameKeyState(3, 0)  -- KEY_LEFT
        setGameKeyState(4, 0)  -- KEY_RIGHT
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
                safeChatMessage("{00FF00}[Boat Bot] Скрипт загружен. Используйте Insert для паузы.", -1)
                safeChatMessage("{00FF00}[Boat Bot] Убедитесь, что Python бот запущен!", -1)
                -- Выводим пути для отладки
                printPaths()
            end
        end
        
        -- Загружаем команды от Python бота
        loadBotCommands()
        
        if game_data.bot_enabled then
            -- Получаем позицию игрока
            local ped = PLAYER_PED
            if doesCharExist(ped) then
                local x, y, z = getCharCoordinates(ped)
                local heading = getCharHeading(ped)
                
                game_data.player_x = x
                game_data.player_y = y
                game_data.player_z = z
                game_data.player_angle = heading
                
                -- Получаем активный чекпоинт
                local checkpoint, distance = getActiveCheckpoint()
                
                if checkpoint then
                    game_data.checkpoint_x = checkpoint.x
                    game_data.checkpoint_y = checkpoint.y
                    game_data.checkpoint_z = checkpoint.z
                    game_data.checkpoint_distance = distance
                    
                    -- Определяем тип чекпоинта
                    local color = getCheckpointColor(checkpoint)
                    game_data.checkpoint_type = getCheckpointTypeByColor(color)
                    game_data.checkpoint_id = checkpoint.id or 0
                else
                    -- Чекпоинт не найден
                    game_data.checkpoint_x = 0.0
                    game_data.checkpoint_y = 0.0
                    game_data.checkpoint_z = 0.0
                    game_data.checkpoint_type = CHECKPOINT_TYPE_NONE
                    game_data.checkpoint_id = 0
                    game_data.checkpoint_distance = 0.0
                end
                
                -- Обрабатываем команды управления
                processBotCommand()
            end
        else
            -- Бот выключен - останавливаем управление
            setGameKeyState(0, 0)  -- KEY_UP
            setGameKeyState(3, 0)  -- KEY_LEFT
            setGameKeyState(4, 0)  -- KEY_RIGHT
        end
        
        -- Сохраняем данные для Python бота
        saveGameData()
    end
end

-- Обработка нажатия Insert для паузы
function onScriptKey(key)
    if key == VK_INSERT then
        game_data.bot_enabled = not game_data.bot_enabled
        if game_data.bot_enabled then
            safeChatMessage("{00FF00}[Boat Bot] Бот включен", -1)
        else
            safeChatMessage("{FF0000}[Boat Bot] Бот выключен", -1)
            -- Останавливаем управление
            setGameKeyState(0, 0)
            setGameKeyState(3, 0)
            setGameKeyState(4, 0)
        end
    end
end

-- Инициализация
function onScriptLoad()
    script_loaded = true
    init_done = false
    init_wait = 0
end

function onScriptExit()
    -- Останавливаем управление при выходе
    setGameKeyState(0, 0)
    setGameKeyState(3, 0)
    setGameKeyState(4, 0)
    safeChatMessage("{FF0000}[Boat Bot] Скрипт выгружен", -1)
end

