-- Автономный бот для плавания на лодке в GTA SAMP
-- Полностью на Lua, без Python
-- Требует: MoonLoader, SAMPFUNCS
-- Устанавливается в: moonloader/boat_bot_standalone.lua

script_name("Boat Bot Standalone")
script_author("Auto")
script_description("Автономный бот для плавания на лодке - полностью на Lua")

-- Настройка кодировки для русского текста
local encoding = require 'encoding'
encoding.default = 'CP1251'

-- Функция для правильного отображения русского текста в чате
local function msg(text)
    -- Конвертируем UTF-8 в CP1251 для правильного отображения в SAMP
    local text_cp1251 = encoding.utf8_to_cp1251(text)
    sampAddChatMessage(text_cp1251, -1)
end

-- SAMPFUNCS должен быть загружен автоматически через MoonLoader
-- Если нет - скрипт проверит это в main()

-- Константы для типов чекпоинтов (по цвету)
local CHECKPOINT_TYPE_NONE = 0
local CHECKPOINT_TYPE_RED = 1
local CHECKPOINT_TYPE_YELLOW = 2
local CHECKPOINT_TYPE_PINK = 3
local CHECKPOINT_TYPE_GREEN = 4
local CHECKPOINT_TYPE_WHITE = 5
local CHECKPOINT_TYPE_ORANGE = 6
local CHECKPOINT_TYPE_PURPLE = 7

-- Параметры управления
local TURN_THRESHOLD = 3.0  -- Градусы для начала поворота
local TURN_THRESHOLD_CLOSE = 1.5  -- Порог когда близко к цели
local MIN_DISTANCE = 5.0  -- Метры для засчитывания чекпоинта
local CLOSE_DISTANCE_THRESHOLD = 10.0  -- Близкое расстояние
local CHECKPOINT_COOLDOWN = 1.5  -- Секунды между чекпоинтами

-- Система состояний
local state = 'Y1'  -- Начальное состояние

-- Система подсчета чекпоинтов (костыль для бага)
-- Из-за бага один физический чекпоинт засчитывается 3 раза
local checkpoint_counter = {
    internal = 0,  -- Внутренний счетчик (каждый вызов)
    external = 0   -- Внешний счетчик (каждые 3 внутренних = 1 внешний)
}

function checkpoint_counter:add()
    self.internal = self.internal + 1
    -- Внешний счетчик = целая часть от деления внутреннего на 3
    self.external = math.floor(self.internal / 3)
    return self.internal, self.external
end

function checkpoint_counter:reset()
    self.internal = 0
    self.external = 0
end

function checkpoint_counter:get_internal()
    return self.internal
end

function checkpoint_counter:get_external()
    return self.external
end

function checkpoint_counter:check_threshold_external(threshold)
    return self.external >= threshold
end

-- Переменные состояния
local bot_enabled = false
local last_checkpoint_id = -1
local last_checkpoint_time = 0
local last_checkpoint_center = nil
local distance_history = {}
local target_reached_flag = false
local red_squares_collected = 0
local green_after_7_transition_time = 0
local green_square_reached_time = 0
local last_collected_square_center = nil
local min_distance_to_target = nil

-- Управление клавишами
local keys_pressed = {
    w = false,
    a = false,
    d = false
}
local current_turn_direction = nil

-- Функция определения типа чекпоинта по цвету
function getCheckpointTypeByColor(color)
    -- RGB цвета в формате 0xRRGGBB
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

