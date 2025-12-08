-- МАКСИМАЛЬНО АГРЕССИВНЫЙ перехватчик диалогов для RakSAMP Lite
-- Этот скрипт пытается перехватить ВСЕ возможные диалоги, включая кастомные
-- ВАЖНО: Этот скрипт должен загружаться РАНЬШЕ других скриптов для перехвата RPC

require("addon")
local sampev = require("samp.events")

-- Пароль для авторизации (глобальная переменная)
password = "123456789q"

-- Флаги состояния
local INTERCEPTION_ACTIVE = true
local RPC_LOG_DURATION = 60000 -- Логируем первые 60 секунд
local RPC_LOG_START_TIME = nil
local LAST_DIALOG_ID = nil
local DIALOG_DETECTED = false

-- Счетчик попыток отправки ответа на диалог
local dialogResponseAttempts = {}

-- Функция для безопасной отправки ответа на диалог
local function tryDialogResponse(dialogId, button, list, input)
    if not dialogResponseAttempts[dialogId] then
        dialogResponseAttempts[dialogId] = 0
    end
    
    -- Ограничиваем количество попыток для каждого ID
    if dialogResponseAttempts[dialogId] < 5 then
        dialogResponseAttempts[dialogId] = dialogResponseAttempts[dialogId] + 1
        sendDialogResponse(dialogId, button, list, input)
        print(string.format("[DIALOG INTERCEPTOR] Sent response: ID=%d, button=%d, list=%d, input=%s", 
            dialogId, button, list, input))
        return true
    end
    return false
end

-- Функция для анализа RPC и попытки интерпретировать как диалог
local function analyzeRPCAsDialog(id, bs)
    if not bs or bs == 0 then
        return false
    end
    
    local readOffset = bs:getReadOffset()
    local bitsUsed = bs:getNumberOfBitsUsed()
    local bytesUsed = math.floor(bitsUsed / 8)
    
    -- Пропускаем слишком маленькие или слишком большие RPC
    if bytesUsed < 5 or bytesUsed > 1000 then
        bs:setReadOffset(readOffset)
        return false
    end
    
    -- Пробуем прочитать первые байты
    local firstBytes = {}
    local maxBytes = math.min(10, bytesUsed)
    for i = 1, maxBytes do
        firstBytes[i] = bs:readUInt8()
    end
    bs:setReadOffset(readOffset)
    
    -- Стандартный диалог: dialogId (uint16), style (uint8), titleLen (uint8), title...
    -- Если первые 2 байта выглядят как dialogId (0-65535), а третий как style (0-5)
    local possibleDialogId = firstBytes[1] + (firstBytes[2] * 256) -- little-endian uint16
    local possibleStyle = firstBytes[3]
    
    -- Проверяем, похоже ли это на диалог
    if possibleDialogId < 1000 and possibleStyle <= 5 then
        print(string.format("[DIALOG INTERCEPTOR] RPC %d might be dialog! ID=%d, Style=%d, Bytes=%d", 
            id, possibleDialogId, possibleStyle, bytesUsed))
        print(string.format("[DIALOG INTERCEPTOR] First bytes: %s", table.concat(firstBytes, ", ")))
        
        -- Пробуем отправить ответ на диалог
        tryDialogResponse(possibleDialogId, 1, -1, password)
        LAST_DIALOG_ID = possibleDialogId
        DIALOG_DETECTED = true
        return true
    end
    
    return false
end

