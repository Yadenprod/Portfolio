# 🎮 Mobile Legends Cases - Enterprise Gaming Platform

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-PHP%20%7C%20Vue.js%20%7C%20Node.js%20%7C%20MySQL-blue)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐⭐-red)

**Полнофункциональная enterprise-платформа для открытия кейсов Mobile Legends с интеграцией Steam, платежными системами и real-time обновлениями**

[Backend](./html/app/) | [Frontend](./html/templates/) | [Bot](./html/bot/) | [Documentation](./README.md)

</div>

---

## 📋 Описание проекта

Mobile Legends Cases - это комплексная enterprise-платформа для открытия игровых кейсов с полной интеграцией Steam, автоматизированными ботами, платежными системами и real-time обновлениями. Система построена на модульной архитектуре с поддержкой множественных плагинов и шаблонов.

### 🎯 Основная концепция

Платформа предоставляет:
1. **Открытие кейсов** - Система открытия кейсов с анимациями и real-time обновлениями
2. **Steam интеграция** - Полная интеграция с Steam для авторизации и торговли
3. **Автоматизированные боты** - Node.js боты для автоматической торговли предметами
4. **Платежные системы** - Интеграция с QIWI, Unitpay, FreeKassa, Интеркасса
5. **Real-time обновления** - Centrifugo для мгновенных обновлений
6. **Админ-панель** - Полнофункциональная админ-панель для управления
7. **Дополнительные режимы** - Battle Solo, Upgrade, Contracts

---

## 🏗️ Архитектура

### Backend (PHP)

#### **Core System:**

1. **Database** (`core/class/Database.php`)
   - MySQL интеграция
   - Query builder
   - Кэширование запросов
   - Обработка ошибок

2. **PluginManager** (`core/class/PluginManager.php`)
   - Модульная архитектура
   - Динамическая загрузка плагинов
   - Управление жизненным циклом
   - Автоматическая установка/удаление

3. **User Management** (`core/class/User.php`)
   - Управление пользователями
   - Steam авторизация
   - Сессии и безопасность

4. **Cache System** (`core/class/Cache.php`)
   - Кэширование данных
   - Оптимизация производительности

#### **OpenCase Plugin (Основной плагин):**

1. **Case Management** (`app/plugins/opencase/class/case.php`)
   - Управление кейсами
   - Категории и редкость
   - Цены и скидки
   - Лимиты открытий

2. **Item Management** (`app/plugins/opencase/class/item.php`)
   - Управление предметами
   - 13 уровней качества
   - Ценообразование
   - Интеграция с маркетами

3. **OpenCase System** (`app/plugins/opencase/class/openCase.php`)
   - Логика открытия кейсов
   - Расчет выигрышей
   - История открытий
   - Статистика

4. **Bot System** (`app/plugins/opencase/class/bot.php`)
   - Управление ботами
   - Шифрование данных
   - Статусы ботов
   - Интеграция с Steam

5. **Contract System** (`app/plugins/opencase/class/contract.php`)
   - Система контрактов
   - Обмен предметов
   - История контрактов

6. **Deposit System** (`app/plugins/opencase/class/deposite.php`)
   - Управление депозитами
   - Интеграция платежных систем
   - Статусы платежей

7. **Centrifugo Integration** (`app/plugins/opencase/class/centrifugo.php`)
   - Real-time обновления
   - Отправка событий
   - Статистика в реальном времени

8. **Stats System** (`app/plugins/opencase/class/stats.php`)
   - Сбор статистики
   - Аналитика
   - Расширяемая система метрик

#### **Modules (10 модулей):**

1. **market.module.php** - Интеграция с маркетами (CSGO Market, Dota2 Market)
2. **withdraw.module.php** - Система вывода средств
3. **promo.module.php** - Промокоды и акции
4. **qiwi.module.php** - Интеграция с QIWI
5. **ref.module.php** - Реферальная система
6. **review.module.php** - Система отзывов
7. **support.module.php** - Техподдержка с тикетами
8. **user.module.php** - Управление пользователями
9. **functions.module.php** - Вспомогательные функции
10. **date.module.php** - Работа с датами

#### **Additional Plugins:**

1. **modebattlesolo** - Режим одиночных баттлов
2. **modeupgarde** - Режим апгрейда предметов
3. **mobilelegends** - Специальный плагин для Mobile Legends
4. **faq** - Система FAQ
5. **online** - Отслеживание онлайн пользователей

### Frontend (Vue.js)

#### **Templates:**

1. **maybedrop** (`templates/maybedrop/`)
   - Основной шаблон
   - Vue.js SPA
   - 13 страниц
   - Real-time обновления через Centrifugo

2. **mlegendsdrop** (`templates/mlegendsdrop/`)
   - Специализированный шаблон для Mobile Legends
   - Vue.js SPA
   - 14 страниц
   - Интеграция с Mobile Legends API

#### **Components:**

- **Pages:** Index, Case, Contracts, Upgrade, Battles, Battle, Profile, Top, Livetrade, FAQ
- **Layout:** Header, Footer
- **Popups:** Модальные окна
- **Elements:** Переиспользуемые элементы

#### **Features:**

- Vue Router для навигации
- Vuex для state management
- Centrifugo для real-time
- Axios для API запросов
- Vue Notifications для уведомлений

### Bot System (Node.js)

#### **Bot Architecture:**

1. **Bot Class** (`bot/class/Bot.js`)
   - Управление Steam ботом
   - Event-driven архитектура
   - Автоматическая авторизация
   - Обработка trade offers

2. **Steam Integration:**
   - Steam Community API
   - Trade Offer Manager
   - Steam Guard поддержка
   - 2FA авторизация

