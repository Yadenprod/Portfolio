# 💹 Gaming Stock Market - Full-Stack Trading Platform

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-.NET%208.0%20%7C%20React%20%7C%20PostgreSQL-blue)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐⭐-orange)
![Architecture](https://img.shields.io/badge/Architecture-Microservices-green)

**Enterprise-уровня платформа для торговли акциями игровых персонажей в реальном времени**

[Backend](./Backend/) | [Frontend](./Frontend/) | [Documentation](./Documentation/)

</div>

---

## 📋 Описание проекта

Gaming Stock Market - это полнофункциональная биржа акций для торговли "акциями" по киберспорту, игроков и команд в реальном времени. Система построена на микросервисной архитектуре с использованием современных технологий и best practices.

### 🎯 Основная концепция

Пользователи могут покупать и продавать "акции"  игроков и команд, стоимость которых меняется в зависимости от:
- Производительности игроков в матчах
- Успехов в турнирах
- Популярности и активности
- Торгового объема
- Рыночной волатильности
- Системы дефицита
- Управление и стабилизации цен с помощью ботов

---

## 🏗️ Архитектура

### Backend (ASP.NET Core 8.0)

#### **Основные компоненты:**

1. **TradingService** - Ядро торговой системы
   - Размещение и отмена ордеров
   - Автоматическое сопоставление ордеров (Order Matching)
   - Управление портфелем пользователя
   - Расчет комиссий на основе уровня пользователя (0.5% - 2%)
   - Обработка частичного исполнения ордеров
   - Интеграция с системой достижений

2. **OrderBook** - In-memory книга ордеров
   - SortedDictionary для эффективного сопоставления
   - Price-Time Priority алгоритм
   - Real-time исполнение сделок
   - Event-driven архитектура (OnTradeExecuted)

3. **PriceCalculator** - Динамический расчет цен
   - 6-факторная модель ценообразования:
     - Производительность (40%)
     - Успехи в турнирах (30%)
     - Популярность (20%)
     - Фактор команды (10%)
     - Торговый объем (динамический)
     - Волатильность рынка (динамический)
   - Защита от резких скачков цен (лимит 100% в день)

4. **Background Services:**
   - **PriceUpdateService** - Обновление цен real time
   - **DataParsingService** - Парсинг данных из внешних источников
   - **MarketMakerService** - Создание ликвидности
   - **NotificationService** - Уведомления в real time
   - **AuditService** - Аудит всех операций

5. **Repositories (Repository Pattern):**
   - UserRepository, PlayerRepository, TeamRepository
   - OrderRepository, TradeRepository, TransactionRepository
   - UserPortfolioRepository, PriceHistoryRepository
   - AchievementRepository, NotificationRepository, AuditLogRepository

6. **Services:**
   - **JwtService** - JWT аутентификация и авторизация
   - **PaymentService** - Интеграция со Stripe
   - **EmailService** - Отправка email уведомлений
   - **KycService** - KYC верификация
   - **TwoFactorAuthService** - 2FA аутентификация
   - **AnalyticsService** - Аналитика и статистика
   - **AchievementService** - Система достижений

7. **Controllers:**
   - TradingController, PlayersController, PortfolioController
   - AuthController, PaymentController, AdminController
   - AnalyticsController, AchievementsController, NotificationController
   - StripeWebhookController

#### **Технологии Backend:**
- ASP.NET Core 8.0
- PostgreSQL (Entity Framework Core)
- SignalR для real-time обновлений
- JWT Authentication
- Stripe API для платежей
- Serilog для логирования
- Health Checks
- Rate Limiting (10 запросов/10 секунд)
- Response Caching
- CORS настройки

### Frontend (React + TypeScript)

#### **Основные компоненты:**

1. **State Management (Redux Toolkit):**
   - `tradingSlice` - Управление торговлей
   - `authSlice` - Аутентификация
   - `playerSlice` - Данные игроков
   - `achievementSlice` - Достижения
   - `notificationSlice` - Уведомления

2. **Pages (51 компонент):**
   - **Trading:** OrderBookPage, TradeHistoryPage, PortfolioPage
   - **Players:** PlayersPage, PlayerDetailsPage
   - **Teams:** TeamsPage, TeamDetailsPage
   - **Admin:** AdminDashboard, PlayerManagement, TeamManagement, OrderManagement, TransactionManagement, UserManagement, AnalyticsDashboard
   - **Auth:** LoginPage, RegisterPage
   - **Other:** HomePage, DashboardPage, AchievementsPage, NotificationsPage, SettingsPage

3. **Components:**
   - PriceChart, VolumeChart - Графики цен и объемов
   - Modal, Button, Input, Card - UI компоненты
   - LoadingSpinner, ErrorBoundary - Обработка состояний
   - Navbar, Sidebar, Footer - Навигация

4. **API Integration:**
   - `tradingApi` - Торговые операции
   - `playerApi` - Данные игроков
   - `authApi` - Аутентификация
   - `achievementApi` - Достижения
   - `notificationApi` - Уведомления

#### **Технологии Frontend:**
- React 18.2
- TypeScript
- Redux Toolkit
- React Router
- Vite
- Tailwind CSS
- Axios для HTTP запросов
- SignalR Client для real-time

---

## 🔑 Ключевые особенности

### 1. **Real-time Trading Engine**
- In-memory OrderBook для мгновенного сопоставления
- Price-Time Priority алгоритм
- Автоматическое исполнение сделок
- Поддержка частичного исполнения

### 2. **Динамическое ценообразование**
- 6-факторная модель расчета цен
- Учет производительности, турниров, популярности
- Анализ торгового объема и волатильности
- Защита от манипуляций

### 3. **Система уровней и комиссий**
- 4 уровня пользователей (Novice, Trader, Expert, Master)
- Комиссии от 0.5% до 2% в зависимости от уровня
- Система достижений

### 4. **Безопасность**
- JWT аутентификация
- 2FA поддержка
- KYC верификация
- Rate Limiting
- Audit Logging
- Security Headers

### 5. **Real-time обновления**
- SignalR Hubs для торговли и уведомлений
- Автоматическое обновление цен
- Live обновления OrderBook
- Push уведомления

### 6. **Административная панель**
- Управление игроками и командами
- Управление ордерами и транзакциями
- Аналитика и статистика
- Управление пользователями

---

## 📊 Метрики и производительность

- **Backend:** 11 сервисов, 10 контроллеров, 9 репозиториев
- **Frontend:** 51 компонент, 5 Redux slices
- **Database:** 15+ таблиц с оптимизированными индексами
- **Real-time:** SignalR с поддержкой множественных подключений
- **Rate Limiting:** 10 запросов/10 секунд на endpoint
- **Price Updates:** real time

---

## 🚀 Технологический стек

### Backend
- **Framework:** ASP.NET Core 8.0
- **Database:** PostgreSQL
- **ORM:** Entity Framework Core
- **Real-time:** SignalR
- **Authentication:** JWT Bearer
- **Payments:** Stripe API
- **Logging:** Serilog
- **Architecture:** Clean Architecture, Repository Pattern

### Frontend
- **Framework:** React 18.2
- **Language:** TypeScript
- **State:** Redux Toolkit
- **Routing:** React Router
- **Build:** Vite
- **Styling:** Tailwind CSS
- **HTTP:** Axios
- **Real-time:** SignalR Client

### Infrastructure
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Monitoring:** Health Checks
- **Caching:** Response Caching

---

## 📁 Структура проекта

```
PRmilliard/
├── Backend/
│   ├── GamingStockMarket.API/
│   │   ├── Controllers/          # 10 контроллеров
│   │   ├── Services/             # 11 сервисов
│   │   ├── Repositories/          # 9 репозиториев
│   │   ├── Models/                # Entity модели
│   │   ├── DTOs/                  # Data Transfer Objects
│   │   ├── BackgroundServices/    # 5 фоновых сервисов
│   │   ├── Hubs/                  # SignalR Hubs
│   │   └── Program.cs             # Конфигурация
│   └── GamingStockMarket.Tests/   # Unit тесты
├── Frontend/
│   └── gaming-stock-market/
│       ├── src/
│       │   ├── pages/             # 51 компонент
│       │   ├── components/         # UI компоненты
│       │   ├── slices/             # Redux slices
│       │   ├── api/                # API клиенты
│       │   └── types/              # TypeScript типы
│       └── package.json
├── Documentation/                  # Документация
└── Infrastructure/                 # Docker, CI/CD
```

---

## 🎯 Использованные технологии и паттерны

- **Clean Architecture** - Разделение на слои
- **Repository Pattern** - Абстракция доступа к данным
- **Dependency Injection** - Внедрение зависимостей
- **Event-Driven Architecture** - Событийная архитектура
- **Background Services** - Фоновые задачи
- **Real-time Communication** - SignalR
- **JWT Authentication** - Безопасная аутентификация
- **Rate Limiting** - Защита от перегрузки
- **Health Checks** - Мониторинг состояния
- **Response Caching** - Кэширование ответов
- **Redux Toolkit** - Управление состоянием
- **TypeScript** - Типобезопасность

---

## 💡 Особенности реализации

1. **Эффективный Order Matching:**
   - SortedDictionary для O(log n) поиска
   - Price-Time Priority
   - Мгновенное исполнение

2. **Умное ценообразование:**
   - Многофакторная модель
   - Защита от манипуляций
   - Учет исторических данных

3. **Масштабируемость:**
   - Микросервисная архитектура
   - Фоновые сервисы
   - Кэширование

4. **Безопасность:**
   - Многоуровневая защита
   - Audit logging
   - Rate limiting

---

## 🔧 Установка и запуск

### Backend

```bash
cd Backend/GamingStockMarket.API
dotnet restore
dotnet ef database update
dotnet run
```

### Frontend

```bash
cd Frontend/gaming-stock-market
npm install
npm run dev
```

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик разработки
- Все компоненты покрыты документацией
- Используется Clean Architecture для масштабируемости
- Реализованы best practices для безопасности и производительности

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready
