-- ============================================
-- АНАЛИЗАТОР ПРОЦЕССА АВТОРИЗАЦИИ
-- ============================================

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local log_dir = "moonloader/login_logs/"
local login_data = {
    start_time = os.time(),
    steps = {},
    dialogs = {},
    commands = {},
    messages = {}
}

local function ensure_dir(path)
    os.execute('mkdir "' .. path .. '" 2>nul')
end

ensure_dir(log_dir)

local function log_step(step_name, data)
    table.insert(login_data.steps, {
        step = step_name,
        data = data,
        timestamp = os.time()
    })
    
    local file = io.open(log_dir .. "login_steps.log", "a")
    if file then
        file:write(string.format("[%s] %s: %s\n", 
            os.date("%H:%M:%S"), step_name, json.encode(data)))
        file:close()
    end
end

print("=========================================")
print("АНАЛИЗАТОР АВТОРИЗАЦИИ ЗАПУЩЕН")
print("Выполните процесс входа в игре")
print("=========================================")

local login_started = false

function sampev.onSendCommand(command)
    if string.find(command:lower(), "login") or 
       string.find(command:lower(), "войти") or
       string.find(command:lower(), "вход") then
        login_started = true
        log_step("LOGIN_START", {command = command})
        print(">>> НАЧАЛО АВТОРИЗАЦИИ: " .. command)
    end
    
    if login_started then
        table.insert(login_data.commands, {
            command = command,
            timestamp = os.time()
        })
    end
end

function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    if login_started then
        local dialog_info = {
            dialogId = dialogId,
            style = style,
            title = title,
            button1 = button1,
            button2 = button2,
            text = text
        }
        
        table.insert(login_data.dialogs, dialog_info)
        log_step("DIALOG_SHOWN", dialog_info)
        
        print("=== ДИАЛОГ АВТОРИЗАЦИИ ===")
        print("ID: " .. dialogId)
        print("Заголовок: " .. title)
        print("Текст: " .. text)
    end
end

function sampev.onSendDialogResponse(dialogId, buttonId, listItem, inputText)
    if login_started then
        local response_info = {
            dialogId = dialogId,
            buttonId = buttonId,
            listItem = listItem,
            inputText = inputText
        }
        
        log_step("DIALOG_RESPONSE", response_info)
        print(">>> ОТВЕТ ДИАЛОГА:")
        print("ID: " .. dialogId)
        print("Кнопка: " .. buttonId)
        if inputText then
            print("ВВОД: " .. inputText)
        end
    end
end

function sampev.onServerMessage(color, text)
    if login_started then
        table.insert(login_data.messages, {
            color = color,
            text = text,
            timestamp = os.time()
        })
        
        log_step("SERVER_MESSAGE", {color = color, text = text})
        
        local lower_text = text:lower()
        if string.find(lower_text, "успеш") or 
           string.find(lower_text, "авторизован") or
           string.find(lower_text, "добро") or
           string.find(lower_text, "success") or
           string.find(lower_text, "welcome") then
            login_data.result = "SUCCESS"
            login_data.end_time = os.time()
            log_step("LOGIN_SUCCESS", {message = text})
            print(">>> ✅ АВТОРИЗАЦИЯ УСПЕШНА!")
        elseif string.find(lower_text, "ошибк") or 
               string.find(lower_text, "error") or
               string.find(lower_text, "неверн") or
               string.find(lower_text, "неправильн") then
            login_data.result = "ERROR"
            login_data.end_time = os.time()
            login_data.error_message = text
            log_step("LOGIN_ERROR", {message = text})
            print(">>> ❌ ОШИБКА АВТОРИЗАЦИИ: " .. text)
        end
    end
end

function main()
    wait(2000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("ОШИБКА: SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    print("Ожидание начала авторизации...")
    
    while true do
        wait(5000)
        
        if login_started then
            local file = io.open(log_dir .. "login_data.json", "w")
            if file then
                file:write(json.encode(login_data))
                file:close()
            end
            
            if login_data.result then
                local report_file = io.open(log_dir .. "login_report.txt", "w")
                if report_file then
                    report_file:write("========================================\n")
                    report_file:write("ОТЧЕТ ОБ АВТОРИЗАЦИИ\n")
                    report_file:write("========================================\n\n")
                    report_file:write("РЕЗУЛЬТАТ: " .. login_data.result .. "\n")
                    report_file:write("ВРЕМЯ НАЧАЛА: " .. os.date("%Y-%m-%d %H:%M:%S", login_data.start_time) .. "\n")
                    if login_data.end_time then
                        report_file:write("ВРЕМЯ ЗАВЕРШЕНИЯ: " .. os.date("%Y-%m-%d %H:%M:%S", login_data.end_time) .. "\n")
                    end
                    if login_data.error_message then
                        report_file:write("ОШИБКА: " .. login_data.error_message .. "\n")
                    end
                    report_file:write("\nКОМАНДЫ:\n")
                    for i, cmd in ipairs(login_data.commands) do
                        report_file:write(string.format("%d. %s\n", i, cmd.command))
                    end
                    report_file:write("\nДИАЛОГИ:\n")
                    for i, dlg in ipairs(login_data.dialogs) do
                        report_file:write(string.format("%d. ID: %d | %s\n", i, dlg.dialogId, dlg.title))
                    end
                    report_file:close()
                end
                
                print(">>> ОТЧЕТ СОХРАНЕН")
                break
            end
        end
    end
end

