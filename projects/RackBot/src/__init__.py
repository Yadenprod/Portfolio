"""
RackBot - Headless бот для автоматизации аккаунтов на Radmir RP
"""

__version__ = "1.0.0"
__author__ = "RackBot Team"

from src.bot import RackBot
from src.account_manager import AccountManager
from src.proxy_manager import ProxyManager
from src.mac_changer import MACChanger
from src.samp_client import SAMPClient
from src.samp_protocol import SAMPProtocol, SAMPacketID
from src.logger import BotLogger
from src.moonloader_integration import MoonloaderIntegration
from src.web_api import RadmirWebAPI

__all__ = [
    'RackBot',
    'AccountManager',
    'ProxyManager',
    'MACChanger',
    'SAMPClient',
    'SAMPProtocol',
    'SAMPacketID',
    'BotLogger',
    'MoonloaderIntegration',
    'RadmirWebAPI'
]
