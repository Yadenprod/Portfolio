# 🔐 ProSity Security - AI Theft Detection System

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20MediaPipe%20%7C%20YOLO%20%7C%20WebSocket-blue)
![ML](https://img.shields.io/badge/ML-Computer%20Vision%20%7C%20Pose%20Detection-orange)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐⭐-red)

**AI система для предотвращения краж в торговых центрах с использованием Computer Vision**

[Backend](./backend/) | [Frontend](./frontend/) | [Documentation](./README.md)

</div>

---

## 📋 Описание проекта

ProSity Security - это интеллектуальная система детекции краж в торговых центрах, которая использует Computer Vision для анализа поведения посетителей в реальном времени. Система обнаруживает подозрительное поведение, попытки вскрытия упаковок и движение к выходам.

### 🎯 Основная концепция

Система автоматически:
1. Анализирует видеопоток с камер
2. Детектирует подозрительное поведение
3. Определяет попытки вскрытия упаковок
4. Отслеживает движение к выходам
5. Отправляет real-time уведомления
6. Ведет аналитику и статистику

---

## 🏗️ Архитектура

### Backend (FastAPI)

#### **Основные компоненты:**

1. **TheftDetectionSystem** (`backend/models/detection.py`)
   - MediaPipe для детекции позы, рук и лица
   - Анализ подозрительного поведения
   - Детекция вскрытия упаковок
   - Отслеживание движения к выходам
   - Расчет suspicious_score

2. **AnalyticsEngine** (`backend/models/analytics.py`)
   - Статистика краж
   - Анализ по магазинам
   - Анализ по категориям товаров
   - Сезонные факторы
   - Расчет предотвращенных краж

3. **DatabaseManager** (`backend/models/database.py`)
   - PostgreSQL интеграция
   - Хранение событий
   - Управление данными

4. **FastAPI Application** (`backend/main.py`)
   - REST API endpoints
   - WebSocket для real-time уведомлений
   - CORS настройки
   - Health checks

#### **API Endpoints:**

- `GET /` - Информация о системе
- `GET /api/stats` - Статистика краж
- `POST /api/detect` - Детекция в кадре
- `WebSocket /ws` - Real-time уведомления

### Frontend (React)

#### **Components:**
- Real-time мониторинг
- Статистика и графики
- Уведомления о событиях
- Управление системой

---

## 🔑 Ключевые особенности

### 1. **Computer Vision**
- **MediaPipe Pose** - Детекция позы
- **MediaPipe Hands** - Детекция рук
- **MediaPipe Face Detection** - Детекция лиц
- Анализ наклонов головы
- Детекция скрытия рук

### 2. **Behavioral Analysis**
- Анализ подозрительного поведения
- Детекция вскрытия упаковок
- Отслеживание движения к выходам
- Расчет suspicious_score

### 3. **Real-time Processing**
- WebSocket для уведомлений
- Обработка видеопотока
- Мгновенные алерты

### 4. **Analytics**
- Статистика по магазинам
- Анализ по категориям
- Сезонные факторы
- Расчет предотвращенных краж

---

## 🚀 Технологический стек

### Backend
- **FastAPI** - Web framework
- **MediaPipe** - Computer Vision
- **OpenCV** - Обработка изображений
- **PostgreSQL** - База данных
- **WebSocket** - Real-time communication

### Frontend
- **React** - UI библиотека
- **TypeScript** - Типизация
- **WebSocket Client** - Real-time updates

---

## 📊 Возможности

- ✅ Детекция подозрительного поведения
- ✅ Анализ позы и жестов
- ✅ Детекция вскрытия упаковок
- ✅ Отслеживание движения к выходам
- ✅ Real-time уведомления
- ✅ Аналитика и статистика
- ✅ Интеграция с камерами
- ✅ WebSocket для real-time

---

## 🔧 Установка и запуск

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Структура проекта

```
projectProSity/
├── backend/
│   ├── main.py                  # FastAPI приложение
│   └── models/
│       ├── detection.py         # Система детекции
│       ├── analytics.py         # Аналитика
│       └── database.py          # База данных
└── frontend/                    # React приложение
```

---

## 💡 Особенности реализации

1. **Multi-modal Detection:**
   - Поза, руки, лицо
   - Комбинированный анализ
   - Высокая точность

2. **Real-time Processing:**
   - WebSocket обновления
   - Мгновенные алерты
   - Низкая задержка

3. **Analytics:**
   - Детальная статистика
   - Сезонные факторы
   - Анализ эффективности

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик Computer Vision
- Используется MediaPipe для детекции
- Real-time обработка через WebSocket
- Полная аналитика и статистика

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready
