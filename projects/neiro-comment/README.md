# 🤖 NeiroComment - AI Commenting System

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-Python%20%7C%20OpenAI%20API%20%7C%20Telegram-blue)
![AI](https://img.shields.io/badge/AI-OpenAI%20GPT-orange)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐-orange)

**Автоматизированная система генерации и публикации комментариев в Telegram с использованием AI**

[App](./app/) | [Documentation](./README.md)

</div>

---

## 📋 Описание проекта

NeiroComment - это комплексная система для автоматической генерации и публикации комментариев в Telegram каналах с использованием искусственного интеллекта (OpenAI GPT). Система включает веб-интерфейс, планировщик задач и систему метрик.

### 🎯 Основная концепция

Система автоматически:
1. Мониторит целевые Telegram каналы
2. Анализирует контент постов
3. Генерирует релевантные комментарии с помощью AI
4. Публикует комментарии с задержками
5. Отслеживает статистику и метрики

---

## 🏗️ Архитектура

### Основные компоненты

#### 1. **Comment Generator** (`app/ai/generator.py`)
- **OpenAI Integration:** AsyncOpenAI клиент с GPT-3.5/GPT-4 моделями
- **Smart Generation:** Анализ типа контента (crypto, tech, news, general) через `analyze_content_type()`
- **Multiple Styles:** 5 стилей комментариев (general, question, opinion, support, humor)
- **Mood System:** 4 настроения (positive, neutral, curious, expert) для вариативности
- **Content Cleaning:** Автоматическая очистка от лишних символов, префиксов, ограничение длины
- **Special Prompts:** Специализированные промпты для криптовалют, технологий, новостей
- **Batch Generation:** Генерация нескольких вариантов комментариев через `generate_multiple_comments()`
- **Media Type Support:** Адаптация под фото, видео, документы, аудио

#### 2. **Telegram Client** (`app/telegram/client.py`)
- **Full API Integration:** python-telegram-bot библиотека для полной интеграции
- **Channel Management:** Получение информации о каналах, добавление в БД
- **Post Monitoring:** Автоматическое получение последних постов через `get_recent_posts()`
- **Comment Publishing:** Отправка комментариев с reply-to функциональностью
- **Rate Limiting:** Проверка лимитов (max_comments_per_hour) для защиты от бана
- **Media Detection:** Автоматическое определение типа медиа (photo, video, document, audio, voice, sticker)
- **Database Integration:** Автоматическое сохранение постов и комментариев в PostgreSQL
- **Pending Posts Processing:** Обработка постов без комментариев через `process_pending_posts()`

#### 3. **Channel Monitor** (`app/telegram/monitor.py`)
- **Background Monitoring:** Асинхронный мониторинг каналов каждые 5 минут
- **Active Channels Tracking:** Автоматическое получение активных каналов из БД
- **Post Processing:** Сохранение новых постов и автоматическое комментирование
- **Channel Management:** Добавление/удаление каналов, обновление настроек
- **Error Handling:** Устойчивость к ошибкам с логированием и retry механизмом

#### 4. **Web Interface** (`app/web/routes.py`)
- **FastAPI REST API:** Полнофункциональный REST API с Pydantic моделями
- **Dashboard:** HTML dashboard с JavaScript для real-time обновлений
- **Channel Management:** CRUD операции для каналов (GET, POST, PUT, DELETE)
- **Comment Generation:** Тестовая генерация комментариев через `/api/v1/comments/generate`
- **Metrics API:** Получение метрик системы (каналы, посты, комментарии)
- **Real-time Updates:** JavaScript fetch для обновления данных без перезагрузки

#### 5. **Metrics System** (`app/monitoring/metrics.py`)
- **SystemMetrics Dataclass:** Структурированное хранение метрик (13+ метрик)
- **MetricsCollector:** Автоматический сбор метрик из БД
- **Time-based Metrics:** Комментарии за сегодня, час, минуту
- **Performance Tracking:** Success rate, error rate, system uptime
- **Database Storage:** Сохранение метрик в БД с автоочисткой старых (>7 дней)
- **Health Checker:** Проверка здоровья системы (БД, Telegram API, AI сервис)

#### 6. **Database Models** (`app/database/models.py`)
- **Channel Model:** Управление каналами (is_active, comment_enabled, comment_frequency)
- **Post Model:** Хранение постов с медиа информацией и статусом комментирования
- **Comment Model:** Трекинг комментариев (status: pending/sent/failed, ai_generated flag)
- **Metrics Model:** JSON хранение метрик с временными метками
- **Relationships:** SQLAlchemy relationships для связей между моделями

---

## 🔑 Ключевые особенности

### 1. **AI Generation**
- OpenAI GPT для генерации
- Релевантные комментарии
- Анализ контента
- Персонализация

### 2. **Telegram Integration**
- Полная интеграция с Telegram
- Мониторинг каналов
- Публикация комментариев
- Управление сессиями

### 3. **Web Interface**
- Удобное управление
- Настройка каналов
- Статистика и аналитика
- Мониторинг

### 4. **Scheduler**
- Планировщик задач
- Автоматический мониторинг
- Гибкое расписание

### 5. **Analytics**
- Детальная статистика
- Метрики эффективности
- Отчеты
- Анализ результатов

---

## 🚀 Технологический стек

### Backend
- **Python 3.8+** - Основной язык
- **OpenAI API** - AI генерация
- **Telegram API** - Интеграция с Telegram
- **FastAPI/Flask** - Web framework
- **PostgreSQL** - База данных

### Frontend
- **React/Vue** - UI библиотека
- **TypeScript** - Типизация

### Infrastructure
- **Alembic** - Миграции БД
- **Celery** - Фоновые задачи
- **Redis** - Кэширование

---

## 📊 Возможности

- ✅ AI генерация комментариев
- ✅ Интеграция с Telegram
- ✅ Веб-интерфейс
- ✅ Планировщик задач
- ✅ Система метрик
- ✅ Аналитика и статистика

---

## 🔧 Установка и запуск

### Требования

- Python 3.8+
- PostgreSQL
- OpenAI API ключ
- Telegram API ключи

### Установка

```bash
pip install -r requirements.txt
```

### Настройка

```bash
cp config.env.example .env
# Отредактируйте .env файл
```

### Инициализация БД

```bash
alembic upgrade head
```

### Запуск

```bash
python main.py
```

---

## 📁 Структура проекта

```
neirocomment/
├── app/
│   └── ai/
│       └── generator.py      # AI генератор
├── requirements.txt
└── README.md
```

---

## 💡 Особенности реализации

1. **AI Integration:**
   - OpenAI GPT для генерации
   - Релевантные комментарии
   - Анализ контента

2. **Telegram Integration:**
   - Полная интеграция
   - Мониторинг каналов
   - Публикация комментариев

3. **Analytics:**
   - Детальная статистика
   - Метрики эффективности
   - Отчеты

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик разработки
- Используется OpenAI API для генерации
- Полная интеграция с Telegram
- Веб-интерфейс для управления

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready
