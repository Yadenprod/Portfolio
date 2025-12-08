# 🎮 CS2 Panel - CS2 Account Management System

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-Next.js%20%7C%20TypeScript%20%7C%20MongoDB%20%7C%20Steam%20API-blue)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐⭐-orange)

**Полнофункциональная панель управления для автоматизации CS2 аккаунтов с интеграцией Steam API**

[Backend](./pages/api/) | [Frontend](./pages/) | [Scripts](./scripts/)

</div>

---

## 📋 Описание проекта

CS2 Panel - это комплексная система управления CS2 аккаунтами, которая позволяет автоматизировать вход в Steam, управлять аккаунтами, запускать ботов для фарма кейсов и отслеживать статистику. Система построена на Next.js с интеграцией Steam API и MongoDB.

### 🎯 Основная концепция

Система предоставляет:
1. Управление множеством Steam аккаунтов
2. Автоматический вход в Steam с обработкой Steam Guard
3. Запуск CS2 ботов для автоматического фарма кейсов
4. Отслеживание статистики и кейсов
5. Rate limiting для защиты от банов
6. Real-time обновления статуса

---

## 🏗️ Архитектура

### Backend (Next.js API Routes)

#### **Steam Integration:**

1. **SteamAPI** (`lib/steam/steamAPI.ts`)
   - Обертка над `steam-user`
   - Управление Steam клиентом
   - Обработка событий (loggedOn, disconnected, error)
   - Steam Guard поддержка
   - Mobile confirmation ожидание

2. **SteamManager** (`lib/steam/steamManager.ts`)
   - Управление множественными аккаунтами
   - Rate limiting (15 минут между запросами)
   - Очередь запросов
   - Управление сессиями

3. **API Routes:**
   - `/api/steam/login` - Вход в Steam
   - `/api/steam/logout` - Выход из Steam
   - `/api/steam/status` - Статус аккаунта
   - `/api/steam/login-with-mobile` - Вход с мобильным подтверждением
   - `/api/steam/start-game` - Запуск CS2
   - `/api/steam/stop-game` - Остановка CS2
   - `/api/steam/clear-rate-limit` - Очистка rate limit

#### **Game Automation:**

1. **GameManager** (`lib/automation/gameManager.ts`)
   - Управление множественными игровыми клиентами
   - Ограничение одновременных клиентов (по умолчанию 3)
   - Event-driven архитектура
   - Управление жизненным циклом клиентов

2. **GameClient** (`lib/automation/gameClient.ts`)
   - Управление одним игровым клиентом
   - Запуск CS2 через Steam
   - Интеграция с ботом
   - Обработка событий

3. **CS2 Bot** (`scripts/cs2_bot.py`)
   - Python скрипт для автоматизации CS2
   - Автоматическое движение и стрельба
   - Сбор кейсов
   - Интеграция с панелью через API

4. **API Routes:**
   - `/api/gameplay/start` - Запуск автоматизации
   - `/api/gameplay/stop` - Остановка автоматизации
   - `/api/gameplay/status` - Статус автоматизации
   - `/api/gameplay/[id]` - Управление конкретной сессией
   - `/api/gameplay/simulate` - Симуляция игры

#### **Account Management:**

1. **Account Model** (`models/Account.ts`)
   - MongoDB модель аккаунта
   - Хранение Steam данных
   - Статистика кейсов
   - Статус аккаунта

2. **API Routes:**
   - `/api/accounts` - Список аккаунтов
   - `/api/accounts/[id]` - Управление аккаунтом
   - `/api/accounts/update-cases` - Обновление кейсов

#### **Authentication:**

1. **NextAuth Integration**
   - JWT аутентификация
   - Session management
   - Protected routes

2. **API Routes:**
   - `/api/auth/login` - Вход
   - `/api/auth/register` - Регистрация
   - `/api/auth/[...nextauth]` - NextAuth handler

### Frontend (Next.js Pages)

#### **Pages (61 компонент):**

1. **Dashboard:**
   - `pages/dashboard/index.tsx` - Главная панель
   - `pages/dashboard/accounts.tsx` - Управление аккаунтами
   - `pages/dashboard/cases.tsx` - Статистика кейсов
   - `pages/dashboard/gameplay.tsx` - Управление автоматизацией
   - `pages/dashboard/settings.tsx` - Настройки

2. **Auth:**
   - `pages/login.tsx` - Вход
   - `pages/register.tsx` - Регистрация
   - `pages/logout.tsx` - Выход

3. **Account Details:**
   - `pages/accounts/[id].tsx` - Детали аккаунта

#### **Components:**

1. **SteamStatus** (`components/SteamStatus.tsx`)
   - Отображение статуса Steam
   - Real-time обновления

2. **SteamLogin** (`components/SteamLogin.tsx`)
   - Компонент входа в Steam
   - Обработка Steam Guard

3. **CS2Bot** (`components/CS2Bot.tsx`)
   - Управление CS2 ботом
   - Статус автоматизации

---

## 🔑 Ключевые особенности

### 1. **Steam Integration**
- Полная интеграция с Steam API
- Обработка Steam Guard
- Mobile confirmation поддержка
- Rate limiting защита
- Управление сессиями

### 2. **Game Automation**
- Автоматический запуск CS2
- Python бот для автоматизации
- Управление множественными клиентами
- Event-driven архитектура

### 3. **Account Management**
- Управление множеством аккаунтов
- Отслеживание статистики
- MongoDB хранение данных
- Real-time обновления

### 4. **Security**
- NextAuth аутентификация
- Rate limiting
- Защита от банов
- Безопасное хранение данных

### 5. **Real-time Updates**
- WebSocket для обновлений
- Статус аккаунтов
- Статистика кейсов
- События автоматизации

---

## 🚀 Технологический стек

### Backend
- **Next.js 13+** - Full-stack framework
- **TypeScript** - Типобезопасность
- **MongoDB** - База данных
- **NextAuth** - Аутентификация
- **steam-user** - Steam API клиент

### Frontend
- **React** - UI библиотека
- **TypeScript** - Типизация
- **Next.js Pages** - Роутинг
- **Tailwind CSS** - Стилизация

### Automation
- **Python 3.8+** - Бот скрипт
- **pyautogui** - Автоматизация GUI
- **win32gui** - Windows API
- **keyboard** - Эмуляция клавиатуры

---

## 📊 Метрики

- **Backend:** 61 TypeScript файл
- **API Routes:** 20+ endpoints
- **Components:** 10+ React компонентов
- **Models:** 3 MongoDB модели
- **Automation:** Python бот с полной интеграцией

---

## 🔧 Установка и запуск

### Backend/Frontend

```bash
npm install
npm run dev
```

### CS2 Bot

```bash
cd scripts
pip install -r requirements.txt
python cs2_bot.py
```

---

## 📁 Структура проекта

```
CSPanel/
├── pages/
│   ├── api/                    # API routes
│   │   ├── steam/              # Steam API
│   │   ├── accounts/           # Account management
│   │   ├── gameplay/           # Game automation
│   │   └── auth/               # Authentication
│   ├── dashboard/              # Dashboard pages
│   └── accounts/               # Account pages
├── lib/
│   ├── steam/                  # Steam integration
│   ├── automation/             # Game automation
│   └── dbConnect.ts            # MongoDB connection
├── models/                     # MongoDB models
├── components/                 # React components
├── scripts/
│   └── cs2_bot.py             # CS2 automation bot
└── types/                      # TypeScript types
```

---

## 💡 Особенности реализации

1. **Rate Limiting:**
   - 15 минут между запросами к Steam
   - Защита от банов
   - Очередь запросов

2. **Multi-Account Support:**
   - Управление множеством аккаунтов
   - Параллельная обработка
   - Изоляция сессий

3. **Event-Driven:**
   - WebSocket обновления
   - Real-time статус
   - Асинхронная обработка

4. **Security:**
   - NextAuth аутентификация
   - Безопасное хранение данных
   - Защита от злоупотреблений

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик Next.js разработки
- Полная интеграция с Steam API
- Python бот для автоматизации CS2
- Real-time обновления через WebSocket

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready
