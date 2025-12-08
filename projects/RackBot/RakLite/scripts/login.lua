-- Скрипт авторизации для RakSAMP Lite
-- Поместите этот файл в RakLite/scripts/

require("addon")
local sampev = require("samp.events")

-- Перехватываем RPC напрямую для отладки ВСЕХ RPC
-- Регистрируем через registerHandler чтобы точно сработало
local RPC_LOG_START_TIME = nil
local RPC_LOG_DURATION = 10000 -- Логируем первые 10 секунд после подключения

registerHandler("onReceiveRPC", function(id, bs)
    -- Определяем время начала логирования (при первом RPC после подключения)
    if not RPC_LOG_START_TIME then
        RPC_LOG_START_TIME = os.clock() * 1000
        print("=========================================")
        print("RPC LOGGING STARTED - First 10 seconds")
        print("=========================================")
    end
    
    local timeSinceStart = (os.clock() * 1000) - RPC_LOG_START_TIME
    local shouldLog = timeSinceStart < RPC_LOG_DURATION
    
    -- Логируем ВСЕ RPC для отладки (только важные, чтобы не засорять логи)
    -- RPC.SHOWDIALOG может быть 61 (RPC_SCRSHOWDIALOG) или 63 (стандартный)
    if id == 61 then -- RPC_SCRSHOWDIALOG = 61 (0x3D)
        print("=========================================")
        print("!!! RPC 61 (SHOWDIALOG) RECEIVED !!!")
        print("=========================================")
        print("This is a dialog RPC!")
        
        -- Пробуем прочитать данные диалога вручную (формат из rakbot)
        if bs and bs ~= 0 then
            -- Сохраняем текущую позицию чтения
            local readOffset = bs:getReadOffset()
            
            -- Читаем данные диалога (формат из rakbot ScrShowDialog):
            -- dialogId (uint16_t)
            -- dialogStyle (uint8_t)
            -- titleLen (uint8_t) + title (char[])
            -- okButtonLen (uint8_t) + okButton (char[])
            -- cancelButtonLen (uint8_t) + cancelButton (char[])
            -- dialogText (encoded string)
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
            
            -- Читаем dialogText (encoded string - пропускаем, так как это сложно)
            print("Dialog ID:", dialogId, "Style:", style)
            print("Title:", title)
            print("OK Button:", okButton)
            print("Cancel Button:", cancelButton)
            
            -- Если идет авторизация - обрабатываем ВСЕ диалоги (включая кастомные style 255)
            if not _AUTHORIZATION_COMPLETE and _AUTHORIZATION_IN_PROGRESS then
                print(">>> Processing dialog during authorization!")
                print(">>> Dialog ID:", dialogId, "Style:", style)
                print(">>> Filling password:", password)
                
                -- Отправляем ответ на диалог с паролем (формат из rakbot)
                sendDialogResponse(dialogId, 1, -1, password) -- button=1 (OK/Enter), list=-1, input=password
                print(">>> Password sent via dialog response! id=" .. dialogId)
                
                -- Сохраняем ID диалога
                _LAST_DIALOG_ID = dialogId
            end
            
            -- Восстанавливаем позицию чтения для библиотеки
            bs:setReadOffset(readOffset)
        end
        print("=========================================")
    -- RPC 225 и 226 - это НЕ диалоги, это что-то другое (синхронизация объектов/текстдравов)
    -- Игнорируем их, так как они не являются диалогами авторизации
    -- Логируем другие важные RPC
    elseif id == 50 then -- RPC.INITGAME
        print("[DEBUG] RPC 50 (INITGAME) received")
    elseif id == 51 then -- RPC.SERVERJOIN
        print("[DEBUG] RPC 51 (SERVERJOIN) received")
    elseif id == 52 then -- RPC.SERVERQUIT
        print("[DEBUG] RPC 52 (SERVERQUIT) received")
    elseif id == 128 then -- RPC.REQUESTCLASS
        print("[DEBUG] RPC 128 (REQUESTCLASS) received")
    elseif id == 134 then -- RPC.SHOWTEXTDRAW (стандартный текстдрав)
        if _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
            print("=========================================")
            print("!!! RPC 134 (SHOWTEXTDRAW) received during auth!")
            print("=========================================")
        end
    elseif id == 60 then -- RPC 60 - подозрительный RPC (4 байта)
        if _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
            print("=========================================")
            print("!!! RPC 60 received during auth!")
            print("=========================================")
            if bs and bs ~= 0 then
                local readOffset = bs:getReadOffset()
                local firstBytes = {}
                for i = 1, 4 do
                    firstBytes[i] = bs:readUInt8()
                end
                bs:setReadOffset(readOffset)
                print("RPC 60 bytes:", table.concat(firstBytes, ", "))
                -- Пробуем интерпретировать как диалог (маловероятно, но попробуем)
                -- Если первые 2 байта похожи на dialogId (uint16_t)
                if firstBytes[1] < 100 and firstBytes[2] == 0 then
                    local possibleDialogId = firstBytes[1]
                    print(">>> RPC 60 might be dialog with ID:", possibleDialogId)
                    sendDialogResponse(possibleDialogId, 1, -1, password)
                end
            end
        end
    elseif id == 29 then -- RPC 29 - подозрительный RPC (2 байта)
        if _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
            print("=========================================")
            print("!!! RPC 29 received during auth!")
            print("=========================================")
            if bs and bs ~= 0 then
                local readOffset = bs:getReadOffset()
                local firstBytes = {}
                for i = 1, 2 do
                    firstBytes[i] = bs:readUInt8()
                end
                bs:setReadOffset(readOffset)
                print("RPC 29 bytes:", table.concat(firstBytes, ", "))
            end
        end
    -- Логируем ВСЕ RPC в первые 10 секунд для поиска кастомного диалога
    elseif shouldLog then
        -- Пропускаем только самые частые синхронизационные RPC
        if id ~= 72 and id ~= 11 and id ~= 137 and id ~= 138 and id ~= 155 and id ~= 230 and id ~= 225 and id ~= 226 and id ~= 56 and id ~= 44 and id ~= 58 and id ~= 36 and id ~= 166 and id ~= 45 and id ~= 99 and id ~= 93 and id ~= 69 and id ~= 43 and id ~= 128 and id ~= 129 and id ~= 139 and id ~= 50 and id ~= 51 and id ~= 52 and id ~= 134 and id ~= 61 then
            print("[RPC LOG] RPC " .. id .. " received (time: " .. math.floor(timeSinceStart) .. "ms)")
            
            -- Детальное логирование для подозрительных RPC
            if bs and bs ~= 0 then
                local readOffset = bs:getReadOffset()
                local bitsUsed = bs:getNumberOfBitsUsed()
                local bytesUsed = math.floor(bitsUsed/8)
                
                -- Логируем размер и первые байты для анализа
                if bytesUsed > 0 and bytesUsed < 500 then
                    print("  [RPC LOG] RPC " .. id .. " data: " .. bytesUsed .. " bytes")
                    -- Пробуем прочитать первые несколько байт для анализа
                    local firstBytes = {}
                    local maxBytes = math.min(10, bytesUsed)
                    for i = 1, maxBytes do
                        firstBytes[i] = bs:readUInt8()
                    end
                    bs:setReadOffset(readOffset)
                    print("  [RPC LOG] First bytes: " .. table.concat(firstBytes, ", "))
                end
            end
        end
    -- Логируем другие важные RPC во время авторизации (после первых 10 секунд)
    elseif _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
        -- Пропускаем стандартные синхронизационные RPC
        if id ~= 72 and id ~= 11 and id ~= 137 and id ~= 138 and id ~= 155 and id ~= 230 and id ~= 225 and id ~= 226 and id ~= 56 and id ~= 44 and id ~= 58 and id ~= 36 and id ~= 166 and id ~= 45 and id ~= 99 and id ~= 93 and id ~= 69 and id ~= 43 and id ~= 128 and id ~= 129 and id ~= 139 then
            print("[DEBUG] RPC " .. id .. " received during authorization")
        end
    end
end)

-- ============================================
-- НАСТРОЙКИ
-- ============================================
-- Функция для чтения ника из конфигурационного файла
local function getNicknameFromConfig()
    local configFile = io.open("settings/RakSAMP Lite.ini", "r")
    if configFile then
        for line in configFile:lines() do
            local nick = line:match("^nick%s*=%s*(.+)")
            if nick then
                configFile:close()
                return nick:match("^%s*(.-)%s*$") -- Убираем пробелы
            end
        end
        configFile:close()
    end
    return "test_user" -- Значение по умолчанию
end

local username = getNicknameFromConfig()  -- Читаем ник из конфига
password = "123456789q"   -- Пароль для авторизации (глобальная переменная для доступа из обработчиков)

-- Глобальный флаг состояния авторизации
_AUTHORIZATION_COMPLETE = false
_AUTHORIZATION_IN_PROGRESS = false
_GAME_INITIALIZED = false  -- Флаг инициализации игры
_LAST_DIALOG_ID = nil  -- Последний ID диалога, который мы видели

-- Начинаем слушать события сразу при загрузке скрипта
-- Диалог может появиться в любой момент, даже до onInitGame
print("=========================================")
print("LOGIN SCRIPT LOADED")
print("Waiting for authorization dialog...")
print("=========================================")

