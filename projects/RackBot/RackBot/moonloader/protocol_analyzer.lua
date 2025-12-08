-- ============================================
-- СКРИПТ ДЛЯ АНАЛИЗА ПРОТОКОЛА RADMIR RP
-- ============================================
-- Этот скрипт перехватывает и логирует все взаимодействия с сервером
-- Используйте для изучения протокола регистрации, авторизации и прокачки

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local log_dir = "moonloader/protocol_logs/"
local timestamp = os.date("%Y%m%d_%H%M%S")

-- Создаем директорию для логов
local function ensure_dir(path)
    local ok, err = pcall(function()
        os.execute('mkdir "' .. path .. '" 2>nul')
    end)
end

ensure_dir(log_dir)

-- Функция для логирования с временной меткой
local function log_to_file(filename, data)
    local file = io.open(log_dir .. filename, "a")
    if file then
        file:write(os.date("[%Y-%m-%d %H:%M:%S] ") .. data .. "\n")
        file:close()
    end
end

-- Функция для сохранения JSON данных
local function save_json(filename, data)
    local json_str = json.encode(data)
    local file = io.open(log_dir .. filename, "w")
    if file then
        file:write(json_str)
        file:close()
    end
end

print("=========================================")
print("ПРОТОКОЛ АНАЛИЗАТОР ЗАПУЩЕН")
print("Логи сохраняются в: " .. log_dir)
print("=========================================")

-- ============================================
-- ПЕРЕХВАТ ОТПРАВЛЯЕМЫХ КОМАНД
-- ============================================
function sampev.onSendCommand(command)
    local cmd_data = {
        type = "command_sent",
        command = command,
        timestamp = os.time()
    }
    
    log_to_file("commands_sent.log", "КОМАНДА: " .. command)
    save_json("commands_sent_" .. timestamp .. ".json", cmd_data)
    
    print(">>> КОМАНДА: " .. command)
end

-- ============================================
-- ПЕРЕХВАТ СООБЩЕНИЙ СЕРВЕРА
-- ============================================
function sampev.onServerMessage(color, text)
    local msg_data = {
        type = "server_message",
        color = color,
        text = text,
        timestamp = os.time()
    }
    
    log_to_file("server_messages.log", string.format("ЦВЕТ: %d | СООБЩЕНИЕ: %s", color, text))
    save_json("server_messages_" .. timestamp .. ".json", msg_data)
    
    print("<<< СЕРВЕР: " .. text)
end

-- ============================================
-- ПЕРЕХВАТ ДИАЛОГОВ
-- ============================================
function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    local dialog_data = {
        type = "dialog_shown",
        dialogId = dialogId,
        style = style,
        title = title,
        button1 = button1,
        button2 = button2,
        text = text,
        timestamp = os.time()
    }
    
    local log_msg = string.format(
        "ДИАЛОГ | ID: %d | СТИЛЬ: %d | ЗАГОЛОВОК: %s | КНОПКА1: %s | КНОПКА2: %s | ТЕКСТ: %s",
        dialogId, style, title, button1, button2, text
    )
    
    log_to_file("dialogs.log", log_msg)
    save_json("dialog_" .. dialogId .. "_" .. timestamp .. ".json", dialog_data)
    
    print("=== ДИАЛОГ ===")
    print("ID: " .. dialogId)
    print("Заголовок: " .. title)
    print("Текст: " .. text)
    print("Кнопки: [" .. button1 .. "] [" .. button2 .. "]")
end