-- Основной обработчик RPC - перехватываем ВСЕ RPC
registerHandler("onReceiveRPC", function(id, bs)
    -- Определяем время начала логирования
    if not RPC_LOG_START_TIME then
        RPC_LOG_START_TIME = os.clock() * 1000
        print("=========================================")
        print("[DIALOG INTERCEPTOR] RPC LOGGING STARTED - First 60 seconds")
        print("[DIALOG INTERCEPTOR] Looking for dialog RPCs...")
        print("=========================================")
    end
    
    local timeSinceStart = (os.clock() * 1000) - RPC_LOG_START_TIME
    local shouldLog = timeSinceStart < RPC_LOG_DURATION
    
    -- КРИТИЧЕСКИ ВАЖНО: RPC 61 - стандартный диалог
    -- Перехватываем ДО стандартного обработчика, возвращаем false чтобы предотвратить дальнейшую обработку
    if id == 61 then
        print("=========================================")
        print("[DIALOG INTERCEPTOR] !!! RPC 61 (SHOWDIALOG) RECEIVED !!!")
        print("=========================================")
        
        if bs and bs ~= 0 then
            local readOffset = bs:getReadOffset()
            
            -- Читаем данные диалога
            local dialogId = bs:readUInt16()
            local style = bs:readUInt8()
            
            -- Читаем title
            local titleLen = bs:readUInt8()
            local title = ""
            if titleLen > 0 then
                title = bs:readString(titleLen)
            end
            
            -- Читаем okButton
            local okButtonLen = bs:readUInt8()
            local okButton = ""
            if okButtonLen > 0 then
                okButton = bs:readString(okButtonLen)
            end
            
            -- Читаем cancelButton
            local cancelButtonLen = bs:readUInt8()
            local cancelButton = ""
            if cancelButtonLen > 0 then
                cancelButton = bs:readString(cancelButtonLen)
            end
            
            print(string.format("[DIALOG INTERCEPTOR] Dialog ID: %d, Style: %d", dialogId, style))
            print(string.format("[DIALOG INTERCEPTOR] Title: %s", title))
            print(string.format("[DIALOG INTERCEPTOR] OK Button: %s", okButton))
            print(string.format("[DIALOG INTERCEPTOR] Cancel Button: %s", cancelButton))
            
            -- Автоматически отправляем ответ на диалог
            tryDialogResponse(dialogId, 1, -1, password)
            LAST_DIALOG_ID = dialogId
            DIALOG_DETECTED = true
            
            bs:setReadOffset(readOffset)
            
            -- ВАЖНО: Возвращаем false чтобы предотвратить дальнейшую обработку библиотекой
            -- Это может помочь перехватить диалог до стандартного обработчика
            return false
        end
    -- Анализируем другие подозрительные RPC в первые 60 секунд
    elseif shouldLog and id ~= 72 and id ~= 11 and id ~= 137 and id ~= 138 and id ~= 155 and 
           id ~= 230 and id ~= 225 and id ~= 226 and id ~= 56 and id ~= 44 and id ~= 58 and 
           id ~= 36 and id ~= 166 and id ~= 45 and id ~= 99 and id ~= 93 and id ~= 69 and 
           id ~= 43 and id ~= 128 and id ~= 129 and id ~= 139 and id ~= 50 and id ~= 51 and 
           id ~= 52 and id ~= 134 and id ~= 61 and id ~= 86 then
        -- Пробуем интерпретировать как диалог
        analyzeRPCAsDialog(id, bs)
    end
end)

-- Перехватываем стандартное событие onShowDialog
function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    print("=========================================")
    print("[DIALOG INTERCEPTOR] !!! onShowDialog EVENT !!!")
    print("=========================================")
    print(string.format("[DIALOG INTERCEPTOR] Dialog ID: %d", dialogId))
    print(string.format("[DIALOG INTERCEPTOR] Style: %d", style))
    print(string.format("[DIALOG INTERCEPTOR] Title: %s", title or "(no title)"))
    print(string.format("[DIALOG INTERCEPTOR] Button 1: %s", button1 or "(no button1)"))
    print(string.format("[DIALOG INTERCEPTOR] Button 2: %s", button2 or "(no button2)"))
    print(string.format("[DIALOG INTERCEPTOR] Text: %s", (text and text:sub(1, 100)) or "(no text)"))
    print("=========================================")
    
    -- Автоматически отправляем ответ на диалог
    tryDialogResponse(dialogId, 1, -1, password)
    LAST_DIALOG_ID = dialogId
    DIALOG_DETECTED = true
    
    -- Возвращаем false чтобы предотвратить дальнейшую обработку
    -- Это "потребляет" событие, чтобы другие обработчики не получили его
    return false
end

-- Перехватываем события текстовых элементов (textdraws)
function sampev.onShowTextDraw(textdrawId, textdraw)
    if textdraw and textdraw.text then
        local text = textdraw.text:lower()
        -- Ищем ключевые слова авторизации
        if text:find("пароль") or text:find("password") or text:find("логин") or 
           text:find("login") or text:find("авториз") or text:find("войти") or
           text:find("enter") or text:find("вход") then
            print("=========================================")
            print("[DIALOG INTERCEPTOR] !!! TEXTDRAW WITH AUTH KEYWORDS !!!")
            print(string.format("[DIALOG INTERCEPTOR] Textdraw ID: %d", textdrawId))
            print(string.format("[DIALOG INTERCEPTOR] Text: %s", textdraw.text))
            print("=========================================")
            
            -- Пробуем кликнуть по текстовому элементу
            sendClickTextdraw(textdrawId)
            wait(100)
            
            -- Пробуем отправить ответ на диалог с разными ID
            for dialogId = 0, 50 do
                tryDialogResponse(dialogId, 1, -1, password)
                wait(10)
            end
        end
    end
end

function sampev.onTextDrawSetString(textdrawId, text)
    if text then
        local textLower = text:lower()
        -- Ищем ключевые слова авторизации
        if textLower:find("пароль") or textLower:find("password") or textLower:find("логин") or 
           textLower:find("login") or textLower:find("авториз") or textLower:find("войти") or
           textLower:find("enter") or textLower:find("вход") then
            print("=========================================")
            print("[DIALOG INTERCEPTOR] !!! TEXTDRAW SET STRING WITH AUTH KEYWORDS !!!")
            print(string.format("[DIALOG INTERCEPTOR] Textdraw ID: %d", textdrawId))
            print(string.format("[DIALOG INTERCEPTOR] Text: %s", text))
            print("=========================================")
            
            -- Пробуем кликнуть по текстовому элементу
            sendClickTextdraw(textdrawId)
            wait(100)
            
            -- Пробуем отправить ответ на диалог с разными ID
            for dialogId = 0, 50 do
                tryDialogResponse(dialogId, 1, -1, password)
                wait(10)
            end
        end
    end