-- ============================================
-- ОСНОВНАЯ ЛОГИКА
-- ============================================

-- Событие инициализации игры (реальное подключение)
function sampev.onInitGame()
    print("=========================================")
    print("GAME INITIALIZED - REAL CONNECTION")
    print("=========================================")
    _GAME_INITIALIZED = true
    
    -- Начинаем авторизацию сразу
    _AUTHORIZATION_IN_PROGRESS = true
    _AUTHORIZATION_COMPLETE = false
    
    print("=========================================")
    print("AUTHORIZATION STARTED")
    print("=========================================")
                print("Username:", username)
                print("Waiting for authorization dialog...")
                print("=========================================")
                
                -- КРИТИЧЕСКИ ВАЖНО: Пробуем отправить ответ на диалог СРАЗУ после onInitGame
                -- Кастомное окно может появиться сразу, но событие onShowDialog не сработает
                newTask(function()
                    wait(500) -- Небольшая задержка для появления диалога
                    print("=========================================")
                    print("IMMEDIATE DIALOG RESPONSE ATTEMPT")
                    print("=========================================")
                    print("Trying to send dialog response immediately after onInitGame...")
                    for dialogId = 0, 5 do
                        sendDialogResponse(dialogId, 1, -1, password)
                        wait(100)
                    end
                    print("=========================================")
                end)
     
     -- Пробуем альтернативные методы авторизации
    newTask(function()
        -- Ждем 3 секунды после подключения
        wait(3000)
        
        -- Метод 1: Попробуем отправить пароль через команду (если сервер поддерживает)
        print("=========================================")
        print("Trying alternative authorization methods...")
        print("=========================================")
        
        -- Пробуем различные варианты команд
        local loginCommands = {
            "/login " .. password,
            "/l " .. password,
            "/auth " .. password,
            "/pass " .. password,
            password  -- Просто пароль без команды
        }
        
        for i, cmd in ipairs(loginCommands) do
            print("Trying command:", cmd)
            sendInput(cmd)
            wait(1000)
            
            -- Если авторизация завершилась, выходим
            if _AUTHORIZATION_COMPLETE then
                print("Authorization successful via command!")
                return
            end
        end
        
        print("Command-based authorization failed, trying dialogs...")
    end)
        
        -- Периодически пробуем отправить ответ на диалог, если он не перехватывается автоматически
        newTask(function()
            local attempts = 0
            
            -- Ждем 2 секунды после подключения, чтобы диалог успел появиться
            wait(2000)
            
            while not _AUTHORIZATION_COMPLETE and attempts < 30 do -- Пробуем 30 раз (30 секунд)
                attempts = attempts + 1
                
                if not _AUTHORIZATION_COMPLETE then
                    -- Если мы видели диалог через RPC, пробуем его ID
                    if _LAST_DIALOG_ID then
                        print("Trying last seen dialog ID:", _LAST_DIALOG_ID)
                        sendDialogResponse(_LAST_DIALOG_ID, 1, -1, password)
                        wait(100) -- Небольшая задержка между попытками
                    end
                    
                    -- Пробуем отправить ответ на диалог с разными ID
                    -- Возможно, диалог уже открыт, но событие не сработало
                    if attempts <= 2 then
                        -- Первые 2 попытки пробуем только стандартные ID (0-10)
                        print("Trying dialog IDs 0-10 (attempt", attempts .. ")")
                        for dialogId = 0, 10 do
                            sendDialogResponse(dialogId, 1, -1, password)
                            wait(50)
                        end
                    elseif attempts <= 5 then
                        -- Следующие 3 попытки пробуем расширенный диапазон (0-20)
                        print("Trying dialog IDs 0-20 (attempt", attempts .. ")")
                        for dialogId = 0, 20 do
                            sendDialogResponse(dialogId, 1, -1, password)
                            wait(100)
                        end
                    else
                        -- После 5 попыток пробуем только стандартные ID (0-5) с большей задержкой
                        if attempts % 3 == 0 then -- Каждые 3 попытки
                            print("Trying dialog IDs 0-5 (attempt", attempts .. ")")
                            for dialogId = 0, 5 do
                                sendDialogResponse(dialogId, 1, -1, password)
                                wait(200)
                            end
                        end
                    end
                    
                    if attempts % 5 == 0 then -- Каждые 5 секунд логируем
                        print("Still waiting for dialog... Attempt", attempts, "Last dialog ID:", _LAST_DIALOG_ID or "none")
                    end
                    
                    wait(1000) -- Ждем 1 секунду перед следующей попыткой
                end
            end
        end)
