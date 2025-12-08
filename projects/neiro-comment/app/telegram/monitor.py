"""
Мониторинг каналов Telegram
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from app.telegram.client import TelegramClient
from app.database.connection import SessionLocal
from app.database.models import Channel, Post

logger = logging.getLogger(__name__)


class ChannelMonitor:
    """Монитор каналов для отслеживания новых постов"""
    
    def __init__(self):
        self.client = TelegramClient()
        self.is_running = False
        
    async def start_monitoring(self):
        """Запуск мониторинга каналов"""
        try:
            await self.client.initialize()
            self.is_running = True
            
            logger.info("Мониторинг каналов запущен")
            
            while self.is_running:
                try:
                    # Получаем активные каналы
                    active_channels = await self._get_active_channels()
                    
                    for channel in active_channels:
                        try:
                            # Получаем новые посты
                            posts = await self.client.get_recent_posts(channel.channel_id)
                            
                            if posts:
                                # Сохраняем посты в БД
                                await self.client.save_posts_to_database(posts)
                                
                                # Обрабатываем посты для комментирования
                                await self.client.process_pending_posts()
                                
                        except Exception as e:
                            logger.error(f"Ошибка обработки канала {channel.username}: {e}")
                    
                    # Пауза между проверками (5 минут)
                    await asyncio.sleep(300)
                    
                except Exception as e:
                    logger.error(f"Ошибка в цикле мониторинга: {e}")
                    await asyncio.sleep(60)  # Пауза при ошибке
                    
        except Exception as e:
            logger.error(f"Критическая ошибка мониторинга: {e}")
            self.is_running = False
    
    async def stop_monitoring(self):
        """Остановка мониторинга"""
        self.is_running = False
        logger.info("Мониторинг каналов остановлен")
    
    async def _get_active_channels(self) -> List[Channel]:
        """Получение активных каналов"""
        try:
            db = SessionLocal()
            
            channels = db.query(Channel).filter(
                Channel.is_active == True,
                Channel.comment_enabled == True
            ).all()
            
            return channels
            
        except Exception as e:
            logger.error(f"Ошибка получения активных каналов: {e}")
            return []
        finally:
            db.close()
    
    async def add_channel(self, channel_username: str) -> bool:
        """Добавление нового канала для мониторинга"""
        try:
            # Получаем информацию о канале
            channel_info = await self.client.get_channel_info(channel_username)
            
            if not channel_info:
                logger.error(f"Не удалось получить информацию о канале {channel_username}")
                return False
            
            # Добавляем канал в БД
            success = await self.client.add_channel_to_database(channel_info)
            
            if success:
                logger.info(f"Канал {channel_username} добавлен для мониторинга")
                return True
            else:
                logger.error(f"Не удалось добавить канал {channel_username} в БД")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка добавления канала {channel_username}: {e}")
            return False
    
    async def remove_channel(self, channel_id: str) -> bool:
        """Удаление канала из мониторинга"""
        try:
            db = SessionLocal()
            
            channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
            
            if channel:
                channel.is_active = False
                db.commit()
                logger.info(f"Канал {channel.username} удален из мониторинга")
                return True
            else:
                logger.warning(f"Канал {channel_id} не найден")
                return False
                
        except Exception as e:
            logger.error(f"Ошибка удаления канала: {e}")
            return False
        finally:
            db.close()
    
    async def update_channel_settings(self, channel_id: str, settings: dict) -> bool:
        """Обновление настроек канала"""
        try:
            db = SessionLocal()
            
            channel = db.query(Channel).filter(Channel.channel_id == channel_id).first()
            
            if not channel:
                logger.warning(f"Канал {channel_id} не найден")
                return False
            
            # Обновляем настройки
            if "comment_enabled" in settings:
                channel.comment_enabled = settings["comment_enabled"]
            if "comment_frequency" in settings:
                channel.comment_frequency = settings["comment_frequency"]
            
            channel.updated_at = datetime.now()
            db.commit()
            
            logger.info(f"Настройки канала {channel.username} обновлены")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обновления настроек канала: {e}")
            return False
        finally:
            db.close()


# Глобальный экземпляр монитора
monitor = ChannelMonitor()


async def start_monitoring():
    """Запуск мониторинга (вызывается из main.py)"""
    await monitor.start_monitoring()


async def stop_monitoring():
    """Остановка мониторинга"""
    await monitor.stop_monitoring()


async def add_channel(channel_username: str) -> bool:
    """Добавление канала для мониторинга"""
    return await monitor.add_channel(channel_username)


async def remove_channel(channel_id: str) -> bool:
    """Удаление канала из мониторинга"""
    return await monitor.remove_channel(channel_id)


async def update_channel_settings(channel_id: str, settings: dict) -> bool:
    """Обновление настроек канала"""
    return await monitor.update_channel_settings(channel_id, settings)
