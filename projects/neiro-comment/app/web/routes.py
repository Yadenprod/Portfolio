"""
API маршруты для веб-интерфейса
"""
import logging
from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db, SessionLocal
from app.database.models import Channel, Post, Comment, Metrics
from app.telegram.monitor import add_channel, remove_channel, update_channel_settings
from app.ai.generator import CommentGenerator

logger = logging.getLogger(__name__)

# Создание роутера
router = APIRouter()

# Pydantic модели для API
class ChannelCreate(BaseModel):
    username: str
    title: Optional[str] = None
    description: Optional[str] = None

class ChannelUpdate(BaseModel):
    is_active: Optional[bool] = None
    comment_enabled: Optional[bool] = None
    comment_frequency: Optional[int] = None

class CommentGenerate(BaseModel):
    content: str
    media_type: str = "text"
    style: Optional[str] = None
    mood: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    content: str
    status: str
    created_at: datetime
    channel_id: str
    post_id: Optional[str] = None

class ChannelResponse(BaseModel):
    id: int
    channel_id: str
    username: str
    title: str
    description: Optional[str]
    is_active: bool
    comment_enabled: bool
    comment_frequency: int
    created_at: datetime
    updated_at: datetime

class PostResponse(BaseModel):
    id: int
    post_id: str
    channel_id: str
    content: Optional[str]
    media_type: Optional[str]
    published_at: datetime
    is_commented: bool
    comment_id: Optional[str]

class MetricsResponse(BaseModel):
    total_channels: int
    active_channels: int
    total_posts: int
    commented_posts: int
    total_comments: int
    comments_today: int
    comments_this_hour: int


@router.get("/", response_class=HTMLResponse)
async def dashboard():
    """Главная страница дашборда"""
    return """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NeiroComment Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .card { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .btn-danger { background: #dc3545; }
            .btn-danger:hover { background: #c82333; }
            .form-group { margin-bottom: 15px; }
            .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
            .form-group input, .form-group select { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
            .table { width: 100%; border-collapse: collapse; }
            .table th, .table td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            .table th { background-color: #f8f9fa; }
            .status-active { color: #28a745; font-weight: bold; }
            .status-inactive { color: #dc3545; font-weight: bold; }
            .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
            .metric-card { background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center; }
            .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
            .metric-label { color: #6c757d; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 NeiroComment Dashboard</h1>
                <p>Система автоматического комментирования в Telegram</p>
            </div>
            
            <div class="card">
                <h2>📊 Метрики</h2>
                <div class="metrics-grid" id="metrics">
                    <!-- Метрики будут загружены через JavaScript -->
                </div>
            </div>
            
            <div class="card">
                <h2>➕ Добавить канал</h2>
                <form id="addChannelForm">
                    <div class="form-group">
                        <label for="channelUsername">Username канала (без @):</label>
                        <input type="text" id="channelUsername" placeholder="example_channel" required>
                    </div>
                    <button type="submit" class="btn">Добавить канал</button>
                </form>
            </div>
            
            <div class="card">
                <h2>📱 Управление каналами</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Канал</th>
                            <th>Статус</th>
                            <th>Комментарии</th>
                            <th>Частота</th>
                            <th>Действия</th>
                        </tr>
                    </thead>
                    <tbody id="channelsTable">
                        <!-- Каналы будут загружены через JavaScript -->
                    </tbody>
                </table>
            </div>
            
            <div class="card">
                <h2>💬 Тест генерации комментариев</h2>
                <form id="testCommentForm">
                    <div class="form-group">
                        <label for="testContent">Содержимое поста:</label>
                        <textarea id="testContent" rows="3" placeholder="Введите текст поста для тестирования..." required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="testMediaType">Тип контента:</label>
                        <select id="testMediaType">
                            <option value="text">Текст</option>
                            <option value="photo">Фото</option>
                            <option value="video">Видео</option>
                            <option value="document">Документ</option>
                        </select>
                    </div>
                    <button type="submit" class="btn">Сгенерировать комментарий</button>
                </form>
                <div id="testResult" style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 4px; display: none;">
                    <strong>Результат:</strong>
                    <div id="testComment"></div>
                </div>
            </div>
        </div>
        
        <script>
            // Загрузка метрик
            async function loadMetrics() {
                try {
                    const response = await fetch('/api/v1/metrics');
                    const metrics = await response.json();
                    
                    document.getElementById('metrics').innerHTML = `
                        <div class="metric-card">
                            <div class="metric-value">${metrics.total_channels}</div>
                            <div class="metric-label">Всего каналов</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${metrics.active_channels}</div>
                            <div class="metric-label">Активных</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${metrics.total_posts}</div>
                            <div class="metric-label">Всего постов</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${metrics.commented_posts}</div>
                            <div class="metric-label">С комментариями</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${metrics.total_comments}</div>
                            <div class="metric-label">Всего комментариев</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${metrics.comments_today}</div>
                            <div class="metric-label">Сегодня</div>
                        </div>
                    `;
                } catch (error) {
                    console.error('Ошибка загрузки метрик:', error);
                }
            }
            
            // Загрузка каналов
            async function loadChannels() {
                try {
                    const response = await fetch('/api/v1/channels');
                    const channels = await response.json();
                    
                    const tbody = document.getElementById('channelsTable');
                    tbody.innerHTML = channels.map(channel => `
                        <tr>
                            <td>@${channel.username} - ${channel.title}</td>
                            <td><span class="${channel.is_active ? 'status-active' : 'status-inactive'}">${channel.is_active ? 'Активен' : 'Неактивен'}</span></td>
                            <td><span class="${channel.comment_enabled ? 'status-active' : 'status-inactive'}">${channel.comment_enabled ? 'Включены' : 'Отключены'}</span></td>
                            <td>${channel.comment_frequency}/час</td>
                            <td>
                                <button class="btn" onclick="toggleChannel(${channel.id}, ${!channel.is_active})">${channel.is_active ? 'Деактивировать' : 'Активировать'}</button>
                                <button class="btn btn-danger" onclick="deleteChannel(${channel.id})">Удалить</button>
                            </td>
                        </tr>
                    `).join('');
                } catch (error) {
                    console.error('Ошибка загрузки каналов:', error);
                }
            }
            
            // Добавление канала
            document.getElementById('addChannelForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('channelUsername').value;
                
                try {
                    const response = await fetch('/api/v1/channels', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username })
                    });
                    
                    if (response.ok) {
                        alert('Канал добавлен успешно!');
                        document.getElementById('channelUsername').value = '';
                        loadChannels();
                        loadMetrics();
                    } else {
                        const error = await response.json();
                        alert('Ошибка: ' + error.detail);
                    }
                } catch (error) {
                    alert('Ошибка добавления канала: ' + error.message);
                }
            });
            
            // Тест генерации комментариев
            document.getElementById('testCommentForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const content = document.getElementById('testContent').value;
                const mediaType = document.getElementById('testMediaType').value;
                
                try {
                    const response = await fetch('/api/v1/comments/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ content, media_type: mediaType })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        document.getElementById('testComment').textContent = result.comment;
                        document.getElementById('testResult').style.display = 'block';
                    } else {
                        const error = await response.json();
                        alert('Ошибка: ' + error.detail);
                    }
                } catch (error) {
                    alert('Ошибка генерации комментария: ' + error.message);
                }
            });
            
            // Переключение статуса канала
            async function toggleChannel(channelId, newStatus) {
                try {
                    const response = await fetch(`/api/v1/channels/${channelId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ is_active: newStatus })
                    });
                    
                    if (response.ok) {
                        loadChannels();
                        loadMetrics();
                    } else {
                        alert('Ошибка обновления канала');
                    }
                } catch (error) {
                    alert('Ошибка: ' + error.message);
                }
            }
            
            // Удаление канала
            async function deleteChannel(channelId) {
                if (!confirm('Вы уверены, что хотите удалить этот канал?')) return;
                
                try {
                    const response = await fetch(`/api/v1/channels/${channelId}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        loadChannels();
                        loadMetrics();
                    } else {
                        alert('Ошибка удаления канала');
                    }
                } catch (error) {
                    alert('Ошибка: ' + error.message);
                }
            }
            
            // Загрузка данных при загрузке страницы
            document.addEventListener('DOMContentLoaded', () => {
                loadMetrics();
                loadChannels();
            });
        </script>
    </body>
    </html>
    """


