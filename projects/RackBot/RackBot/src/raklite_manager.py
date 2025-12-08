"""
Модуль для управления RakLite клиентами
"""
import subprocess
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import threading


class RakLiteManager:
    """Класс для управления экземплярами RakLite"""
    
    def __init__(self, raklite_path: str = "RakLite", config_path: str = "config/raklite_config.json"):
        """
        Инициализация менеджера RakLite
        
        Args:
            raklite_path: Путь к папке RakLite
            config_path: Путь к конфигурации
        """
        self.raklite_path = Path(raklite_path)
        self.config_path = Path(config_path)
        self.launcher_exe = self.raklite_path / "RakLaunch Lite.exe"
        self.client_exe = self.raklite_path / "RakSAMP Lite.exe"
        self.scripts_dir = self.raklite_path / "scripts"
        
        self.running_instances: Dict[int, subprocess.Popen] = {}
        self.instance_configs: Dict[int, Dict] = {}
        self.instance_id_counter = 0
        
        # Загружаем конфигурацию
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Загружает конфигурацию RakLite"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "max_instances": 10,
            "script_timeout": 300,
            "auto_restart": True
        }
    
    def _save_config(self):
        """Сохраняет конфигурацию"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def create_script(self, script_name: str, script_content: str) -> Path:
        """
        Создает Lua скрипт для RakLite
        
        Args:
            script_name: Имя скрипта
            script_content: Содержимое скрипта
        
        Returns:
            Путь к созданному скрипту
        """
        script_path = self.scripts_dir / script_name
        script_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def generate_register_script(self, username: str, password: str, 
                                email: str, script_name: str = None) -> Path:
        """
        Генерирует скрипт регистрации для RakLite
        
        Args:
            username: Имя пользователя
            password: Пароль
            email: Email
            script_name: Имя скрипта
        
        Returns:
            Путь к скрипту
        """
        if script_name is None:
            script_name = f"register_{username}.lua"
        
        script_content = f'''-- Скрипт регистрации для RakLite
-- Сгенерировано RackBot

local addon = require("libs.addon")
local events = require("libs.samp.events")

local username = "{username}"
local password = "{password}"
local email = "{email}"

function events.onInitGame()
    print("Игра инициализирована, начинаю регистрацию...")
    
    -- Ждем немного
    wait(2000)
    
    -- Отправляем команду регистрации
    sendInput("/register " .. password .. " " .. email)
    print("Отправлена команда регистрации")
end

function events.onShowDialog(dialogId, style, title, button1, button2, text)
    print("Диалог показан:", dialogId, title)
    
    -- Если это диалог регистрации
    if string.find(string.lower(title or ""), "регистр") or 
       string.find(string.lower(text or ""), "регистр") then
        print("Заполняю диалог регистрации...")
        -- Заполняем поля диалога
        sendDialogResponse(dialogId, 1, 0, password)
    end
end

function events.onServerMessage(color, text)
    print("Сообщение сервера:", text)
    
    local lower_text = string.lower(text or "")
    if string.find(lower_text, "успешно") or 
       string.find(lower_text, "зарегистрирован") then
        print("Регистрация успешна!")
        
        -- Сохраняем результат для Python бота
        local result = {{
            username = username,
            status = "success",
            timestamp = os.time()
        }}
        local file = io.open("raklite_results/register_" .. username .. ".json", "w")
        if file then
            file:write(json.encode(result))
            file:close()
        end
    elseif string.find(lower_text, "ошибка") or 
           string.find(lower_text, "уже") then
        print("Ошибка регистрации:", text)
        
        local result = {{
            username = username,
            status = "error",
            message = text,
            timestamp = os.time()
        }}
        local file = io.open("raklite_results/register_" .. username .. ".json", "w")
        if file then
            file:write(json.encode(result))
            file:close()
        end
    end
end
'''
        
        return self.create_script(script_name, script_content)
    
    def generate_login_script(self, username: str, password: str,
                             script_name: str = None) -> Path:
        """
        Генерирует скрипт авторизации для RakLite
        
        Args:
            username: Имя пользователя
            password: Пароль
            script_name: Имя скрипта
        
        Returns:
            Путь к скрипту
        """
        if script_name is None:
            script_name = f"login_{username}.lua"
        
        script_content = f'''-- Скрипт авторизации для RakLite
-- Сгенерировано RackBot

local addon = require("libs.addon")
local events = require("libs.samp.events")

local username = "{username}"
local password = "{password}"

function events.onInitGame()
    print("Игра инициализирована, начинаю авторизацию...")
    
    wait(2000)
    
    -- Отправляем команду входа
    sendInput("/login " .. password)
    print("Отправлена команда авторизации")
end

function events.onShowDialog(dialogId, style, title, button1, button2, text)
    print("Диалог показан:", dialogId, title)
    
    -- Если это диалог авторизации
    if string.find(string.lower(title or ""), "вход") or 
       string.find(string.lower(title or ""), "логин") or
       string.find(string.lower(text or ""), "пароль") then
        print("Заполняю диалог авторизации...")
        sendDialogResponse(dialogId, 1, 0, password)
    end
end

function events.onServerMessage(color, text)
    print("Сообщение сервера:", text)
    
    local lower_text = string.lower(text or "")
    if string.find(lower_text, "успешно") or 
       string.find(lower_text, "авторизован") or
       string.find(lower_text, "добро") then
        print("Авторизация успешна!")
        
        local result = {{
            username = username,
            status = "success",
            timestamp = os.time()
        }}
        local file = io.open("raklite_results/login_" .. username .. ".json", "w")
        if file then
            file:write(json.encode(result))
            file:close()
        end
    end
end
'''
        
        return self.create_script(script_name, script_content)
    
    def generate_farm_script(self, actions: List[str] = None,
                            script_name: str = "farm.lua") -> Path:
        """
        Генерирует скрипт прокачки для RakLite
        
        Args:
            actions: Список действий
            script_name: Имя скрипта
        
        Returns:
            Путь к скрипту
        """
        if actions is None:
            actions = ['move_forward', 'move_backward', 'jump', 'crouch']
        
        script_content = f'''-- Скрипт прокачки для RakLite
-- Сгенерировано RackBot

local addon = require("libs.addon")
local events = require("libs.samp.events")
local synchronization = require("libs.samp.synchronization")

function events.onInitGame()
    print("Начало прокачки опыта...")
end

function events.onPlayerSpawn()
    print("Игрок заспавнен, начинаю прокачку...")
    
    -- Основной цикл прокачки
    newTask(function()
        while true do
            -- Движение вперед
            -- Отправляем синхронизацию игрока
            wait(5000)  -- 5 секунд
            
            -- Пауза
            wait(20000)  -- 20 секунд
            
            -- Движение назад
            wait(5000)  -- 5 секунд
            
            -- Пауза
            wait(20000)  -- 20 секунд
        end
    end)
end

function events.onServerMessage(color, text)
    if string.find(string.lower(text or ""), "опыт") or 
       string.find(string.lower(text or ""), "exp") then
        print("Получен опыт:", text)
    end
end
'''
        
        return self.create_script(script_name, script_content)
    
    def launch_instance(self, server_ip: str, server_port: int, 
                       nickname: str, script_path: Optional[Path] = None,
                       proxy: Optional[Dict] = None) -> int:
        """
        Запускает экземпляр RakLite
        
        Args:
            server_ip: IP сервера
            server_port: Порт сервера
            nickname: Никнейм
            script_path: Путь к Lua скрипту (опционально)
            proxy: Настройки прокси (опционально)
        
        Returns:
            ID экземпляра
        """
        if len(self.running_instances) >= self.config.get('max_instances', 10):
            raise Exception("Достигнут максимум экземпляров")
        
        self.instance_id_counter += 1
        instance_id = self.instance_id_counter
        
        # Подготавливаем параметры запуска
        # RakLite обычно принимает параметры через командную строку или конфиг
        # Нужно уточнить формат запуска
        
        try:
            # Запускаем клиент
            # Формат может быть разным, это пример
            cmd = [
                str(self.client_exe),
                server_ip,
                str(server_port),
                nickname
            ]
            
            # Если есть прокси, нужно настроить (зависит от реализации RakLite)
            if proxy:
                # Настройка прокси через переменные окружения или параметры
                pass
            
            process = subprocess.Popen(
                cmd,
                cwd=str(self.raklite_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running_instances[instance_id] = process
            self.instance_configs[instance_id] = {
                'server_ip': server_ip,
                'server_port': server_port,
                'nickname': nickname,
                'script_path': str(script_path) if script_path else None,
                'proxy': proxy,
                'start_time': time.time()
            }
            
            return instance_id
            
        except Exception as e:
            raise Exception(f"Ошибка запуска экземпляра: {e}")
    
    def stop_instance(self, instance_id: int) -> bool:
        """
        Останавливает экземпляр RakLite
        
        Args:
            instance_id: ID экземпляра
        
        Returns:
            True если успешно
        """
        if instance_id not in self.running_instances:
            return False
        
        try:
            process = self.running_instances[instance_id]
            process.terminate()
            process.wait(timeout=5)
            
            del self.running_instances[instance_id]
            if instance_id in self.instance_configs:
                del self.instance_configs[instance_id]
            
            return True
        except Exception:
            try:
                process.kill()
            except Exception:
                pass
            return False
    
    def get_instance_status(self, instance_id: int) -> Optional[Dict]:
        """
        Получает статус экземпляра
        
        Args:
            instance_id: ID экземпляра
        
        Returns:
            Словарь со статусом или None
        """
        if instance_id not in self.running_instances:
            return None
        
        process = self.running_instances[instance_id]
        config = self.instance_configs.get(instance_id, {})
        
        return {
            'instance_id': instance_id,
            'running': process.poll() is None,
            'return_code': process.poll(),
            'uptime': time.time() - config.get('start_time', 0),
            'config': config
        }
    
    def get_all_instances(self) -> List[Dict]:
        """Возвращает статус всех экземпляров"""
        return [self.get_instance_status(id) for id in self.running_instances.keys()]
    
    def stop_all(self):
        """Останавливает все экземпляры"""
        for instance_id in list(self.running_instances.keys()):
            self.stop_instance(instance_id)

