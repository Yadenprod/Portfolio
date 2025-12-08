"""
Модуль для интеграции с Moonloader скриптами
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class MoonloaderIntegration:
    """Класс для работы с Moonloader скриптами"""
    
    def __init__(self, scripts_dir: str = 'moonloader'):
        """
        Инициализация
        
        Args:
            scripts_dir: Директория для Moonloader скриптов
        """
        self.scripts_dir = Path(scripts_dir)
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_register_script(self, username: str, password: str, email: str, 
                                 output_file: str = None) -> str:
        """
        Генерирует Moonloader скрипт для регистрации аккаунта
        
        Args:
            username: Имя пользователя
            password: Пароль
            email: Email
            output_file: Имя выходного файла
        
        Returns:
            Путь к созданному скрипту
        """
        if output_file is None:
            output_file = f"register_{username}.lua"
        
        script_content = f'''-- Moonloader скрипт для регистрации аккаунта
-- Сгенерировано RackBot

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local username = "{username}"
local password = "{password}"
local email = "{email}"

function main()
    wait(5000)  -- Ждем загрузки игры
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    -- Подключаемся к серверу (если еще не подключены)
    if not sampIsLocalPlayerSpawned() then
        -- Логика подключения
        wait(2000)
    end
    
    -- Регистрация через команду или диалог
    -- Вариант 1: Команда /register
    sampSendChat("/register " .. password .. " " .. email)
    
    -- Вариант 2: Если используется диалог регистрации
    -- Нужно найти ID диалога и заполнить поля
    -- sampSendDialogResponse(dialogId, buttonId, listItem, inputText)
    
    wait(1000)
    
    -- Проверяем успешность регистрации
    -- Можно проверить через сообщение в чате или статус
    
    print("Регистрация завершена для: " .. username)
end

-- Обработка ответов сервера
function sampev.onServerMessage(color, text)
    if string.find(text, "успешно") or string.find(text, "зарегистрирован") then
        print("Регистрация успешна!")
        -- Можно сохранить результат в файл для Python бота
        local file = io.open("moonloader/register_result.json", "w")
        if file then
            file:write(json.encode({{username = username, status = "success"}}))
            file:close()
        end
    elseif string.find(text, "ошибка") or string.find(text, "уже") then
        print("Ошибка регистрации: " .. text)
        local file = io.open("moonloader/register_result.json", "w")
        if file then
            file:write(json.encode({{username = username, status = "error", message = text}}))
            file:close()
        end
    end
end
'''
        
        script_path = self.scripts_dir / output_file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def generate_login_script(self, username: str, password: str,
                             output_file: str = None) -> str:
        """
        Генерирует Moonloader скрипт для авторизации
        
        Args:
            username: Имя пользователя
            password: Пароль
            output_file: Имя выходного файла
        
        Returns:
            Путь к созданному скрипту
        """
        if output_file is None:
            output_file = f"login_{username}.lua"
        
        script_content = f'''-- Moonloader скрипт для авторизации
-- Сгенерировано RackBot

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local username = "{username}"
local password = "{password}"

function main()
    wait(5000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    -- Авторизация через команду
    sampSendChat("/login " .. password)
    
    -- Или через диалог
    -- sampSendDialogResponse(dialogId, buttonId, listItem, password)
    
    wait(1000)
    print("Авторизация для: " .. username)
end

function sampev.onServerMessage(color, text)
    if string.find(text, "успешно") or string.find(text, "авторизован") then
        print("Авторизация успешна!")
        local file = io.open("moonloader/login_result.json", "w")
        if file then
            file:write(json.encode({{username = username, status = "success"}}))
            file:close()
        end
    end
end
'''
        
        script_path = self.scripts_dir / output_file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def generate_farm_script(self, actions: List[str] = None,
                            output_file: str = "farm_exp.lua") -> str:
        """
        Генерирует Moonloader скрипт для прокачки опыта
        
        Args:
            actions: Список действий для прокачки
            output_file: Имя выходного файла
        
        Returns:
            Путь к созданному скрипту
        """
        if actions is None:
            actions = ['move', 'jump', 'crouch']
        
        actions_lua = json.dumps(actions, ensure_ascii=False)
        
        script_content = f'''-- Moonloader скрипт для прокачки опыта
-- Сгенерировано RackBot

require "lib.moonloader"
local sampev = require 'lib.samp.events'
local encoding = require 'encoding'
encoding.default = 'CP1251'

local actions = {actions_lua}
local current_action = 1
local action_interval = 2000  -- Интервал между действиями в мс

function main()
    wait(5000)
    
    if not isSampLoaded() or not isSampfuncsLoaded() then
        print("SAMP или SAMPFUNCS не загружены!")
        return
    end
    
    -- Проверяем, что игрок заспавнен
    if not sampIsLocalPlayerSpawned() then
        print("Игрок не заспавнен!")
        return
    end
    
    print("Начало прокачки опыта...")
    
    -- Основной цикл прокачки
    while true do
        if sampIsLocalPlayerSpawned() then
            performAction(actions[current_action])
            current_action = (current_action % #actions) + 1
        end
        
        wait(action_interval + math.random(-500, 500))  -- Случайная задержка
    end
end

function performAction(action)
    if action == "move" or action == "move_forward" then
        -- Движение вперед
        setCharControlState(PLAYER_PED, 0, true)  -- W
        wait(500)
        setCharControlState(PLAYER_PED, 0, false)
    elseif action == "jump" then
        -- Прыжок
        setCharControlState(PLAYER_PED, 2, true)  -- Space
        wait(100)
        setCharControlState(PLAYER_PED, 2, false)
    elseif action == "crouch" then
        -- Приседание
        setCharControlState(PLAYER_PED, 15, true)  -- C
        wait(500)
        setCharControlState(PLAYER_PED, 15, false)
    elseif action == "turn_left" then
        -- Поворот влево
        setCharControlState(PLAYER_PED, 4, true)  -- A
        wait(300)
        setCharControlState(PLAYER_PED, 4, false)
    elseif action == "turn_right" then
        -- Поворот вправо
        setCharControlState(PLAYER_PED, 5, true)  -- D
        wait(300)
        setCharControlState(PLAYER_PED, 5, false)
    end
end

-- Обработка сообщений о получении опыта
function sampev.onServerMessage(color, text)
    if string.find(text, "опыт") or string.find(text, "exp") or string.find(text, "EXP") then
        print("Получен опыт: " .. text)
    end
end
'''
        
        script_path = self.scripts_dir / output_file
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return str(script_path)
    
    def check_script_result(self, result_file: str = "register_result.json") -> Optional[Dict]:
        """
        Проверяет результат выполнения Moonloader скрипта
        
        Args:
            result_file: Имя файла с результатом
        
        Returns:
            Словарь с результатом или None
        """
        result_path = self.scripts_dir / result_file
        
        if not result_path.exists():
            return None
        
        try:
            with open(result_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка чтения результата: {e}")
            return None
    
    def get_available_scripts(self) -> List[str]:
        """Возвращает список доступных Moonloader скриптов"""
        return [f.name for f in self.scripts_dir.glob("*.lua")]