@router.get("/channels", response_model=List[ChannelResponse])
async def get_channels(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Получение списка каналов"""
    try:
        channels = db.query(Channel).offset(skip).limit(limit).all()
        return channels
    except Exception as e:
        logger.error(f"Ошибка получения каналов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения каналов")


@router.post("/channels", response_model=ChannelResponse)
async def create_channel(channel_data: ChannelCreate, db: Session = Depends(get_db)):
    """Добавление нового канала"""
    try:
        # Добавляем канал через монитор
        success = await add_channel(channel_data.username)
        
        if not success:
            raise HTTPException(status_code=400, detail="Не удалось добавить канал")
        
        # Получаем добавленный канал
        channel = db.query(Channel).filter(Channel.username == channel_data.username).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Канал не найден после добавления")
        
        return channel
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка добавления канала: {e}")
        raise HTTPException(status_code=500, detail="Ошибка добавления канала")


@router.put("/channels/{channel_id}", response_model=ChannelResponse)
async def update_channel(channel_id: int, channel_data: ChannelUpdate, db: Session = Depends(get_db)):
    """Обновление настроек канала"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Канал не найден")
        
        # Обновляем поля
        if channel_data.is_active is not None:
            channel.is_active = channel_data.is_active
        if channel_data.comment_enabled is not None:
            channel.comment_enabled = channel_data.comment_enabled
        if channel_data.comment_frequency is not None:
            channel.comment_frequency = channel_data.comment_frequency
        
        channel.updated_at = datetime.now()
        db.commit()
        db.refresh(channel)
        
        return channel
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка обновления канала: {e}")
        raise HTTPException(status_code=500, detail="Ошибка обновления канала")


@router.delete("/channels/{channel_id}")
async def delete_channel(channel_id: int, db: Session = Depends(get_db)):
    """Удаление канала"""
    try:
        channel = db.query(Channel).filter(Channel.id == channel_id).first()
        
        if not channel:
            raise HTTPException(status_code=404, detail="Канал не найден")
        
        # Удаляем канал через монитор
        success = await remove_channel(channel.channel_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Не удалось удалить канал")
        
        # Удаляем из БД
        db.delete(channel)
        db.commit()
        
        return {"message": "Канал удален успешно"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка удаления канала: {e}")
        raise HTTPException(status_code=500, detail="Ошибка удаления канала")


@router.get("/posts", response_model=List[PostResponse])
async def get_posts(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Получение списка постов"""
    try:
        posts = db.query(Post).offset(skip).limit(limit).order_by(Post.published_at.desc()).all()
        return posts
    except Exception as e:
        logger.error(f"Ошибка получения постов: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения постов")


@router.get("/comments", response_model=List[CommentResponse])
async def get_comments(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Получение списка комментариев"""
    try:
        comments = db.query(Comment).offset(skip).limit(limit).order_by(Comment.created_at.desc()).all()
        return comments
    except Exception as e:
        logger.error(f"Ошибка получения комментариев: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения комментариев")


@router.post("/comments/generate")
async def generate_comment(comment_data: CommentGenerate):
    """Генерация тестового комментария"""
    try:
        generator = CommentGenerator()
        
        comment = await generator.generate_comment(
            content=comment_data.content,
            media_type=comment_data.media_type,
            style=comment_data.style,
            mood=comment_data.mood
        )
        
        if not comment:
            raise HTTPException(status_code=400, detail="Не удалось сгенерировать комментарий")
        
        return {"comment": comment}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка генерации комментария: {e}")
        raise HTTPException(status_code=500, detail="Ошибка генерации комментария")


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(db: Session = Depends(get_db)):
    """Получение метрик системы"""
    try:
        # Общие метрики
        total_channels = db.query(Channel).count()
        active_channels = db.query(Channel).filter(Channel.is_active == True).count()
        total_posts = db.query(Post).count()
        commented_posts = db.query(Post).filter(Post.is_commented == True).count()
        total_comments = db.query(Comment).count()
        
        # Комментарии за сегодня
        today = datetime.now().date()
        comments_today = db.query(Comment).filter(
            Comment.created_at >= today
        ).count()
        
        # Комментарии за последний час
        one_hour_ago = datetime.now() - timedelta(hours=1)
        comments_this_hour = db.query(Comment).filter(
            Comment.created_at >= one_hour_ago
        ).count()
        
        return MetricsResponse(
            total_channels=total_channels,
            active_channels=active_channels,
            total_posts=total_posts,
            commented_posts=commented_posts,
            total_comments=total_comments,
            comments_today=comments_today,
            comments_this_hour=comments_this_hour
        )
        
    except Exception as e:
        logger.error(f"Ошибка получения метрик: {e}")
        raise HTTPException(status_code=500, detail="Ошибка получения метрик")