end

-- Старое событие onConnect (может вызываться раньше)
function onConnect()
    print("Connection event received, waiting for game initialization...")
    -- Не делаем ничего здесь, ждем onInitGame
end

-- Обработка текстдравов (может быть диалог реализован через текстдравы)
function sampev.onShowTextDraw(textdrawId, textdraw)
    if _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
        print("=========================================")
        print("!!! TEXTDRAW SHOWN during auth!")
        print("=========================================")
        print("TextDraw ID:", textdrawId)
        if textdraw and textdraw.text then
            print("TextDraw text:", textdraw.text)
            local lower_text = string.lower(textdraw.text or "")
            -- Проверяем, не является ли это диалогом авторизации
            if string.find(lower_text, "пароль") or 
               string.find(lower_text, "password") or
               string.find(lower_text, "войти") or
               string.find(lower_text, "введите") or
               string.find(lower_text, "login") or
               string.find(lower_text, "авториз") then
                print(">>> This might be login textdraw!")
                print(">>> Trying to click textdraw ID:", textdrawId)
                -- Пробуем кликнуть по текстдраву
                sendClickTextdraw(textdrawId)
                -- Также пробуем отправить пароль через диалог
                wait(500)
                for dialogId = 0, 50 do
                    sendDialogResponse(dialogId, 1, -1, password)
                end
            end
        end
        print("=========================================")
    end
end

function sampev.onTextDrawSetString(id, text)
    if _AUTHORIZATION_IN_PROGRESS and not _AUTHORIZATION_COMPLETE then
        print("=========================================")
        print("!!! TEXTDRAW STRING SET during auth!")
        print("=========================================")
        print("TextDraw ID:", id)
        print("Text:", text)
        local lower_text = string.lower(text or "")
        if string.find(lower_text, "пароль") or 
           string.find(lower_text, "password") or
           string.find(lower_text, "войти") or
           string.find(lower_text, "введите") or
           string.find(lower_text, "login") or
           string.find(lower_text, "авториз") then
            print(">>> This might be login textdraw string!")
            print(">>> Trying to click textdraw ID:", id)
            -- Пробуем кликнуть по текстдраву
            sendClickTextdraw(id)
            -- Также пробуем отправить пароль через диалог
            wait(500)
            for dialogId = 0, 50 do
                sendDialogResponse(dialogId, 1, -1, password)
            end
        end
        print("=========================================")
    end