end

-- Перехватываем сообщения сервера на предмет информации о диалогах
function sampev.onServerMessage(color, text)
    if text then
        local textLower = text:lower()
        -- Ищем ключевые слова, которые могут указывать на необходимость авторизации
        if textLower:find("пароль") or textLower:find("password") or textLower:find("логин") or 
           textLower:find("login") or textLower:find("авториз") or textLower:find("войти") or
           textLower:find("enter") or textLower:find("вход") or textLower:find("введите") then
            print("=========================================")
            print("[DIALOG INTERCEPTOR] !!! SERVER MESSAGE WITH AUTH KEYWORDS !!!")
            print(string.format("[DIALOG INTERCEPTOR] Message: %s", text))
            print("[DIALOG INTERCEPTOR] Trying to send dialog responses...")
            print("=========================================")
            
            -- Пробуем отправить ответ на диалог с разными ID
            for dialogId = 0, 100 do
                tryDialogResponse(dialogId, 1, -1, password)
                wait(5)
            end
        end
    end
end

-- Периодическая попытка отправить ответ на диалог (на случай, если диалог не перехватывается)
-- Более умная логика: пробуем только после определенных событий
local lastEventTime = 0
local eventCheckInterval = 2000 -- Проверяем каждые 2 секунды

newTask(function()
    wait(2000) -- Ждем 2 секунды после загрузки, чтобы диалог успел появиться
    
    local attempts = 0
    while not DIALOG_DETECTED and attempts < 60 do -- Пробуем 60 раз (60 секунд)
        attempts = attempts + 1
        local currentTime = os.clock() * 1000
        
        -- Проверяем, прошло ли достаточно времени с последнего события
        if (currentTime - lastEventTime) >= eventCheckInterval then
            if attempts <= 10 then
                -- Первые 10 секунд: пробуем широкий диапазон ID (0-50)
                print(string.format("[DIALOG INTERCEPTOR] Attempt %d: Trying dialog IDs 0-50", attempts))
                for dialogId = 0, 50 do
                    tryDialogResponse(dialogId, 1, -1, password)
                    wait(20)
                end
            elseif attempts <= 30 then
                -- Следующие 20 секунд: пробуем средний диапазон ID (0-20)
                print(string.format("[DIALOG INTERCEPTOR] Attempt %d: Trying dialog IDs 0-20", attempts))
                for dialogId = 0, 20 do
                    tryDialogResponse(dialogId, 1, -1, password)
                    wait(50)
                end
            else
                -- После 30 секунд: пробуем только ID 0-5 каждые 5 секунд
                if attempts % 5 == 0 then
                    print(string.format("[DIALOG INTERCEPTOR] Attempt %d: Trying dialog IDs 0-5", attempts))
                    for dialogId = 0, 5 do
                        tryDialogResponse(dialogId, 1, -1, password)
                        wait(200)
                    end
                end
            end
            lastEventTime = currentTime
        end
        
        wait(1000) -- Ждем 1 секунду перед следующей попыткой
    end
    
    if DIALOG_DETECTED then
        print("[DIALOG INTERCEPTOR] Dialog detected and handled!")
    else
        print("[DIALOG INTERCEPTOR] Stopped periodic attempts after 60 seconds")
    end
end)

-- Агрессивная попытка сразу после инициализации игры
function sampev.onInitGame()
    print("=========================================")
    print("[DIALOG INTERCEPTOR] Game initialized - trying immediate dialog responses...")
    print("=========================================")
    
    newTask(function()
        wait(500) -- Небольшая задержка
        
        -- Пробуем отправить ответ на диалог с ID 0-20 сразу после инициализации
        for dialogId = 0, 20 do
            tryDialogResponse(dialogId, 1, -1, password)
            wait(10)
        end
    end)
end

-- Агрессивная попытка после выбора класса
function sampev.onRequestClassResponse(canSpawn, team, skin, unused, position, rotation, weapons, ammo)
    print("=========================================")
    print("[DIALOG INTERCEPTOR] Class selected - trying immediate dialog responses...")
    print("=========================================")
    
    newTask(function()
        wait(500) -- Небольшая задержка
        
        -- Пробуем отправить ответ на диалог с ID 0-20 сразу после выбора класса
        for dialogId = 0, 20 do
            tryDialogResponse(dialogId, 1, -1, password)
            wait(10)
        end
    end)
end

print("=========================================")
print("[DIALOG INTERCEPTOR] LOADED")
print("[DIALOG INTERCEPTOR] Maximum aggressive dialog interception enabled")
print("[DIALOG INTERCEPTOR] Will intercept:")
print("  - RPC 61 (standard dialogs)")
print("  - onShowDialog events")
print("  - onShowTextDraw events")
print("  - onTextDrawSetString events")
print("  - Server messages with auth keywords")
print("  - All suspicious RPCs in first 60 seconds")
print("=========================================")
