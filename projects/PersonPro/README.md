# 📱 PersonPro - React Native Personal Development App

<div align="center">

![Status](https://img.shields.io/badge/Status-Production--ready-brightgreen)
![Tech Stack](https://img.shields.io/badge/Stack-React%20Native%20%7C%20TypeScript%20%7C%20Expo-blue)
![Mobile](https://img.shields.io/badge/Platform-iOS%20%7C%20Android-lightgrey)
![Complexity](https://img.shields.io/badge/Complexity-⭐⭐⭐⭐-orange)

**Современное мобильное приложение для личного развития с AI рекомендациями и отслеживанием целей**

[App](./App.tsx) | [Screens](./src/screens/) | [Components](./src/components/) | [Documentation](./README.md)

</div>

---

## 📋 Описание проекта

PersonPro - это полнофункциональное React Native приложение для личного развития, которое помогает пользователям ставить цели, отслеживать прогресс и получать AI-рекомендации для достижения успеха.

### 🎯 Основная концепция

Приложение объединяет:
- 📊 **Отслеживание целей** с визуализацией прогресса
- 🤖 **AI рекомендации** для личного развития
- 📈 **Статистика и аналитика** достижений
- 👤 **Профиль пользователя** с настройками
- 🎨 **Современный UI/UX** с Material Design

---

## 🏗️ Архитектура

### Основные компоненты

#### 1. **Navigation** (`src/navigation/AppNavigator.tsx`)
- React Navigation для навигации между экранами
- Stack Navigator для основных экранов
- Tab Navigator для главного раздела
- Auth Navigator для экранов авторизации

#### 2. **Screens**
- **Auth Screens:**
  - `WelcomeScreen.tsx` - Приветственный экран
  - `LoginScreen.tsx` - Экран входа
  - `RegisterScreen.tsx` - Экран регистрации
- **Main Screens:**
  - `DashboardScreen.tsx` - Главная панель с целями
  - `GoalDetailScreen.tsx` - Детали цели
  - `NewGoalScreen.tsx` - Создание новой цели
  - `StatsScreen.tsx` - Статистика и аналитика
  - `AIRecommendationsScreen.tsx` - AI рекомендации
  - `ProfileScreen.tsx` - Профиль пользователя
  - `SettingsScreen.tsx` - Настройки приложения

#### 3. **Components**
- `GoalCard.tsx` - Карточка цели с прогрессом
- `ProgressBar.tsx` - Индикатор прогресса
- `StatsCard.tsx` - Карточка статистики
- `RecommendationCard.tsx` - Карточка AI рекомендации

#### 4. **Context** (`src/context/AppContext.tsx`)
- Глобальное состояние приложения
- Управление пользователем
- Управление целями и прогрессом
- Интеграция с AsyncStorage

#### 5. **Types** (`src/types/index.ts`)
- TypeScript типы для всех сущностей
- Интерфейсы для целей, пользователя, статистики

---

## 🔑 Ключевые особенности

### 1. **Goal Management**
- Создание и редактирование целей
- Отслеживание прогресса с визуализацией
- Категоризация целей
- Напоминания и уведомления

### 2. **AI Recommendations**
- Персонализированные рекомендации
- Анализ прогресса пользователя
- Предложения по улучшению
- Адаптивные советы

### 3. **Statistics & Analytics**
- Визуализация прогресса
- Графики достижений
- Анализ трендов
- Экспорт данных

### 4. **User Experience**
- Современный Material Design UI
- Плавные анимации и переходы
- Темная тема
- Адаптивный дизайн

### 5. **Data Persistence**
- AsyncStorage для локального хранения
- Синхронизация данных
- Офлайн режим
- Backup и восстановление

---

## 🚀 Технологический стек

### Core
- **Framework:** React Native, Expo
- **Language:** TypeScript
- **Navigation:** React Navigation
- **State Management:** Context API, AsyncStorage
- **UI Components:** Custom components, React Native Paper (optional)

### Features
- **Charts:** React Native Charts (optional)
- **Icons:** React Native Vector Icons
- **Storage:** AsyncStorage
- **Animations:** React Native Reanimated (optional)

---

## 📊 Возможности

- ✅ Управление целями
- ✅ Отслеживание прогресса
- ✅ AI рекомендации
- ✅ Статистика и аналитика
- ✅ Профиль пользователя
- ✅ Настройки приложения
- ✅ Офлайн режим
- ✅ Темная тема

---

## 🔧 Установка и запуск

### Требования

- Node.js 16+
- npm или yarn
- Expo CLI
- iOS Simulator или Android Emulator (для разработки)

### Установка

```bash
npm install
# или
yarn install
```

### Запуск

```bash
npm start
# или
yarn start
```

### Сборка

```bash
# iOS
expo build:ios

# Android
expo build:android
```

---

## 📁 Структура проекта

```
PersonPro/
├── App.tsx                    # Главный компонент приложения
├── src/
│   ├── screens/              # Экраны приложения
│   │   ├── auth/            # Экраны авторизации
│   │   └── main/            # Основные экраны
│   ├── components/          # Переиспользуемые компоненты
│   ├── navigation/          # Навигация
│   ├── context/            # Context API для состояния
│   ├── types/              # TypeScript типы
│   └── assets/             # Ресурсы (изображения, иконки)
├── package.json
└── tsconfig.json
```

---

## 💡 Особенности реализации

1. **TypeScript:** Полная типизация для надежности кода
2. **Context API:** Централизованное управление состоянием
3. **React Navigation:** Современная навигация с поддержкой глубоких ссылок
4. **AsyncStorage:** Локальное хранение данных
5. **Component-based:** Модульная архитектура с переиспользуемыми компонентами

---

## 📝 Примечания

- Проект разработан с использованием **Cursor AI** и современных практик разработки
- Используется TypeScript для типобезопасности
- Material Design принципы для UI/UX
- Оптимизация производительности и батареи

---

**Разработчик:** Дмитрий  
**Дата:** Декабрь 2025  
**Статус:** Production-ready