end

function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    -- КРИТИЧЕСКОЕ ЛОГИРОВАНИЕ - эта функция должна вызываться при любом диалоге
    print("=========================================")
    print("!!! DIALOG SHOWN - FUNCTION CALLED !!!")
    print("=========================================")
    print("ID:", dialogId)
    print("Style:", style)
    print("Title:", title or "(no title)")
    print("Button 1:", button1 or "(no button1)")
    print("Button 2:", button2 or "(no button2)")
    print("Text:", (text and text:sub(1, 100)) or "(no text)") -- Первые 100 символов
    print("Auth in progress:", _AUTHORIZATION_IN_PROGRESS)
    print("Auth complete:", _AUTHORIZATION_COMPLETE)
    print("=========================================")
    
    -- Обрабатываем ВСЕ диалоги во время авторизации, независимо от стиля
    if not _AUTHORIZATION_COMPLETE and _AUTHORIZATION_IN_PROGRESS then
        print(">>> Processing dialog during authorization!")
        print(">>> Dialog ID:", dialogId, "Style:", style)
        print(">>> Filling password:", password)
        
        -- Отправляем ответ на диалог с паролем
        sendDialogResponse(dialogId, 1, -1, password) -- button=1 (OK/Enter), list=-1, input=password
        print(">>> Password sent! id=" .. dialogId .. ", button=1, list=-1, input=" .. password)
        
        -- Возвращаем false чтобы предотвратить дальнейшую обработку
        return false
    elseif not _AUTHORIZATION_COMPLETE then
        -- Если авторизация еще не началась, но диалог появился - начинаем авторизацию
        print(">>> Dialog appeared before authorization started, starting now...")
        _AUTHORIZATION_IN_PROGRESS = true
        
        print(">>> Filling password:", password)
        sendDialogResponse(dialogId, 1, -1, password)
        print(">>> Password sent! id=" .. dialogId)
        
        return false
    else
        print(">>> Authorization already complete, skipping dialog...")
    end
end

function sampev.onServerMessage(color, text)
    print("Server message:", text)
    
    local lower_text = string.lower(text or "")
    
    -- Проверяем, не требуется ли авторизация (если сервер просит ввести пароль)
    if not _AUTHORIZATION_COMPLETE and not _AUTHORIZATION_IN_PROGRESS then
        if string.find(lower_text, "пароль") or 
           string.find(lower_text, "password") or
           string.find(lower_text, "войти") or
           string.find(lower_text, "введите") or
           string.find(lower_text, "login") or
           string.find(lower_text, "авториз") or
           string.find(lower_text, "вход") then
            print("=========================================")
            print("SERVER ASKS FOR PASSWORD - Starting authorization!")
            print("=========================================")
            _AUTHORIZATION_IN_PROGRESS = true
            
            -- Пробуем отправить ответ на диалог сразу
            newTask(function()
                wait(500) -- Небольшая задержка
                print("Trying to send dialog response after server message...")
                for dialogId = 0, 20 do
                    sendDialogResponse(dialogId, 1, -1, password)
                    wait(50)
                end
            end)
        end
    end
    
    -- Successful authorization - расширенный список ключевых слов
    if string.find(lower_text, "успешно") or 
       string.find(lower_text, "авторизован") or
       string.find(lower_text, "добро") or
       string.find(lower_text, "welcome") or
       string.find(lower_text, "добро пожаловать") or
       string.find(lower_text, "выберите класс") or
       string.find(lower_text, "выберите скин") or
       string.find(lower_text, "вы вошли") or
       string.find(lower_text, "вы зашли") then
        print("=========================================")
        print("SUCCESS: AUTHORIZATION COMPLETE!")
        print("=========================================")
        
        -- Устанавливаем флаги
        _AUTHORIZATION_COMPLETE = true
        _AUTHORIZATION_IN_PROGRESS = false
        
        local result = {
            username = username,
            status = "success",
            timestamp = os.time()
        }
        
        os.execute('mkdir results 2>nul')
        local file = io.open("results/login_" .. username .. ".json", "w")
        if file then
            -- Простое сохранение без json библиотеки
            file:write(string.format('{"username":"%s","status":"%s","timestamp":%d}', 
                username, result.status, result.timestamp))
            file:close()
        end
    end
    
    -- Authorization error
    if string.find(lower_text, "ошибка") or 
       string.find(lower_text, "error") or
       string.find(lower_text, "неверн") or
       string.find(lower_text, "неправильн") or
       string.find(lower_text, "неверный пароль") then
        print("=========================================")
        print("ERROR: AUTHORIZATION FAILED")
        print("=========================================")
        print("Text:", text)
    end