3. **API Integration** (`bot/api.js`)
   - Синхронизация с backend
   - Обновление инвентаря
   - Обновление курсов валют
   - Market tick обновления

4. **Security:**
   - Шифрование данных
   - Безопасное хранение секретов
   - Mafiles поддержка

---

## 🔑 Ключевые особенности

### 1. **Модульная архитектура**
- Plugin-based система
- Динамическая загрузка плагинов
- Легкое расширение функциональности
- Изоляция модулей

### 2. **Real-time обновления**
- Centrifugo WebSocket
- Мгновенные обновления открытий
- Real-time статистика
- Live trade обновления

### 3. **Steam интеграция**
- Полная авторизация через Steam
- Автоматизированные боты
- Trade offers управление
- Инвентарь синхронизация

### 4. **Платежные системы**
- QIWI интеграция
- Unitpay поддержка
- FreeKassa интеграция
- Интеркасса поддержка
- Автоматическая обработка платежей

### 5. **Система кейсов**
- 13 уровней качества предметов
- Динамическое ценообразование
- Система шансов
- История открытий
- Статистика

### 6. **Дополнительные режимы**
- Battle Solo - одиночные баттлы
- Upgrade - апгрейд предметов
- Contracts - система контрактов
- Live Trade - живая торговля

### 7. **Админ-панель**
- Управление кейсами
- Управление предметами
- Управление ботами
- Управление пользователями
- Статистика и аналитика
- Настройки системы

---

## 🚀 Технологический стек

### Backend
- **PHP 7.4+** - Основной язык
- **MySQL** - База данных
- **Custom MVC** - Собственный фреймворк
- **Plugin System** - Модульная архитектура

### Frontend
- **Vue.js 2** - UI фреймворк
- **Vue Router** - Роутинг
- **Vuex** - State management
- **Axios** - HTTP клиент
- **Centrifugo** - Real-time обновления
- **Webpack** - Сборка

### Bot
- **Node.js** - Runtime
- **steam-community** - Steam API
- **steam-tradeoffer-manager** - Trade offers
- **steam-totp** - 2FA

### Infrastructure
- **Centrifugo** - Real-time сервер
- **XAMPP** - Локальная разработка
- **Apache** - Web сервер
- **MySQL** - База данных

---

## 📊 Метрики проекта

- **Backend:** 22 PHP классов в opencase плагине
- **Frontend:** 2 Vue.js шаблона, 27+ компонентов
- **Modules:** 10 модулей
- **Plugins:** 6+ плагинов
- **Bot:** Node.js бот с полной Steam интеграцией
- **Database:** Множественные таблицы для всех функций
- **API:** Внутренние и внешние API endpoints

---

## 🔧 Установка и запуск

### Требования

- Windows 10+
- XAMPP (PHP 7.4+, MySQL, Apache)
- Node.js 14+
- Права администратора

### Установка

1. **Установите XAMPP:**
   ```bash
   # Скачайте с https://www.apachefriends.org/
   # Установите в D:\XPL
   ```

2. **Запустите скрипт настройки:**
   ```bash
   setup_mobile_legends.bat  # От имени администратора
   ```

3. **Настройте hosts файл:**
   ```
   127.0.0.1 mobile-legends.local
   ```

4. **Запустите серверы:**
   - Apache
   - MySQL

5. **Откройте установщик:**
   ```
   http://mobile-legends.local/install.php
   ```

6. **Запустите бота:**
   ```bash
   cd html/bot
   npm install
   node bot.js
   ```

---

## 📁 Структура проекта

```
ML/
├── html/
│   ├── app/
│   │   └── plugins/
│   │       ├── opencase/          # Основной плагин
│   │       │   ├── class/         # 22 PHP класса
│   │       │   ├── modules/       # 10 модулей
│   │       │   ├── admin/         # Админ-панель
│   │       │   ├── user/          # Пользовательские страницы
│   │       │   └── internalapi/   # Внутренние API
│   │       ├── modebattlesolo/    # Battle Solo режим
│   │       ├── modeupgarde/       # Upgrade режим
│   │       ├── mobilelegends/     # Mobile Legends плагин
│   │       └── faq/               # FAQ система
│   ├── core/
│   │   ├── class/                 # Core классы
│   │   ├── modules/               # Core модули
│   │   └── settings/              # Настройки
│   ├── templates/
│   │   ├── maybedrop/             # Основной шаблон (Vue.js)
│   │   └── mlegendsdrop/          # ML шаблон (Vue.js)
│   ├── bot/                       # Node.js бот
│   │   ├── class/                 # Bot классы
│   │   └── modules/               # Bot модули
│   └── public/                    # Публичные файлы
├── cms.sql                        # Структура БД
└── mobile_legends_tables.sql      # ML таблицы
```

---

## 💡 Особенности реализации

1. **Модульная архитектура:**
   - Plugin-based система
   - Динамическая загрузка
   - Изоляция модулей
   - Легкое расширение

2. **Real-time система:**
   - Centrifugo WebSocket
   - Мгновенные обновления
   - Live статистика
   - Event-driven архитектура

3. **Steam интеграция:**
   - Полная авторизация
   - Автоматизированные боты
   - Trade offers
   - Безопасное хранение данных

4. **Платежные системы:**
   - Множественные провайдеры
   - Автоматическая обработка
   - Статусы платежей
   - История транзакций

5. **Система кейсов:**
   - 13 уровней качества
   - Динамическое ценообразование
   - Система шансов
   - Статистика и аналитика

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик разработки
- Enterprise-уровень архитектуры
- Модульная система для легкого расширения
- Полная интеграция с Steam и платежными системами
- Real-time обновления через Centrifugo
- Два Vue.js шаблона для разных игр

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready Enterprise Platform

