"""
Модуль для подмены MAC адреса
"""
import subprocess
import random
import re
from typing import Optional, List
import platform


class MACChanger:
    """Класс для изменения MAC адреса сетевого интерфейса"""
    
    def __init__(self):
        self.system = platform.system()
    
    def generate_random_mac(self) -> str:
        """
        Генерирует случайный MAC адрес
        
        Returns:
            MAC адрес в формате XX:XX:XX:XX:XX:XX
        """
        # Первые 3 байта - OUI (можно использовать локально администрируемый адрес)
        # Локально администрируемый адрес имеет второй бит первого байта = 1
        # Пример: x2, x6, xA, xE (где x - любая hex цифра)
        mac = [
            0x02,  # Локально администрируемый
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)
        ]
        return ':'.join(f'{b:02x}' for b in mac)
    
    def get_network_interfaces(self) -> List[str]:
        """
        Получает список сетевых интерфейсов
        
        Returns:
            Список имен интерфейсов
        """
        if self.system == 'Windows':
            return self._get_windows_interfaces()
        elif self.system == 'Linux':
            return self._get_linux_interfaces()
        else:
            return []
    
    def _get_windows_interfaces(self) -> List[str]:
        """Получает интерфейсы на Windows"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 'Get-NetAdapter | Select-Object -ExpandProperty Name'],
                capture_output=True,
                text=True
            )
            interfaces = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return interfaces
        except Exception as e:
            print(f"Ошибка получения интерфейсов: {e}")
            return []
    
    def _get_linux_interfaces(self) -> List[str]:
        """Получает интерфейсы на Linux"""
        try:
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            interfaces = re.findall(r'\d+: (\w+):', result.stdout)
            return interfaces
        except Exception as e:
            print(f"Ошибка получения интерфейсов: {e}")
            return []
    
    def get_current_mac(self, interface: str) -> Optional[str]:
        """
        Получает текущий MAC адрес интерфейса
        
        Args:
            interface: Имя интерфейса
        
        Returns:
            MAC адрес или None
        """
        if self.system == 'Windows':
            return self._get_windows_mac(interface)
        elif self.system == 'Linux':
            return self._get_linux_mac(interface)
        return None
    
    def _get_windows_mac(self, interface: str) -> Optional[str]:
        """Получает MAC на Windows"""
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 f'Get-NetAdapter -Name "{interface}" | Select-Object -ExpandProperty MacAddress'],
                capture_output=True,
                text=True
            )
            mac = result.stdout.strip()
            return mac if mac else None
        except Exception as e:
            print(f"Ошибка получения MAC: {e}")
            return None
    
    def _get_linux_mac(self, interface: str) -> Optional[str]:
        """Получает MAC на Linux"""
        try:
            result = subprocess.run(
                ['cat', f'/sys/class/net/{interface}/address'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() if result.stdout.strip() else None
        except Exception as e:
            print(f"Ошибка получения MAC: {e}")
            return None
    
    def change_mac(self, interface: str, new_mac: Optional[str] = None) -> bool:
        """
        Изменяет MAC адрес интерфейса
        
        Args:
            interface: Имя интерфейса
            new_mac: Новый MAC адрес (если None - генерируется случайный)
        
        Returns:
            True если успешно
        """
        if new_mac is None:
            new_mac = self.generate_random_mac()
        
        if self.system == 'Windows':
            return self._change_windows_mac(interface, new_mac)
        elif self.system == 'Linux':
            return self._change_linux_mac(interface, new_mac)
        else:
            print(f"Неподдерживаемая система: {self.system}")
            return False
    
    def _change_windows_mac(self, interface: str, new_mac: str) -> bool:
        """Изменяет MAC на Windows (требует прав администратора)"""
        try:
            # Отключаем интерфейс
            subprocess.run(
                ['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=disable'],
                check=True,
                capture_output=True
            )
            
            # Изменяем MAC
            subprocess.run(
                ['powershell', '-Command',
                 f'Set-NetAdapter -Name "{interface}" -MacAddress "{new_mac}"'],
                check=True,
                capture_output=True
            )
            
            # Включаем интерфейс
            subprocess.run(
                ['netsh', 'interface', 'set', 'interface', f'name="{interface}"', 'admin=enable'],
                check=True,
                capture_output=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Ошибка изменения MAC (требуются права администратора): {e}")
            return False
        except Exception as e:
            print(f"Ошибка изменения MAC: {e}")
            return False
    
    def _change_linux_mac(self, interface: str, new_mac: str) -> bool:
        """Изменяет MAC на Linux (требует прав root)"""
        try:
            # Отключаем интерфейс
            subprocess.run(['ip', 'link', 'set', interface, 'down'], check=True)
            
            # Изменяем MAC
            subprocess.run(['ip', 'link', 'set', interface, 'address', new_mac], check=True)
            
            # Включаем интерфейс
            subprocess.run(['ip', 'link', 'set', interface, 'up'], check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Ошибка изменения MAC (требуются права root): {e}")
            return False
        except Exception as e:
            print(f"Ошибка изменения MAC: {e}")
            return False

