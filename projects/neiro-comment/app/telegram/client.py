"""
Telegram клиент для работы с API
"""
import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.error import TelegramError

from app.config import settings
from app.database.connection import SessionLocal
from app.database.models import Channel, Post, Comment
from app.ai.generator import CommentGenerator

logger = logging.getLogger(__name__)


class TelegramClient:
    """Клиент для работы с Telegram API"""
    
    def __init__(self):
        self.bot = Bot(token=settings.telegram_bot_token)
        self.application = None
        self.comment_generator = CommentGenerator()
        
    async def initialize(self):
        """Инициализация клиента"""
        try:
            self.application = Application.builder().token(settings.telegram_bot_token).build()
            await self.application.initialize()
            logger.info("Telegram клиент инициализирован")
        except Exception as e:
            logger.error(f"Ошибка инициализации Telegram клиента: {e}")
            raise
    
    async def get_channel_info(self, channel_username: str) -> Optional[Dict[str, Any]]:
        """Получение информации о канале"""
        try:
            # Удаляем @ если есть
            if channel_username.startswith('@'):
                channel_username = channel_username[1:]
            
            # Получаем информацию о канале
            chat = await self.bot.get_chat(f"@{channel_username}")
            
            return {
                "id": str(chat.id),
                "username": channel_username,
                "title": chat.title,
                "description": chat.description,
                "type": chat.type
            }
        except TelegramError as e:
            logger.error(f"Ошибка получения информации о канале {channel_username}: {e}")
            return None
    
    async def get_recent_posts(self, channel_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Получение последних постов канала"""
        try:
            # Получаем последние сообщения
            updates = await self.bot.get_updates(limit=limit)
            posts = []
            
            for update in updates:
                if update.channel_post and str(update.channel_post.chat.id) == channel_id:
                    post = {
                        "id": str(update.channel_post.message_id),
                        "content": update.channel_post.text or update.channel_post.caption or "",
                        "media_type": self._get_media_type(update.channel_post),
                        "media_url": self._get_media_url(update.channel_post),
                        "published_at": datetime.fromtimestamp(update.channel_post.date),
                        "channel_id": channel_id
                    }
                    posts.append(post)
            
            return posts
        except TelegramError as e:
            logger.error(f"Ошибка получения постов канала {channel_id}: {e}")
            return []
    
    async def send_comment(self, channel_id: str, post_id: str, comment_text: str) -> Optional[str]:
        """Отправка комментария к посту"""
        try:
            # Отправляем комментарий
            message = await self.bot.send_message(
                chat_id=channel_id,
                text=comment_text,
                reply_to_message_id=int(post_id)
            )
            
            logger.info(f"Комментарий отправлен: {message.message_id}")
            return str(message.message_id)
            
        except TelegramError as e:
            logger.error(f"Ошибка отправки комментария: {e}")
            return None
    
    def _get_media_type(self, message) -> Optional[str]:
        """Определение типа медиа"""
        if message.photo:
            return "photo"
        elif message.video:
            return "video"
        elif message.document:
            return "document"
        elif message.audio:
            return "audio"
        elif message.voice:
            return "voice"
        elif message.sticker:
            return "sticker"
        else:
            return "text"
    
    def _get_media_url(self, message) -> Optional[str]:
        """Получение URL медиа"""
        if message.photo:
            return message.photo[-1].file_id
        elif message.video:
            return message.video.file_id
        elif message.document:
            return message.document.file_id
        return None
    
    async def add_channel_to_database(self, channel_data: Dict[str, Any]) -> bool:
        """Добавление канала в базу данных"""
        try:
            db = SessionLocal()
            
            # Проверяем, существует ли канал
            existing_channel = db.query(Channel).filter(
                Channel.channel_id == channel_data["id"]
            ).first()
            
            if existing_channel:
                logger.info(f"Канал {channel_data['username']} уже существует")
                return True
            
            # Создаем новый канал
            channel = Channel(
                channel_id=channel_data["id"],
                username=channel_data["username"],
                title=channel_data["title"],
                description=channel_data.get("description", ""),
                is_active=True,
                comment_enabled=True
            )
            
            db.add(channel)
            db.commit()
            
            logger.info(f"Канал {channel_data['username']} добавлен в базу данных")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка добавления канала в БД: {e}")
            return False
        finally:
            db.close()
    
    async def save_posts_to_database(self, posts: List[Dict[str, Any]]) -> bool:
        """Сохранение постов в базу данных"""
        try:
            db = SessionLocal()
            
            for post_data in posts:
                # Проверяем, существует ли пост
                existing_post = db.query(Post).filter(
                    Post.post_id == post_data["id"],
                    Post.channel_id == post_data["channel_id"]
                ).first()
                
                if existing_post:
                    continue
                
                # Создаем новый пост
                post = Post(
                    post_id=post_data["id"],
                    channel_id=post_data["channel_id"],
                    content=post_data["content"],
                    media_type=post_data.get("media_type"),
                    media_url=post_data.get("media_url"),
                    published_at=post_data["published_at"]
                )
                
                db.add(post)
            
            db.commit()
            logger.info(f"Сохранено {len(posts)} постов в БД")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения постов в БД: {e}")
            return False
        finally:
            db.close()
    
    async def get_pending_posts(self) -> List[Post]:
        """Получение постов, ожидающих комментариев"""
        try:
            db = SessionLocal()
            
            # Получаем активные каналы с включенными комментариями
            active_channels = db.query(Channel).filter(
                Channel.is_active == True,
                Channel.comment_enabled == True
            ).all()
            
            if not active_channels:
                return []
            
            channel_ids = [ch.channel_id for ch in active_channels]
            
            # Получаем посты без комментариев
            posts = db.query(Post).filter(
                Post.channel_id.in_(channel_ids),
                Post.is_commented == False
            ).order_by(Post.published_at.desc()).limit(10).all()
            
            return posts
            
        except Exception as e:
            logger.error(f"Ошибка получения постов: {e}")
            return []
        finally:
            db.close()
    
    async def process_pending_posts(self):
        """Обработка постов, ожидающих комментариев"""
        try:
            posts = await self.get_pending_posts()
            
            for post in posts:
                # Проверяем rate limiting
                if not await self._check_rate_limit(post.channel_id):
                    continue
                
                # Генерируем комментарий
                comment_text = await self.comment_generator.generate_comment(
                    post.content or "",
                    post.media_type or "text"
                )
                
                if not comment_text:
                    logger.warning(f"Не удалось сгенерировать комментарий для поста {post.post_id}")
                    continue
                
                # Отправляем комментарий
                comment_id = await self.send_comment(
                    post.channel_id,
                    post.post_id,
                    comment_text
                )
                
                if comment_id:
                    # Сохраняем комментарий в БД
                    await self._save_comment(post, comment_text, comment_id)
                    
                    # Обновляем статус поста
                    await self._update_post_status(post.post_id, True, comment_id)
                    
                    logger.info(f"Комментарий отправлен для поста {post.post_id}")
                else:
                    logger.error(f"Не удалось отправить комментарий для поста {post.post_id}")
                
                # Задержка между комментариями
                await asyncio.sleep(settings.comment_delay_min)
                
        except Exception as e:
            logger.error(f"Ошибка обработки постов: {e}")
    
    async def _check_rate_limit(self, channel_id: str) -> bool:
        """Проверка лимитов отправки комментариев"""
        try:
            db = SessionLocal()
            
            # Проверяем количество комментариев за последний час
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_comments = db.query(Comment).filter(
                Comment.channel_id == channel_id,
                Comment.created_at >= one_hour_ago,
                Comment.status == "sent"
            ).count()
            
            if recent_comments >= settings.max_comments_per_hour:
                logger.warning(f"Превышен лимит комментариев для канала {channel_id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка проверки rate limit: {e}")
            return False
        finally:
            db.close()
    
    async def _save_comment(self, post: Post, comment_text: str, comment_id: str):
        """Сохранение комментария в БД"""
        try:
            db = SessionLocal()
            
            comment = Comment(
                comment_id=comment_id,
                channel_id=post.channel_id,
                post_id=post.post_id,
                content=comment_text,
                ai_generated=True,
                status="sent",
                sent_at=datetime.now()
            )
            
            db.add(comment)
            db.commit()
            
        except Exception as e:
            logger.error(f"Ошибка сохранения комментария: {e}")
        finally:
            db.close()
    
    async def _update_post_status(self, post_id: str, is_commented: bool, comment_id: str = None):
        """Обновление статуса поста"""
        try:
            db = SessionLocal()
            
            post = db.query(Post).filter(Post.post_id == post_id).first()
            if post:
                post.is_commented = is_commented
                if comment_id:
                    post.comment_id = comment_id
                db.commit()
                
        except Exception as e:
            logger.error(f"Ошибка обновления статуса поста: {e}")
        finally:
            db.close()