-- Функция получения активного чекпоинта нужного типа
function getActiveCheckpoint(checkpoint_type)
    -- Проверяем доступность SAMPFUNCS
    if not isSampfuncsLoaded() then
        return nil, 0.0
    end
    
    -- Пробуем разные методы получения чекпоинтов
    local checkpoint_count = 0
    
    -- Метод 1: Через SAMPFUNCS API
    if sampGetCheckpointCount then
        checkpoint_count = sampGetCheckpointCount()
    end
    
    -- Если чекпоинтов нет, возвращаем nil
    if checkpoint_count == 0 then
        return nil, 0.0
    end
    
    local ped = PLAYER_PED
    if not doesCharExist(ped) then
        return nil, 0.0
    end
    
    local player_x, player_y, player_z = getCharCoordinates(ped)
    
    local nearest_checkpoint = nil
    local min_distance = 999999.0
    
    -- Ищем ближайший чекпоинт нужного типа
    for i = 0, checkpoint_count - 1 do
        local success, cp = pcall(function() return sampGetCheckpointInfo(i) end)
        if success and cp and cp.active then
            -- Пытаемся получить цвет чекпоинта
            local cp_color = 0xFF0000  -- По умолчанию красный
            local cp_type = CHECKPOINT_TYPE_RED  -- По умолчанию красный
            
            -- Метод 1: Прямой цвет
            if cp.color then
                cp_color = cp.color
                cp_type = getCheckpointTypeByColor(cp_color)
            -- Метод 2: RGB компоненты
            elseif cp.r and cp.g and cp.b then
                cp_color = (cp.r * 65536) + (cp.g * 256) + cp.b
                cp_type = getCheckpointTypeByColor(cp_color)
            -- Метод 3: Если цвет недоступен, используем альтернативный метод
            -- (можно добавить чтение из памяти или другие методы)
            end
            
            -- Если нужен конкретный тип, проверяем
            if checkpoint_type == nil or cp_type == checkpoint_type then
                local dx = cp.x - player_x
                local dy = cp.y - player_y
                local dz = cp.z - player_z
                local distance = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                if distance < min_distance then
                    min_distance = distance
                    nearest_checkpoint = {
                        x = cp.x,
                        y = cp.y,
                        z = cp.z,
                        color = cp_color,
                        type = cp_type,
                        id = cp.id or i,
                        distance = distance
                    }
                end
            end
        end
    end
    
    if nearest_checkpoint then
        return nearest_checkpoint, min_distance
    end
    
    return nil, 0.0
end

-- Функция получения текущей цели в зависимости от состояния
function getCurrentTarget()
    local target_type = nil
    
    -- Определяем какой тип чекпоинта нужен для текущего состояния
    if state == 'Y1' or state == 'Y_AFTER_RED' or state == 'Y_FINAL' then
        target_type = CHECKPOINT_TYPE_YELLOW
    elseif state == 'P1' or state == 'P2' or state == 'P_AFTER_Y' or state == 'P_FINAL' then
        target_type = CHECKPOINT_TYPE_PINK
    elseif state == 'G1' or state == 'GREEN_AFTER_7' or state == 'GREEN_AFTER_10' then
        target_type = CHECKPOINT_TYPE_GREEN
    elseif state == 'W1' or state == 'W_AFTER_O10' then
        target_type = CHECKPOINT_TYPE_WHITE
    elseif state == 'O_BEFORE_FIRST' or state == 'O_AFTER_10' or state == 'O1' or state == 'O2' then
        target_type = CHECKPOINT_TYPE_ORANGE
    elseif state == 'PURPLE_FINAL' then
        target_type = CHECKPOINT_TYPE_PURPLE
    elseif state == 'RED_UNTIL_WHITE' or state == 'RED_1_7' or state == 'RED_8' or 
           state == 'RED_9_10' or state == 'RED_AFTER_GREEN7' or state == 'RED_UNTIL_PURPLE' or 
           state == 'RED_FINAL' then
        target_type = CHECKPOINT_TYPE_RED
    end
    
    if target_type == nil then
        return nil
    end
    
    local checkpoint, distance = getActiveCheckpoint(target_type)
    if checkpoint then
        return {
            found = true,
            x = checkpoint.x,
            y = checkpoint.y,
            z = checkpoint.z,
            type = checkpoint.type,
            id = checkpoint.id,
            distance = distance
        }
    end
    
    return nil
end

-- Функция вычисления угла к цели
function calculateAngleToTarget(player_x, player_y, player_angle, target_x, target_y)
    local dx = target_x - player_x
    local dy = target_y - player_y
    
    -- Угол к цели в радианах
    local target_angle_rad = math.atan2(dy, dx)
    local target_angle = target_angle_rad * 180.0 / math.pi  -- Конвертируем радианы в градусы
    
    -- Нормализуем углы в диапазон 0-360
    target_angle = (target_angle + 360) % 360
    player_angle = (player_angle + 360) % 360
    
    -- Разница углов
    local angle_diff = target_angle - player_angle
    
    -- Нормализуем в диапазон -180 до 180
    if angle_diff > 180 then
        angle_diff = angle_diff - 360
    elseif angle_diff < -180 then
        angle_diff = angle_diff + 360
    end
    
    return angle_diff
end

-- Функция проверки достижения цели
function checkTargetReached(target, distance)
    if not target or not target.found then
        return false
    end
    
    -- Добавляем расстояние в историю
    table.insert(distance_history, distance)
    if #distance_history > 5 then
        table.remove(distance_history, 1)
    end
    
    -- Для красных чекпоинтов - более строгий порог
    local effective_threshold = MIN_DISTANCE
    if target.type == CHECKPOINT_TYPE_RED then
        effective_threshold = 5.0  -- Метры
    elseif target.type == CHECKPOINT_TYPE_YELLOW or target.type == CHECKPOINT_TYPE_PINK or 
           target.type == CHECKPOINT_TYPE_WHITE or target.type == CHECKPOINT_TYPE_ORANGE or 
           target.type == CHECKPOINT_TYPE_GREEN then
        effective_threshold = 8.0  -- Метры
    end
    
    -- Если расстояние меньше порога - считаем что достигли
    if distance < effective_threshold then
        return true
    end
    
    -- Проверяем паттерн: расстояние уменьшалось, потом начало увеличиваться
    if #distance_history >= 3 then
        local min_dist = distance_history[1]
        for i = 2, #distance_history do
            if distance_history[i] < min_dist then
                min_dist = distance_history[i]
            end
        end
        
        if min_dist < effective_threshold then
            local recent = {}
            for i = math.max(1, #distance_history - 2), #distance_history do
                table.insert(recent, distance_history[i])
            end
            if #recent >= 3 and recent[1] < recent[2] and recent[2] < recent[3] then
                return true  -- Расстояние увеличивается после минимума
            end
        end
    end
    
    return false
end

-- Функция обновления состояния
function updateState(target, distance)
    if not target or not target.found then
        return
    end
    
    local target_reached = checkTargetReached(target, distance)
    
    -- Для красных чекпоинтов - альтернативная проверка
    if target.type == CHECKPOINT_TYPE_RED and not target_reached then
        if state == 'RED_1_7' or state == 'RED_9_10' or state == 'RED_AFTER_GREEN7' or 
           state == 'RED_UNTIL_WHITE' or state == 'RED_UNTIL_PURPLE' or state == 'RED_FINAL' then
            local min_dist = distance
            for i = 1, #distance_history do
                if distance_history[i] < min_dist then
                    min_dist = distance_history[i]
                end
            end
            if min_dist < 5.0 then  -- Метры
                target_reached = true
            end
        end
    end
    
    if not target_reached then
        return
    end
    
    -- Защита от повторного засчитывания для красных чекпоинтов
    if target.type == CHECKPOINT_TYPE_RED then
        if target_reached_flag then
            return
        end
        
        local current_time = os.clock()
        local time_since_last = current_time - last_checkpoint_time
        
        if time_since_last < CHECKPOINT_COOLDOWN then
            return
        end
        
        target_reached_flag = true
        last_checkpoint_time = current_time
    else
        if target_reached_flag then
            return
        end
        target_reached_flag = true
    end
    
    -- Функция сброса для нового состояния
    local function resetForNewState()
        min_distance_to_target = nil
        distance_history = {}
        target_reached_flag = false
        if state ~= 'RED_1_7' and state ~= 'RED_8' and state ~= 'RED_9_10' and 
           state ~= 'RED_AFTER_GREEN7' and state ~= 'RED_UNTIL_WHITE' and 
           state ~= 'RED_UNTIL_PURPLE' and state ~= 'RED_FINAL' then
            last_checkpoint_center = nil
        end
    end
    
    -- ---- Блок 1: стартовая последовательность ----
    if state == 'Y1' and target.type == CHECKPOINT_TYPE_YELLOW then
        msg("{00FF00}[Boat Bot] Достигнут первый желтый квадрат -> перехожу к первому розовому.")
        state = 'P1'
        resetForNewState()
        wait(1000)
        return
    end
    
    if state == 'P1' and target.type == CHECKPOINT_TYPE_PINK then
        msg("{00FF00}[Boat Bot] Достигнут первый розовый квадрат -> перехожу к первому зеленому.")
        state = 'G1'
        resetForNewState()
        wait(1000)
        return
    end
    
    if state == 'G1' and target.type == CHECKPOINT_TYPE_GREEN then
        msg("{00FF00}[Boat Bot] Достигнут первый зеленый квадрат -> плыву к красным чекпоинтам.")
        checkpoint_counter:reset()
        state = 'RED_UNTIL_WHITE'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- ---- Красные чекпоинты до появления белого ----
    if state == 'RED_UNTIL_WHITE' and target.type == CHECKPOINT_TYPE_RED then
        local internal, external = checkpoint_counter:add()
        red_squares_collected = external
        msg(string.format("{00FF00}[Boat Bot] ✓ Чекпоинт (internal: %d, external: %d, distance: %.2fм)", 
            internal, external, distance))
        last_collected_square_center = {x = target.x, y = target.y, z = target.z}
        last_checkpoint_center = {x = target.x, y = target.y, z = target.z}
        target_reached_flag = false
        return
    end
    
    -- Белый квадрат после красных
    if state == 'W1' and target.type == CHECKPOINT_TYPE_WHITE then
        msg("{00FF00}[Boat Bot] Достигнут белый квадрат -> перехожу ко второму розовому.")
        state = 'P2'
        resetForNewState()
        return
    end
    
    if state == 'P2' and target.type == CHECKPOINT_TYPE_PINK then
        msg("{00FF00}[Boat Bot] Достигнут второй розовый квадрат -> перехожу к оранжевому.")
        state = 'O_BEFORE_FIRST'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- Оранжевый перед первым чекпоинтом
    if state == 'O_BEFORE_FIRST' and target.type == CHECKPOINT_TYPE_ORANGE then
        msg("{00FF00}[Boat Bot] Достигнут оранжевый квадрат -> начинаю собирать красные чекпоинты 1-7.")
        checkpoint_counter:reset()
        red_squares_collected = 0
        last_checkpoint_time = 0
        state = 'RED_1_7'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- ---- Блок 2: красные чекпоинты 1–7 ----
    if state == 'RED_1_7' and target.type == CHECKPOINT_TYPE_RED then
        local internal, external = checkpoint_counter:add()
        red_squares_collected = external
        msg(string.format("{00FF00}[Boat Bot] ✓ Чекпоинт (internal: %d, external: %d, distance: %.2fм)", 
            internal, external, distance))
        last_collected_square_center = {x = target.x, y = target.y, z = target.z}
        last_checkpoint_center = {x = target.x, y = target.y, z = target.z}
        
        if checkpoint_counter:check_threshold_external(7) then
            msg(string.format("{00FF00}[Boat Bot] Собрано %d физических чекпоинтов -> плыву к зеленому квадрату.", 
                external))
            state = 'GREEN_AFTER_7'
            green_after_7_transition_time = os.clock()
            resetForNewState()
            wait(1000)
        else
            target_reached_flag = false
        end
        return
    end
    
    -- Зеленый после 7 чекпоинтов
    if state == 'GREEN_AFTER_7' and target.type == CHECKPOINT_TYPE_GREEN then
        msg("{00FF00}[Boat Bot] Достигнут зеленый квадрат после 7 чекпоинтов -> плыву к 8-му чекпоинту.")
        green_square_reached_time = os.clock()
        state = 'RED_8'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- 8-й красный чекпоинт
    if state == 'RED_8' and target.type == CHECKPOINT_TYPE_RED then
        local internal, external = checkpoint_counter:add()
        red_squares_collected = external
        msg(string.format("{00FF00}[Boat Bot] ✓ 8-й чекпоинт (internal: %d, external: %d, distance: %.2fм)", 
            internal, external, distance))
        last_collected_square_center = {x = target.x, y = target.y, z = target.z}
        last_checkpoint_center = {x = target.x, y = target.y, z = target.z}
        
        msg("{00FF00}[Boat Bot] Достигнут 8-й красный чекпоинт -> плыву к желтому квадрату.")
        state = 'Y_AFTER_RED'
        green_after_7_transition_time = 0
        green_square_reached_time = 0
        resetForNewState()
        wait(1000)
        return
    end
    
    -- Желтый после красного
    if state == 'Y_AFTER_RED' and target.type == CHECKPOINT_TYPE_YELLOW then
        msg("{00FF00}[Boat Bot] Достигнут желтый квадрат -> плыву к розовому квадрату.")
        state = 'P_AFTER_Y'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- Розовый после желтого
    if state == 'P_AFTER_Y' and target.type == CHECKPOINT_TYPE_PINK then
        msg("{00FF00}[Boat Bot] Достигнут розовый квадрат -> собираю 9-й и 10-й красные чекпоинты.")
        state = 'RED_9_10'
        resetForNewState()
        wait(1000)
        return
    end
    
    -- ---- Блок 3: красные чекпоинты 9–10 ----
    if state == 'RED_9_10' and target.type == CHECKPOINT_TYPE_RED then
        local internal, external = checkpoint_counter:add()
        red_squares_collected = external
        msg(string.format("{00FF00}[Boat Bot] ✓ Чекпоинт (internal: %d, external: %d, distance: %.2fм)", 
            internal, external, distance))
        last_collected_square_center = {x = target.x, y = target.y, z = target.z}
        last_checkpoint_center = {x = target.x, y = target.y, z = target.z}
        
        if checkpoint_counter:check_threshold_external(10) then
            msg(string.format("{00FF00}[Boat Bot] Собрано %d физических чекпоинтов -> жду 2 секунды с W без поворотов.", 
                external))
            
            -- Отпускаем повороты
            setGameKeyState(3, 0)  -- KEY_LEFT
            setGameKeyState(4, 0)  -- KEY_RIGHT
            keys_pressed.a = false
            keys_pressed.d = false
            current_turn_direction = nil
            
            -- Держим W
            setGameKeyState(0, 255)  -- KEY_UP
            keys_pressed.w = true
            
            -- Ждем 2 секунды
            wait(2000)
            
            msg("{00FF00}[Boat Bot] Задержка завершена, перехожу к зеленому квадрату.")
            state = 'GREEN_AFTER_10'
            resetForNewState()
        else
            target_reached_flag = false
        end
        return
    end
    
    -- Зеленый после 10-го красного
    if state == 'GREEN_AFTER_10' and target.type == CHECKPOINT_TYPE_GREEN then
        msg("{00FF00}[Boat Bot] Достигнут зеленый квадрат после 10-го чекпоинта -> плыву к красным чекпоинтам.")
        state = 'RED_UNTIL_PURPLE'
        resetForNewState()
        return
    end
    
    -- Красные до появления фиолетового
    if state == 'RED_UNTIL_PURPLE' and target.type == CHECKPOINT_TYPE_RED then
        local internal, external = checkpoint_counter:add()
        red_squares_collected = external
        msg(string.format("{00FF00}[Boat Bot] ✓ Чекпоинт (internal: %d, external: %d, distance: %.2fм)", 
            internal, external, distance))
        last_collected_square_center = {x = target.x, y = target.y, z = target.z}
        last_checkpoint_center = {x = target.x, y = target.y, z = target.z}
        target_reached_flag = false
        return
    end
    
    -- ---- Финальный блок ----
    if state == 'PURPLE_FINAL' and target.type == CHECKPOINT_TYPE_PURPLE then
        msg("{00FF00}[Boat Bot] Достигнут финальный фиолетовый квадрат -> плыву к финальному розовому.")
        state = 'P_FINAL'
        resetForNewState()
        return
    end
    
    if state == 'P_FINAL' and target.type == CHECKPOINT_TYPE_PINK then
        msg("{00FF00}[Boat Bot] Достигнут финальный розовый квадрат -> плыву к финальному желтому.")
        state = 'Y_FINAL'
        resetForNewState()
        return
    end
    
    if state == 'Y_FINAL' and target.type == CHECKPOINT_TYPE_YELLOW then
        msg("{00FF00}[Boat Bot] Достигнут финальный желтый квадрат -> плыву к последнему красному чекпоинту.")
        state = 'RED_FINAL'
        resetForNewState()
        return
    end
    
    if state == 'RED_FINAL' and target.type == CHECKPOINT_TYPE_RED then
        msg(string.format("{00FF00}[Boat Bot] Достигнут финальный красный чекпоинт (distance: %.2fм) -> рейс завершен, начинаю новый цикл.", 
            distance))
        
        -- Полный сброс цикла
        state = 'Y1'
        red_squares_collected = 0
        checkpoint_counter:reset()
        last_collected_square_center = nil
        resetForNewState()
        return
    end
end

-- Функция управления лодкой
function controlBoat(angle_diff, distance)
    -- Всегда нажимаем W для движения вперед
    if not keys_pressed.w then
        setGameKeyState(0, 255)  -- KEY_UP
        keys_pressed.w = true
    end
    
    -- Адаптивный порог
    local threshold = TURN_THRESHOLD
    local is_red_checkpoint = (state == 'RED_1_7' or state == 'RED_8' or state == 'RED_9_10' or 
                              state == 'RED_AFTER_GREEN7' or state == 'RED_UNTIL_WHITE' or 
                              state == 'RED_UNTIL_PURPLE' or state == 'RED_FINAL')
    
    if distance then
        if is_red_checkpoint then
            threshold = 0.1  -- Максимальная точность для красных
        elseif distance < CLOSE_DISTANCE_THRESHOLD then
            threshold = TURN_THRESHOLD_CLOSE
        end
    end
    
    local abs_angle_diff = math.abs(angle_diff)
    
    if abs_angle_diff > threshold then
        if angle_diff > 0 then
            -- Поворот вправо (D)
            if current_turn_direction ~= 'right' then
                if keys_pressed.a then
                    setGameKeyState(3, 0)  -- KEY_LEFT
                    keys_pressed.a = false
                end
                setGameKeyState(4, 255)  -- KEY_RIGHT
                keys_pressed.d = true
                current_turn_direction = 'right'
            end
        else
            -- Поворот влево (A)
            if current_turn_direction ~= 'left' then
                if keys_pressed.d then
                    setGameKeyState(4, 0)  -- KEY_RIGHT
                    keys_pressed.d = false
                end
                setGameKeyState(3, 255)  -- KEY_LEFT
                keys_pressed.a = true
                current_turn_direction = 'left'
            end
        end
    else
        -- Угол недостаточен - двигаемся прямо
        if current_turn_direction then
            if keys_pressed.a then
                setGameKeyState(3, 0)  -- KEY_LEFT
                keys_pressed.a = false
            end
            if keys_pressed.d then
                setGameKeyState(4, 0)  -- KEY_RIGHT
                keys_pressed.d = false
            end
            current_turn_direction = nil
        end
    end
end

-- Функция остановки лодки
function stopBoat(release_w)
    if release_w and keys_pressed.w then
        setGameKeyState(0, 0)  -- KEY_UP
        keys_pressed.w = false
    end
    if keys_pressed.a then
        setGameKeyState(3, 0)  -- KEY_LEFT
        keys_pressed.a = false
    end
    if keys_pressed.d then
        setGameKeyState(4, 0)  -- KEY_RIGHT
        keys_pressed.d = false
    end
    current_turn_direction = nil
end

-- Основной цикл
function main()
    -- Ждем загрузки SAMP
    while not isSampAvailable() do
        wait(100)
    end
    
    -- Проверяем SAMPFUNCS
    if not isSampfuncsLoaded() then
        msg("{FF0000}[Boat Bot] SAMPFUNCS не загружен! Бот не будет работать.")
        msg("{FFFF00}[Boat Bot] Установите SAMPFUNCS для работы бота.")
        wait(-1)
        return
    end
    
    -- Проверяем доступность функций чекпоинтов
    if not sampGetCheckpointCount then
        msg("{FF0000}[Boat Bot] Функции чекпоинтов недоступны! Обновите SAMPFUNCS.")
        wait(-1)
        return
    end
    
    -- Регистрируем команды
    sampRegisterChatCommand("pirs", cmd_pirs)
    
    msg("{00FF00}[Boat Bot] Скрипт загружен")
    msg("{FFFF00}[Boat Bot] Команды: /pirs on - включить, /pirs off - выключить")
    msg("{FFFF00}[Boat Bot] Альтернатива: Insert - включить/выключить")
    msg("{FFFF00}[Boat Bot] Состояние: " .. state)
    msg("{FFFF00}[Boat Bot] SAMPFUNCS загружен, функции чекпоинтов доступны.")
    
    local last_log_time = 0
    
    while true do
        wait(0)
        
        if not bot_enabled then
            stopBoat(true)
            wait(100)
            goto continue
        end
        
        local ped = PLAYER_PED
        if not doesCharExist(ped) then
            wait(100)
            goto continue
        end
        
        -- Получаем позицию игрока
        local player_x, player_y, player_z = getCharCoordinates(ped)
        local player_angle = getCharHeading(ped)
        
        -- Проверяем специальные условия (белый/фиолетовый)
        if state == 'RED_UNTIL_WHITE' then
            local white_checkpoint = getActiveCheckpoint(CHECKPOINT_TYPE_WHITE)
            if white_checkpoint then
                msg("{00FF00}[Boat Bot] Обнаружен белый квадрат -> переключаюсь на W1.")
                state = 'W1'
                distance_history = {}
                target_reached_flag = false
            end
        end
        
        if state == 'RED_UNTIL_PURPLE' then
            local purple_checkpoint = getActiveCheckpoint(CHECKPOINT_TYPE_PURPLE)
            if purple_checkpoint then
                msg("{00FF00}[Boat Bot] Обнаружен фиолетовый квадрат -> переключаюсь на PURPLE_FINAL.")
                state = 'PURPLE_FINAL'
                distance_history = {}
                target_reached_flag = false
            end
        end
        
        -- Автоматическое увеличение счетчика до 8 через 5 секунд после достижения зеленого
        if green_square_reached_time > 0 and checkpoint_counter:get_external() == 7 then
            local current_time = os.clock()
            local time_since_green = current_time - green_square_reached_time
            if time_since_green >= 5.0 then
                msg("{FFFF00}[Boat Bot] Автоматическое увеличение счетчика до 8 (костыль для бага)")
                for i = 1, 3 do
                    checkpoint_counter:add()
                end
                green_square_reached_time = 0
            end
        end
        
        -- Получаем текущую цель
        local target = getCurrentTarget()
        
        if not target then
            -- Цель не найдена - продолжаем движение вперед
            if keys_pressed.w then
                controlBoat(0, nil)
            else
                setGameKeyState(0, 255)
                keys_pressed.w = true
            end
            wait(16)  -- ~60 FPS
            goto continue
        end
        
        -- Вычисляем угол к цели
        local angle_diff = calculateAngleToTarget(player_x, player_y, player_angle, target.x, target.y)
        
        -- Отслеживаем минимальное расстояние
        if min_distance_to_target == nil or target.distance < min_distance_to_target then
            min_distance_to_target = target.distance
        end
        
        -- Обновляем состояние
        updateState(target, target.distance)
        
        -- Управляем лодкой
        controlBoat(angle_diff, target.distance)
        
        -- Логирование (периодически)
        local current_time = os.clock()
        if current_time - last_log_time >= 0.5 then
            local action = "Прямо"
            if math.abs(angle_diff) > TURN_THRESHOLD then
                action = angle_diff > 0 and "Вправо (D)" or "Влево (A)"
            end
            
            local target_name = "unknown"
            if target.type == CHECKPOINT_TYPE_RED then target_name = "red"
            elseif target.type == CHECKPOINT_TYPE_YELLOW then target_name = "yellow"
            elseif target.type == CHECKPOINT_TYPE_PINK then target_name = "pink"
            elseif target.type == CHECKPOINT_TYPE_GREEN then target_name = "green"
            elseif target.type == CHECKPOINT_TYPE_WHITE then target_name = "white"
            elseif target.type == CHECKPOINT_TYPE_ORANGE then target_name = "orange"
            elseif target.type == CHECKPOINT_TYPE_PURPLE then target_name = "purple"
            end
            
            local internal = checkpoint_counter:get_internal()
            local external = checkpoint_counter:get_external()
            
            msg(string.format("{FFFF00}[Boat Bot] State: %s | Target: %s | Angle: %.1f° | Distance: %.2fм | %s | CP: %d/%d", 
                state, target_name, angle_diff, target.distance, action, external, internal))
            last_log_time = current_time
        end
        
        ::continue::
    end
end

-- Команды для управления ботом
function cmd_pirs_on()
    if bot_enabled then
        msg("{FFFF00}[Boat Bot] Бот уже включен")
    else
        bot_enabled = true
        msg("{00FF00}[Boat Bot] Бот включен")
    end
end

function cmd_pirs_off()
    if not bot_enabled then
        msg("{FFFF00}[Boat Bot] Бот уже выключен")
    else
        bot_enabled = false
        msg("{FF0000}[Boat Bot] Бот выключен")
        stopBoat(true)
    end
end

function cmd_pirs(arg)
    -- Обработка команд /pirs on и /pirs off
    if arg == nil or arg == "" then
        -- Показываем статус
        if bot_enabled then
            msg("{00FF00}[Boat Bot] Бот включен. Используйте /pirs off для выключения")
        else
            msg("{FF0000}[Boat Bot] Бот выключен. Используйте /pirs on для включения")
        end
    elseif arg:lower() == "on" then
        cmd_pirs_on()
    elseif arg:lower() == "off" then
        cmd_pirs_off()
    else
        msg("{FFFF00}[Boat Bot] Использование: /pirs [on|off]")
        msg("{FFFF00}[Boat Bot] Примеры: /pirs on, /pirs off")
    end
end

-- Обработка нажатия Insert для паузы (альтернативный способ)
function onScriptKey(key)
    if key == VK_INSERT then
        bot_enabled = not bot_enabled
        if bot_enabled then
            msg("{00FF00}[Boat Bot] Бот включен (Insert)")
        else
            msg("{FF0000}[Boat Bot] Бот выключен (Insert)")
            stopBoat(true)
        end
    end
end

-- Инициализация
function onScriptLoad()
    msg("{00FF00}[Boat Bot] Автономный бот загружен (полностью на Lua)")
    msg("{FFFF00}[Boat Bot] Команды: /pirs on - включить, /pirs off - выключить")
    msg("{FFFF00}[Boat Bot] Альтернатива: Insert - включить/выключить")
end

function onScriptExit()
    stopBoat(true)
    msg("{FF0000}[Boat Bot] Скрипт выгружен")
end

