<p align="center"><a href="https://laravel.com" target="_blank"><img src="https://raw.githubusercontent.com/laravel/art/master/logo-lockup/5%20SVG/2%20CMYK/1%20Full%20Color/laravel-logolockup-cmyk-red.svg" width="400" alt="Laravel Logo"></a></p>

<p align="center">
<a href="https://github.com/laravel/framework/actions"><img src="https://github.com/laravel/framework/workflows/tests/badge.svg" alt="Build Status"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/dt/laravel/framework" alt="Total Downloads"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/v/laravel/framework" alt="Latest Stable Version"></a>
<a href="https://packagist.org/packages/laravel/framework"><img src="https://img.shields.io/packagist/l/laravel/framework" alt="License"></a>
</p>

## About Laravel

Laravel is a web application framework with expressive, elegant syntax. We believe development must be an enjoyable and creative experience to be truly fulfilling. Laravel takes the pain out of development by easing common tasks used in many web projects, such as:

- [Simple, fast routing engine](https://laravel.com/docs/routing).
- [Powerful dependency injection container](https://laravel.com/docs/container).
- Multiple back-ends for [session](https://laravel.com/docs/session) and [cache](https://laravel.com/docs/cache) storage.
- Expressive, intuitive [database ORM](https://laravel.com/docs/eloquent).
- Database agnostic [schema migrations](https://laravel.com/docs/migrations).
- [Robust background job processing](https://laravel.com/docs/queues).
- [Real-time event broadcasting](https://laravel.com/docs/broadcasting).

Laravel is accessible, powerful, and provides tools required for large, robust applications.

## Learning Laravel

Laravel has the most extensive and thorough [documentation](https://laravel.com/docs) and video tutorial library of all modern web application frameworks, making it a breeze to get started with the framework.

You may also try the [Laravel Bootcamp](https://bootcamp.laravel.com), where you will be guided through building a modern Laravel application from scratch.

If you don't feel like reading, [Laracasts](https://laracasts.com) can help. Laracasts contains thousands of video tutorials on a range of topics including Laravel, modern PHP, unit testing, and JavaScript. Boost your skills by digging into our comprehensive video library.

## Laravel Sponsors

We would like to extend our thanks to the following sponsors for funding Laravel development. If you are interested in becoming a sponsor, please visit the [Laravel Partners program](https://partners.laravel.com).

### Premium Partners

- **[Vehikl](https://vehikl.com)**
- **[Tighten Co.](https://tighten.co)**
- **[Kirschbaum Development Group](https://kirschbaumdevelopment.com)**
- **[64 Robots](https://64robots.com)**
- **[Curotec](https://www.curotec.com/services/technologies/laravel)**
- **[DevSquad](https://devsquad.com/hire-laravel-developers)**
- **[Redberry](https://redberry.international/laravel-development)**
- **[Active Logic](https://activelogic.com)**

## Contributing

Thank you for considering contributing to the Laravel framework! The contribution guide can be found in the [Laravel documentation](https://laravel.com/docs/contributions).

## Code of Conduct

In order to ensure that the Laravel community is welcoming to all, please review and abide by the [Code of Conduct](https://laravel.com/docs/contributions#code-of-conduct).

## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an e-mail to Taylor Otwell via [taylor@laravel.com](mailto:taylor@laravel.com). All security vulnerabilities will be promptly addressed.

## License

The Laravel framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).

# IIoT Dashboard (Промышленный Мониторинг Оборудования)

## Требования
- Docker
- Docker Compose

## Запуск через Docker

1. Клонирование репозитория
```bash
git clone https://github.com/ваш-репозиторий/iiot-dashboard.git
cd iiot-dashboard/backend
```

2. Сборка и запуск контейнеров
```bash
docker-compose up --build
```

3. Первоначальная настройка
```bash
# Выполнить миграции и заполнить базу данных
docker-compose exec backend php artisan migrate:fresh --seed
```

## Доступ к приложению
- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Nginx прокси: `http://localhost:80`

## Тестовые пользователи
- Администратор: `admin@example.com`
- Инженер: `engineer@example.com`
- Оператор: `operator@example.com`

Пароль для всех: `password`

## Остановка
```bash
docker-compose down
```

## Требования
- PHP 8.2+
- Composer
- Node.js 18+
- npm или yarn

## Установка

1. Клонирование репозитория
```bash
git clone https://github.com/ваш-репозиторий/iiot-dashboard.git
cd iiot-dashboard/backend
```

2. Установка зависимостей PHP
```bash
composer install
```

3. Настройка окружения
```bash
cp .env.example .env
php artisan key:generate
```

4. Настройка базы данных
- Откройте `.env` и настройте подключение к базе данных
- Для SQLite создайте файл базы данных:
```bash
touch database/database.sqlite
```

5. Миграции и заполнение тестовыми данными
```bash
php artisan migrate:fresh --seed
```

## Запуск тестов
```bash
php artisan test
```

## Запуск сервера разработки
```bash
php artisan serve
```

## Роли пользователей
- Администратор (`admin`)
- Инженер (`engineer`)
- Оператор (`operator`)

## Внешние API
- Симуляция данных с датчиков: `/api/external/simulate-sensor`
- Погодный сервис: `/api/external/weather`

## Аутентификация
- Регистрация: `POST /api/register`
- Вход: `POST /api/login`
- Выход: `POST /api/logout`
- Текущий пользователь: `GET /api/me`

## Архитектура и Масштабирование

### Принципы проектирования
- **Модульность**: Каждый компонент системы спроектирован с учетом возможности независимого развития
- **Расширяемость**: Легкое добавление новых типов оборудования, датчиков и API
- **Безопасность**: Многоуровневая система прав доступа

### Потенциал развития
1. **Микросервисная архитектура**
   - Возможность разделения на независимые сервисы (авторизация, мониторинг, управление)
   - Горизонтальное масштабирование

2. **Интеграционные возможности**
   - Поддержка различных протоколов обмена данными
   - Адаптеры для подключения к корпоративным системам (ERP, MES)

3. **Машинное обучение**
   - Прогнозирование отказов оборудования
   - Оптимизация режимов работы

### Рекомендации по развитию
- Внедрение WebSocket для real-time мониторинга
- Создание dashboard с расширенной аналитикой
- Интеграция с системами управления инцидентами

## Безопасность

### Текущие механизмы
- Аутентификация через Laravel Sanctum
- Роль-базированный доступ
- Защита от CSRF
- Валидация входящих данных

### Рекомендации
- Внедрение двухфакторной аутентификации
- Регулярный аудит безопасности
- Мониторинг и логирование действий пользователей

## Производительность

### Оптимизация
- Кэширование частых запросов
- Отложенная загрузка данных
- Минимизация количества запросов к базе данных

### Мониторинг
- Встроенное логирование действий
- Профилирование производительности
- Отслеживание нагрузки на систему

## Лицензия
Проект разработан для демонстрации возможностей Laravel и Vue.js

## API Документация (Swagger/OpenAPI)
- Swagger JSON: `storage/api-docs/swagger.json`
- Для просмотра используйте [Swagger Editor](https://editor.swagger.io/) или любой совместимый viewer.
- Основные эндпоинты описаны для оборудования и заявок на обслуживание.
- Для обновления документации: вручную редактируйте swagger.json или используйте генераторы (например, [Swagger-PHP](https://zircote.github.io/swagger-php/)).

# IIoT Dashboard — КАО «Азот»

## 🎨 Фирменный стиль
- Цвета: azot, industrial, chemical (см. tailwind.config.js)
- Градиенты, glow-тени, WOW-скругления, фоновые паттерны
- Типографика: Inter (основной), Roboto Mono (технический)
- Анимации: wow-fade-in, wow-slide-up, wow-bounce и др.
- Поддержка темной темы, accessibility, адаптивность

## 🧩 Использование компонентов
- **Button.vue** — фирменные кнопки с градиентом, glow, badge, loading
- **Card.vue** — карточки с тенями, скруглениями, паттернами
- **Modal.vue** — модальные окна с анимацией, блокировкой скролла
- **Sidebar.vue** — фирменное меню с логотипом, градиентом
- **Topbar.vue** — верхняя панель с профилем, темой, логотипом
- **Toast.vue** — уведомления с прогресс-баром, цветовой индикацией

## 💡 Best practices
- Используйте только фирменные цвета и утилиты из tailwind.config.js
- Для WOW-эффекта применяйте .wow-gradient, .wow-glow, .wow-bounce и др.
- Всегда проверяйте адаптивность (мобильные, планшеты, десктоп)
- Для доступности: используйте .touch-target, .sr-only, aria-атрибуты
- Не забывайте про плавные переходы и анимации
- Для новых компонентов — следуйте стилю и структуре существующих

## 📦 Примеры
```vue
<Button variant="primary" size="lg" :loading="isLoading">Войти</Button>
<Card :closable="true" badge="NEW">
  <template #header>Заголовок</template>
  Контент карточки
</Card>
```

## 🚀 Поддержка WOW-уровня
- Регулярно обновляйте дизайн, следите за трендами
- Используйте фирменные SVG/PNG-элементы для фона
- Не бойтесь bold-решений: крупные заголовки, яркие акценты, анимации
- Всегда тестируйте на реальных устройствах

---

© 2025 КАО «Азот». Все права защищены.
