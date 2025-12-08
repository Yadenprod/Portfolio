"""
Модели базы данных
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class Channel(Base):
    """Модель канала Telegram"""
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    comment_enabled = Column(Boolean, default=True)
    comment_frequency = Column(Integer, default=1)  # комментариев в час
    last_comment_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Связи
    posts = relationship("Post", back_populates="channel")
    comments = relationship("Comment", back_populates="channel")


class Post(Base):
    """Модель поста в канале"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(String, nullable=False)
    channel_id = Column(String, ForeignKey("channels.channel_id"), nullable=False)
    content = Column(Text, nullable=True)
    media_type = Column(String, nullable=True)  # text, photo, video, etc.
    media_url = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=False)
    is_commented = Column(Boolean, default=False)
    comment_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    channel = relationship("Channel", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    """Модель комментария"""
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(String, nullable=True)
    channel_id = Column(String, ForeignKey("channels.channel_id"), nullable=False)
    post_id = Column(String, ForeignKey("posts.post_id"), nullable=True)
    content = Column(Text, nullable=False)
    ai_generated = Column(Boolean, default=True)
    status = Column(String, default="pending")  # pending, sent, failed
    error_message = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Связи
    channel = relationship("Channel", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Settings(Base):
    """Модель настроек системы"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Metrics(Base):
    """Модель метрик системы"""
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Integer, nullable=False)
    metric_data = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=func.now())
    
    # Индексы для быстрого поиска
    __table_args__ = (
        {"sqlite_autoincrement": True}
    )