end

-- Обработчик ответа на запрос класса (когда сервер отвечает на выбор класса)
function sampev.onRequestClassResponse(canSpawn, team, skin, _unused, position, rotation, weapons, ammo)
    print("=========================================")
    print("CLASS SELECTED - REQUESTING SPAWN")
    print("=========================================")
    print("Can spawn:", canSpawn)
    print("Team:", team)
    print("Skin:", skin)
    print("=========================================")
    
    -- НЕ помечаем авторизацию как завершенную после выбора класса
    -- Диалог авторизации может появиться позже, после спавна
    print("Class selected, but NOT marking auth as complete yet")
    print("Waiting for authorization dialog...")
    
    -- КРИТИЧЕСКИ ВАЖНО: Пробуем отправить ответ на диалог сразу после выбора класса
    -- Диалог может появиться в этот момент
    newTask(function()
        wait(500) -- Небольшая задержка для появления диалога
        print("=========================================")
        print("Trying to send dialog response after class selection...")
        print("=========================================")
        
        -- Пробуем разные варианты:
        -- 1. Стандартные ID (0-20) с button=1
        for dialogId = 0, 20 do
            sendDialogResponse(dialogId, 1, -1, password)
            wait(50)
        end
        
        wait(500)
        
        -- 2. Пробуем с button=0
        for dialogId = 0, 10 do
            sendDialogResponse(dialogId, 0, -1, password)
            wait(50)
        end
        
        wait(500)
        
        -- 3. Пробуем с list=0
        for dialogId = 0, 10 do
            sendDialogResponse(dialogId, 1, 0, password)
            wait(50)
        end
        
        print("=========================================")
    end)
    
    -- Автоматически запрашиваем спавн после выбора класса
    if canSpawn then
        newTask(function()
            wait(1000) -- Небольшая задержка
            print("Requesting spawn...")
            sendSpawnRequest()
        end)
    end
end

function sampev.onPlayerSpawn()
    print("=========================================")
    print("PLAYER SPAWNED")
    print("=========================================")
    
    if not _AUTHORIZATION_COMPLETE then
        print("Player spawned but not authorized yet")
        print("Waiting for authorization dialog to appear automatically...")
        
        -- Попробуем отправить ответ на диалог после спавна (может быть диалог появляется после спавна)
        newTask(function()
            wait(1000) -- Ждем 1 секунду после спавна
            print("=========================================")
            print("Trying to send dialog response after spawn...")
            print("=========================================")
            
            -- Пробуем разные варианты:
            -- 1. Стандартные ID (0-20)
            for dialogId = 0, 20 do
                sendDialogResponse(dialogId, 1, -1, password) -- button=1 (OK/Enter)
                wait(50)
            end
            
            wait(500)
            
            -- 2. Пробуем с button=0 (Cancel/No) на случай, если нужен другой формат
            for dialogId = 0, 10 do
                sendDialogResponse(dialogId, 0, -1, password) -- button=0 (Cancel/No)
                wait(50)
            end
            
            wait(500)
            
            -- 3. Пробуем с list=0 вместо -1
            for dialogId = 0, 10 do
                sendDialogResponse(dialogId, 1, 0, password) -- list=0
                wait(50)
            end
            
            print("=========================================")
        end)
    else
        print("Authorization already complete")
    end
end