-- ============================================
-- ПЕРЕХВАТ ОТВЕТОВ НА ДИАЛОГИ
-- ============================================
function sampev.onSendDialogResponse(dialogId, buttonId, listItem, inputText)
    local response_data = {
        type = "dialog_response",
        dialogId = dialogId,
        buttonId = buttonId,
        listItem = listItem,
        inputText = inputText,
        timestamp = os.time()
    }
    
    local log_msg = string.format(
        "ОТВЕТ ДИАЛОГА | ID: %d | КНОПКА: %d | ЭЛЕМЕНТ: %d | ВВОД: %s",
        dialogId, buttonId, listItem, inputText or ""
    )
    
    log_to_file("dialog_responses.log", log_msg)
    save_json("dialog_response_" .. dialogId .. "_" .. timestamp .. ".json", response_data)
    
    print(">>> ОТВЕТ ДИАЛОГА ID:" .. dialogId .. " КНОПКА:" .. buttonId)
    if inputText then
        print("ВВОД: " .. inputText)
    end
end

-- ============================================
-- ПЕРЕХВАТ ЧАТА
-- ============================================
function sampev.onChatMessage(playerId, text)
    local chat_data = {
        type = "chat_message",
        playerId = playerId,
        text = text,
        timestamp = os.time()
    }
    
    log_to_file("chat.log", string.format("ИГРОК %d: %s", playerId, text))
    save_json("chat_" .. timestamp .. ".json", chat_data)
end

-- ============================================
-- ПЕРЕХВАТ ОТПРАВКИ ЧАТА
-- ============================================
function sampev.onSendChat(text)
    local chat_data = {
        type = "chat_sent",
        text = text,
        timestamp = os.time()
    }
    
    log_to_file("chat_sent.log", "ОТПРАВЛЕНО: " .. text)
    save_json("chat_sent_" .. timestamp .. ".json", chat_data)
    
    print(">>> ЧАТ: " .. text)
end

-- ============================================
-- ПЕРЕХВАТ ПОДКЛЮЧЕНИЯ К СЕРВЕРУ
-- ============================================
function sampev.onServerJoin(serverIp, serverPort)
    local join_data = {
        type = "server_join",
        serverIp = serverIp,
        serverPort = serverPort,
        timestamp = os.time()
    }
    
    log_to_file("connection.log", string.format("ПОДКЛЮЧЕНИЕ: %s:%d", serverIp, serverPort))
    save_json("server_join_" .. timestamp .. ".json", join_data)
    
    print("=== ПОДКЛЮЧЕНИЕ К СЕРВЕРУ ===")
    print("IP: " .. serverIp)
    print("Порт: " .. serverPort)
end

-- ============================================
-- ПЕРЕХВАТ ОТКЛЮЧЕНИЯ
-- ============================================
function sampev.onDisconnect()
    local disconnect_data = {
        type = "disconnect",
        timestamp = os.time()
    }
    
    log_to_file("connection.log", "ОТКЛЮЧЕНИЕ ОТ СЕРВЕРА")
    save_json("disconnect_" .. timestamp .. ".json", disconnect_data)
    
    print("=== ОТКЛЮЧЕНИЕ ===")
end

-- ============================================
-- ПЕРЕХВАТ СПАВНА ИГРОКА
-- ============================================
function sampev.onPlayerSpawn()
    local spawn_data = {
        type = "player_spawn",
        timestamp = os.time()
    }
    
    log_to_file("game_events.log", "ИГРОК ЗАСПАВНЕН")
    save_json("spawn_" .. timestamp .. ".json", spawn_data)
    
    print("=== ИГРОК ЗАСПАВНЕН ===")
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
    print("АНАЛИЗАТОР ПРОТОКОЛА АКТИВЕН")
    print("Начинайте регистрацию/авторизацию")
    print("Все действия будут залогированы")
    print("=========================================")
    
    -- Сохраняем информацию о запуске
    local startup_data = {
        type = "analyzer_started",
        timestamp = os.time(),
        samp_loaded = isSampLoaded(),
        sampfuncs_loaded = isSampfuncsLoaded()
    }
    save_json("analyzer_start_" .. timestamp .. ".json", startup_data)
    
    -- Основной цикл - скрипт работает постоянно
    while true do
        wait(1000)
    end
end

