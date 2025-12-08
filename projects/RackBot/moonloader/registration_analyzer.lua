-- ============================================
-- АНАЛИЗАТОР ПРОЦЕССА РЕГИСТРАЦИИ
-- ============================================
-- Специальный скрипт для детального анализа регистрации

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local log_dir = "moonloader/registration_logs/"
local registration_data = {
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
    table.insert(registration_data.steps, {
        step = step_name,
        data = data,
        timestamp = os.time()
    })
    
    local file = io.open(log_dir .. "registration_steps.log", "a")
    if file then
        file:write(string.format("[%s] %s: %s\n", 
            os.date("%H:%M:%S"), step_name, json.encode(data)))
        file:close()
    end
end

print("=========================================")
print("АНАЛИЗАТОР РЕГИСТРАЦИИ ЗАПУЩЕН")
print("Выполните процесс регистрации в игре")
print("=========================================")

-- Отслеживание начала регистрации
local registration_started = false

function sampev.onSendCommand(command)
    if string.find(command:lower(), "register") or 
       string.find(command:lower(), "reg") or
       string.find(command:lower(), "регистр") then
        registration_started = true
        log_step("REGISTRATION_START", {command = command})
        print(">>> НАЧАЛО РЕГИСТРАЦИИ: " .. command)
    end
    
    if registration_started then
        table.insert(registration_data.commands, {
            command = command,
            timestamp = os.time()
        })
    end
end

function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    if registration_started then
        local dialog_info = {
            dialogId = dialogId,
            style = style,
            title = title,
            button1 = button1,
            button2 = button2,
            text = text
        }
        
        table.insert(registration_data.dialogs, dialog_info)
        log_step("DIALOG_SHOWN", dialog_info)
        
        print("=== ДИАЛОГ РЕГИСТРАЦИИ ===")
        print("ID: " .. dialogId)
        print("Заголовок: " .. title)
        print("Текст: " .. text)
        
        -- Сохраняем полный текст диалога
        local file = io.open(log_dir .. "dialog_" .. dialogId .. ".txt", "w")
        if file then
            file:write("ЗАГОЛОВОК: " .. title .. "\n\n")
            file:write("ТЕКСТ:\n" .. text .. "\n\n")
            file:write("КНОПКИ: [" .. button1 .. "] [" .. button2 .. "]\n")
            file:write("СТИЛЬ: " .. style .. "\n")
            file:close()
        end
    end
end

function sampev.onSendDialogResponse(dialogId, buttonId, listItem, inputText)
    if registration_started then
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
    if registration_started then
        table.insert(registration_data.messages, {
            color = color,
            text = text,
            timestamp = os.time()
        })
        
        log_step("SERVER_MESSAGE", {color = color, text = text})
        
        -- Проверяем на успех/ошибку
        local lower_text = text:lower()
        if string.find(lower_text, "успеш") or 
           string.find(lower_text, "зарегистрирован") or
           string.find(lower_text, "success") then
            registration_data.result = "SUCCESS"
            registration_data.end_time = os.time()
            log_step("REGISTRATION_SUCCESS", {message = text})
            print(">>> ✅ РЕГИСТРАЦИЯ УСПЕШНА!")
        elseif string.find(lower_text, "ошибк") or 
               string.find(lower_text, "error") or
               string.find(lower_text, "неверн") or
               string.find(lower_text, "уже") then
            registration_data.result = "ERROR"
            registration_data.end_time = os.time()
            registration_data.error_message = text
            log_step("REGISTRATION_ERROR", {message = text})
            print(">>> ❌ ОШИБКА РЕГИСТРАЦИИ: " .. text)
        end
    end
end

function main()
    wait(2000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("ОШИБКА: SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    print("Ожидание начала регистрации...")
    
    -- Сохраняем данные каждые 5 секунд
    while true do
        wait(5000)
        
        if registration_started then
            -- Сохраняем промежуточные данные
            local file = io.open(log_dir .. "registration_data.json", "w")
            if file then
                file:write(json.encode(registration_data))
                file:close()
            end
            
            -- Если регистрация завершена, сохраняем финальный отчет
            if registration_data.result then
                local report_file = io.open(log_dir .. "registration_report.txt", "w")
                if report_file then
                    report_file:write("========================================\n")
                    report_file:write("ОТЧЕТ О РЕГИСТРАЦИИ\n")
                    report_file:write("========================================\n\n")
                    report_file:write("РЕЗУЛЬТАТ: " .. registration_data.result .. "\n")
                    report_file:write("ВРЕМЯ НАЧАЛА: " .. os.date("%Y-%m-%d %H:%M:%S", registration_data.start_time) .. "\n")
                    if registration_data.end_time then
                        report_file:write("ВРЕМЯ ЗАВЕРШЕНИЯ: " .. os.date("%Y-%m-%d %H:%M:%S", registration_data.end_time) .. "\n")
                    end
                    if registration_data.error_message then
                        report_file:write("ОШИБКА: " .. registration_data.error_message .. "\n")
                    end
                    report_file:write("\nКОМАНДЫ:\n")
                    for i, cmd in ipairs(registration_data.commands) do
                        report_file:write(string.format("%d. %s\n", i, cmd.command))
                    end
                    report_file:write("\nДИАЛОГИ:\n")
                    for i, dlg in ipairs(registration_data.dialogs) do
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

