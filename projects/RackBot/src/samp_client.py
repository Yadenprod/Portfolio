"""
Модуль для работы с SAMP сервером (headless клиент)
"""
import socket
import struct
import time
import random
import threading
from typing import Optional, Dict, Callable, Tuple
from enum import Enum
from src.samp_protocol import SAMPProtocol, SAMPacketID


class ConnectionState(Enum):
    """Состояния подключения"""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    AUTHENTICATING = "authenticating"
    AUTHENTICATED = "authenticated"
    IN_GAME = "in_game"


class SAMPClient:
    """Headless клиент для подключения к SAMP серверу"""
    
    def __init__(self, server_ip: str, server_port: int, proxy: Optional[Dict] = None):
        """
        Инициализация клиента
        
        Args:
            server_ip: IP адрес сервера
            server_port: Порт сервера
            proxy: Настройки прокси (опционально)
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.proxy = proxy
        
        self.socket = None
        self.state = ConnectionState.DISCONNECTED
        self.player_id = None
        self.server_info = {}
        self.protocol = SAMPProtocol()
        
        # Поток для приема пакетов
        self.receive_thread = None
        self.running = False
        
        # Позиция игрока (для синхронизации)
        self.position = (0.0, 0.0, 0.0)
        self.rotation = 0.0
        
        # Callbacks
        self.on_connect: Optional[Callable] = None
        self.on_disconnect: Optional[Callable] = None
        self.on_message: Optional[Callable] = None
        self.on_dialog: Optional[Callable] = None
    
    def connect(self, timeout: int = 10) -> bool:
        """
        Подключается к серверу
        
        Args:
            timeout: Таймаут подключения
        
        Returns:
            True если успешно
        """
        try:
            self.state = ConnectionState.CONNECTING
            
            # Создаем сокет
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(timeout)
            
            # Если используется прокси, нужно настроить подключение через него
            # Для SAMP обычно используется прямое UDP подключение
            # Прокси нужно настраивать на уровне системы или через VPN
            
            # Отправляем запрос информации о сервере
            query = self._build_server_query()
            self.socket.sendto(query, (self.server_ip, self.server_port))
            
            # Получаем ответ
            response, addr = self.socket.recvfrom(4096)
            
            if self._parse_server_response(response):
                self.state = ConnectionState.CONNECTED
                # Запускаем поток приема пакетов
                self._start_receive_thread()
                if self.on_connect:
                    self.on_connect()
                return True
            
            return False
            
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            self.state = ConnectionState.DISCONNECTED
            return False
    
    def _build_server_query(self) -> bytes:
        """Строит запрос к серверу"""
        # SAMP протокол использует специальный формат запросов
        # 'SAMP' + IP (4 bytes) + Port (2 bytes) + Type (1 byte)
        query = b'SAMP'
        query += socket.inet_aton(self.server_ip)
        query += struct.pack('H', self.server_port)
        query += b'i'  # 'i' = информация о сервере
        return query
    
    def _parse_server_response(self, data: bytes) -> bool:
        """Парсит ответ сервера"""
        try:
            if not data.startswith(b'SAMP'):
                return False
            
            # Парсим ответ сервера
            # Формат зависит от типа запроса
            # Здесь упрощенная версия
            return True
        except Exception:
            return False
    
    def register_account(self, username: str, password: str, email: str) -> bool:
        """
        Регистрирует аккаунт на сервере
        
        Args:
            username: Имя пользователя
            password: Пароль
            email: Email
        
        Returns:
            True если успешно
        """
        try:
            self.state = ConnectionState.AUTHENTICATING
            
            # Отправляем команду регистрации
            # Формат может быть разным, пробуем стандартные варианты
            register_commands = [
                f"/register {password} {email}",
                f"/reg {password} {email}",
                f"/register {username} {password} {email}"
            ]
            
            # Пробуем первый вариант (наиболее распространенный)
            if self.send_command(register_commands[0]):
                # Ждем ответа сервера
                time.sleep(2)
                
                # Если есть диалог регистрации, обработаем его
                # (нужно будет обработать через callback on_dialog)
                
                self.state = ConnectionState.AUTHENTICATED
                return True
            
            return False
            
        except Exception as e:
            print(f"Ошибка регистрации: {e}")
            self.state = ConnectionState.DISCONNECTED
            return False
    
    def login(self, username: str, password: str) -> bool:
        """
        Авторизуется на сервере
        
        Args:
            username: Имя пользователя
            password: Пароль
        
        Returns:
            True если успешно
        """
        try:
            self.state = ConnectionState.AUTHENTICATING
            
            # Отправляем команду входа
            login_commands = [
                f"/login {password}",
                f"/login {username} {password}",
                f"/l {password}"
            ]
            
            if self.send_command(login_commands[0]):
                # Ждем ответа
                time.sleep(2)
                
                self.state = ConnectionState.AUTHENTICATED
                return True
            
            return False
            
        except Exception as e:
            print(f"Ошибка авторизации: {e}")
            self.state = ConnectionState.DISCONNECTED
            return False
    
    def send_command(self, command: str) -> bool:
        """
        Отправляет команду на сервер
        
        Args:
            command: Команда (например "/register password email")
        
        Returns:
            True если отправлено успешно
        """
        if not self.socket or not self.is_connected():
            return False
        
        try:
            # Строим пакет команды
            packet = self.protocol.build_command(command)
            
            # Отправляем через RakNet обертку
            raknet_packet = self._wrap_raknet_packet(packet)
            self.socket.sendto(raknet_packet, (self.server_ip, self.server_port))
            
            return True
        except Exception as e:
            print(f"Ошибка отправки команды: {e}")
            return False
    
    def send_dialog_response(self, dialog_id: int, button_id: int, 
                            list_item: int = 0, input_text: str = "") -> bool:
        """
        Отправляет ответ на диалог
        
        Args:
            dialog_id: ID диалога
            button_id: ID кнопки (0 или 1)
            list_item: Выбранный элемент
            input_text: Введенный текст
        
        Returns:
            True если отправлено успешно
        """
        if not self.socket or not self.is_connected():
            return False
        
        try:
            packet = self.protocol.build_dialog_response(
                dialog_id, button_id, list_item, input_text
            )
            raknet_packet = self._wrap_raknet_packet(packet)
            self.socket.sendto(raknet_packet, (self.server_ip, self.server_port))
            return True
        except Exception as e:
            print(f"Ошибка отправки ответа диалога: {e}")
            return False
    
    def _wrap_raknet_packet(self, data: bytes) -> bytes:
        """
        Оборачивает SAMP пакет в RakNet формат
        
        Args:
            data: Данные SAMP пакета
        
        Returns:
            Байты RakNet пакета
        """
        # Упрощенная обертка RakNet
        # В реальности RakNet имеет сложный протокол с сжатием и т.д.
        # Это базовая версия для работы
        raknet_header = b'SAMP'
        raknet_header += socket.inet_aton(self.server_ip)
        raknet_header += struct.pack('H', self.server_port)
        return raknet_header + data
    
    def _start_receive_thread(self):
        """Запускает поток для приема пакетов"""
        if self.receive_thread and self.receive_thread.is_alive():
            return
        
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self.receive_thread.start()
    
    def _receive_loop(self):
        """Цикл приема пакетов"""
        while self.running and self.socket:
            try:
                data, addr = self.socket.recvfrom(4096)
                self._handle_packet(data)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Ошибка приема пакета: {e}")
                break
    
    def _handle_packet(self, data: bytes):
        """Обрабатывает входящий пакет"""
        try:
            # Убираем RakNet заголовок
            if data.startswith(b'SAMP'):
                # Пропускаем заголовок (4 + 4 + 2 = 10 байт)
                samp_data = data[10:]
            else:
                samp_data = data
            
            # Парсим пакет
            packet = self.protocol.parse_packet(samp_data)
            if not packet:
                return
            
            packet_id = packet['id']
            
            # Обрабатываем специфичные пакеты
            if packet_id == SAMPacketID.CHAT_MESSAGE:
                if self.on_message and 'message' in packet:
                    self.on_message(packet['message'])
            
            elif packet_id == SAMPacketID.DIALOG_SHOW:
                if self.on_dialog and 'dialog_id' in packet:
                    self.on_dialog(packet['dialog_id'], packet.get('data', b''))
            
            elif packet_id == SAMPacketID.CONNECTION_ACCEPTED:
                self.state = ConnectionState.CONNECTED
                if self.on_connect:
                    self.on_connect()
            
        except Exception as e:
            print(f"Ошибка обработки пакета: {e}")
    
    def send_keepalive(self):
        """Отправляет keepalive пакеты для поддержания соединения"""
        if not self.socket or not self.is_connected():
            return
        
        try:
            # Отправляем пакет обновления статистики (ID 212) - часто используется как keepalive
            packet = self.protocol.build_stats_update()
            raknet_packet = self._wrap_raknet_packet(packet)
            self.socket.sendto(raknet_packet, (self.server_ip, self.server_port))
        except Exception:
            pass
    
    def farm_experience(self, actions: list = None):
        """
        Автоматически качает опыт
        
        Args:
            actions: Список действий для прокачки
        """
        if not actions:
            # Дефолтные действия для прокачки
            actions = [
                'move_forward',
                'move_backward',
                'turn_left',
                'turn_right',
                'jump',
                'crouch'
            ]
        
        self.state = ConnectionState.IN_GAME
        
        # Выполняем действия для получения опыта
        for action in actions:
            # Отправляем пакет синхронизации игрока (ID 203)
            # Это имитирует движение/действия
            packet = self.protocol.build_player_sync(
                position=self.position,
                rotation=self.rotation
            )
            
            try:
                raknet_packet = self._wrap_raknet_packet(packet)
                self.socket.sendto(raknet_packet, (self.server_ip, self.server_port))
            except Exception:
                pass
            
            # Обновляем позицию для следующего пакета
            self._update_position_for_action(action)
            
            # Отправляем keepalive
            self.send_keepalive()
            
            time.sleep(random.uniform(0.5, 2.0))
    
    def _update_position_for_action(self, action: str):
        """Обновляет позицию игрока для действия"""
        x, y, z = self.position
        
        if action == 'move_forward':
            # Движение вперед
            x += 0.1
        elif action == 'move_backward':
            x -= 0.1
        elif action == 'turn_left':
            self.rotation -= 5.0
        elif action == 'turn_right':
            self.rotation += 5.0
        elif action == 'jump':
            z += 0.5
        elif action == 'crouch':
            z -= 0.2
        
        self.position = (x, y, z)
    
    def disconnect(self):
        """Отключается от сервера"""
        self.running = False
        
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join(timeout=1)
        
        if self.socket:
            self.socket.close()
            self.socket = None
        
        self.state = ConnectionState.DISCONNECTED
        if self.on_disconnect:
            self.on_disconnect()
    
    def is_connected(self) -> bool:
        """Проверяет подключение"""
        return self.state in [
            ConnectionState.CONNECTED,
            ConnectionState.AUTHENTICATED,
            ConnectionState.IN_GAME
        ]

