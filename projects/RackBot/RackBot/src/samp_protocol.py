"""
Модуль для работы с протоколом SAMP
Реализация на основе захваченных пакетов
"""
import struct
import socket
from typing import Optional, Dict, Tuple
from enum import IntEnum


class SAMPacketID(IntEnum):
    """ID пакетов SAMP на основе логов"""
    # Основные пакеты из логов
    PLAYER_SYNC = 203      # Синхронизация игрока (часто)
    VEHICLE_SYNC = 200    # Синхронизация транспорта
    BULLET_SYNC = 207     # Синхронизация выстрелов
    AIM_SYNC = 205        # Синхронизация прицела
    SPECTATOR_SYNC = 211  # Синхронизация наблюдателя
    STATS_UPDATE = 212    # Обновление статистики (очень часто)
    WEAPONS_UPDATE = 215  # Обновление оружия
    
    # Команды и чат
    CHAT_MESSAGE = 101    # Сообщение в чат
    COMMAND = 102         # Команда
    
    # Диалоги
    DIALOG_RESPONSE = 63  # Ответ на диалог
    DIALOG_SHOW = 64      # Показать диалог
    
    # Подключение
    CONNECTION_REQUEST = 1
    CONNECTION_ACCEPTED = 2
    CONNECTION_REJECTED = 3


class SAMPProtocol:
    """Класс для работы с протоколом SAMP"""
    
    def __init__(self):
        self.raknet_header = b'SAMP'  # Заголовок RakNet для SAMP
    
    def build_packet(self, packet_id: int, data: bytes = b'') -> bytes:
        """
        Строит пакет SAMP
        
        Args:
            packet_id: ID пакета
            data: Данные пакета
        
        Returns:
            Байты пакета
        """
        # Формат SAMP пакета через RakNet:
        # [RakNet Header: 4 bytes] + [IP: 4 bytes] + [Port: 2 bytes] + [Packet ID: 1 byte] + [Data: N bytes]
        packet = struct.pack('B', packet_id)  # ID пакета
        packet += data  # Данные
        return packet
    
    def build_chat_message(self, message: str) -> bytes:
        """
        Строит пакет сообщения в чат
        
        Args:
            message: Текст сообщения
        
        Returns:
            Байты пакета
        """
        # Формат: [Message Length: 1 byte] + [Message: N bytes]
        message_bytes = message.encode('cp1251')  # SAMP использует CP1251
        packet = struct.pack('B', len(message_bytes))
        packet += message_bytes
        return self.build_packet(SAMPacketID.CHAT_MESSAGE, packet)
    
    def build_command(self, command: str) -> bytes:
        """
        Строит пакет команды
        
        Args:
            command: Команда (например "/register password email")
        
        Returns:
            Байты пакета
        """
        # Команды отправляются как сообщения в чат
        return self.build_chat_message(command)
    
    def build_dialog_response(self, dialog_id: int, button_id: int, 
                             list_item: int = 0, input_text: str = "") -> bytes:
        """
        Строит пакет ответа на диалог
        
        Args:
            dialog_id: ID диалога
            button_id: ID кнопки (0 или 1)
            list_item: Выбранный элемент списка
            input_text: Введенный текст
        
        Returns:
            Байты пакета
        """
        # Формат: [Dialog ID: 2 bytes] + [Button ID: 1 byte] + 
        #         [List Item: 2 bytes] + [Input Length: 2 bytes] + [Input: N bytes]
        input_bytes = input_text.encode('cp1251')
        packet = struct.pack('<H', dialog_id)  # Little-endian
        packet += struct.pack('B', button_id)
        packet += struct.pack('<H', list_item)
        packet += struct.pack('<H', len(input_bytes))
        packet += input_bytes
        return self.build_packet(SAMPacketID.DIALOG_RESPONSE, packet)
    
    def build_player_sync(self, position: Tuple[float, float, float],
                         rotation: float, health: float = 100.0,
                         armor: float = 0.0, weapon: int = 0) -> bytes:
        """
        Строит пакет синхронизации игрока (ID 203)
        
        Args:
            position: Позиция (x, y, z)
            rotation: Поворот
            health: Здоровье
            armor: Броня
            weapon: ID оружия
        
        Returns:
            Байты пакета
        """
        # Упрощенная версия синхронизации игрока
        # Полный формат очень сложный, это базовая версия
        packet = struct.pack('<fff', *position)  # Позиция
        packet += struct.pack('<f', rotation)     # Поворот
        packet += struct.pack('<f', health)       # Здоровье
        packet += struct.pack('<f', armor)        # Броня
        packet += struct.pack('<H', weapon)       # Оружие
        return self.build_packet(SAMPacketID.PLAYER_SYNC, packet)
    
    def build_stats_update(self, money: int = 0, drunk_level: int = 0) -> bytes:
        """
        Строит пакет обновления статистики (ID 212)
        Часто отправляется для поддержания соединения
        
        Args:
            money: Деньги
            drunk_level: Уровень опьянения
        
        Returns:
            Байты пакета
        """
        packet = struct.pack('<I', money)        # Деньги (4 байта)
        packet += struct.pack('<I', drunk_level) # Уровень опьянения
        return self.build_packet(SAMPacketID.STATS_UPDATE, packet)
    
    def parse_packet(self, data: bytes) -> Optional[Dict]:
        """
        Парсит входящий пакет
        
        Args:
            data: Байты пакета
        
        Returns:
            Словарь с данными пакета или None
        """
        if len(data) < 1:
            return None
        
        packet_id = data[0]
        packet_data = data[1:] if len(data) > 1 else b''
        
        result = {
            'id': packet_id,
            'data': packet_data,
            'size': len(data)
        }
        
        # Парсим специфичные пакеты
        if packet_id == SAMPacketID.CHAT_MESSAGE:
            if len(packet_data) > 0:
                msg_len = packet_data[0]
                if len(packet_data) > msg_len:
                    result['message'] = packet_data[1:1+msg_len].decode('cp1251', errors='ignore')
        
        elif packet_id == SAMPacketID.DIALOG_SHOW:
            # Парсим диалог
            if len(packet_data) >= 2:
                result['dialog_id'] = struct.unpack('<H', packet_data[0:2])[0]
        
        return result
    
    def build_connection_request(self, nickname: str, server_password: str = "") -> bytes:
        """
        Строит запрос на подключение
        
        Args:
            nickname: Никнейм игрока
            server_password: Пароль сервера (если требуется)
        
        Returns:
            Байты запроса
        """
        # Формат: [Version: 1 byte] + [Nickname: 20 bytes] + 
        #         [Password: 20 bytes] + [Client Version: 4 bytes]
        packet = struct.pack('B', 4)  # Версия протокола
        
        # Никнейм (до 20 символов, дополняется нулями)
        nickname_bytes = nickname.encode('cp1251')[:20]
        packet += nickname_bytes.ljust(20, b'\x00')
        
        # Пароль сервера (до 20 символов)
        password_bytes = server_password.encode('cp1251')[:20]
        packet += password_bytes.ljust(20, b'\x00')
        
        # Версия клиента (обычно 0x03E8 = 1000)
        packet += struct.pack('<I', 1000)
        
        return self.build_packet(SAMPacketID.CONNECTION_REQUEST, packet)

