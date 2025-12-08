FROM php:8.2-fpm

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    sqlite3 \
    libsqlite3-dev

# Очищаем кэш
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем расширения PHP
RUN docker-php-ext-install pdo_mysql pdo_sqlite mbstring exif pcntl bcmath gd

# Устанавливаем Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Устанавливаем рабочую директорию
WORKDIR /var/www/html

# Копируем существующие файлы проекта
COPY . .

# Создаем SQLite базу данных, если она не существует
RUN touch /var/www/html/database/database.sqlite

# Устанавливаем зависимости Composer
RUN composer install --no-interaction

# Устанавливаем Node.js и npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install

# Устанавливаем права доступа
RUN chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache /var/www/html/database/database.sqlite

# Генерируем ключ приложения
RUN php artisan key:generate

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD php artisan migrate:fresh --seed && php artisan serve --host=0.0.0.0 --port=8000
