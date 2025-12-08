# Mobile Legends Cases

Сайт для открытия кейсов Mobile Legends Bang Bang.

## Установка

### Требования
- PHP 7.2+
- MySQL/MariaDB
- Composer
- Node.js и npm
- Apache/Nginx

### Локальная установка

1. **Настройка базы данных:**
   - Создайте базу данных (например, `mobile_legends_cases`)
   - Импортируйте структуру из файла `cms.sql`
   - Если нужно, импортируйте дополнительные данные Mobile Legends из файла `mobile_legends_tables.sql`

2. **Настройка конфигурации:**
   - Отредактируйте `core/settings/DataBaseSet.php` с вашими настройками БД
   - Отредактируйте `core/settings/CacheSet.php` при необходимости

3. **Установка:**
   - Откройте в браузере `http://localhost/install.php`
   - После установки удалите файл `install.php`

4. **Настройка виртуального хоста:**
   ```
   <VirtualHost *:80>
       ServerName localhost
       DocumentRoot "/path/to/html/public"
       
       <Directory "/path/to/html/public">
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
       
       ErrorLog ${APACHE_LOG_DIR}/mobile-legends-error.log
       CustomLog ${APACHE_LOG_DIR}/mobile-legends-access.log combined
   </VirtualHost>
   ```

5. **Запуск:**
   - Перезапустите Apache
   - Откройте сайт в браузере

### Продакшн установка (Ubuntu)

1. **Обновление пакетов:**
   ```
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Установка LAMP:**
   ```
   sudo apt install apache2 mysql-server php php-cli php-fpm php-mysql php-json php-curl php-memcached memcached -y
   ```

3. **Настройка MySQL:**
   ```
   sudo mysql_secure_installation
   sudo mysql
   ```
   
   ```sql
   CREATE DATABASE mobile_legends_cases;
   CREATE USER 'mluser'@'localhost' IDENTIFIED BY 'ваш_пароль';
   GRANT ALL PRIVILEGES ON mobile_legends_cases.* TO 'mluser'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

4. **Настройка Apache:**
   ```
   sudo a2enmod rewrite
   sudo systemctl restart apache2
   ```

5. **Настройка виртуального хоста:**
   ```
   sudo nano /etc/apache2/sites-available/mobile-legends.conf
   ```
   
   Добавьте:
   ```
   <VirtualHost *:80>
       ServerName вашдомен.com
       DocumentRoot /var/www/html/public
       
       <Directory /var/www/html/public>
           Options Indexes FollowSymLinks
           AllowOverride All
           Require all granted
       </Directory>
       
       ErrorLog ${APACHE_LOG_DIR}/mobile-legends-error.log
       CustomLog ${APACHE_LOG_DIR}/mobile-legends-access.log combined
   </VirtualHost>
   ```
   
   ```
   sudo a2ensite mobile-legends.conf
   sudo systemctl reload apache2
   ```

6. **Настройка SSL (Let's Encrypt):**
   ```
   sudo apt install certbot python3-certbot-apache -y
   sudo certbot --apache -d вашдомен.com
   ```

7. **Копирование файлов проекта:**
   ```
   sudo mkdir -p /var/www/html
   sudo cp -r /путь/к/файлам/* /var/www/html/
   sudo chown -R www-data:www-data /var/www/html
   ```

8. **Импорт базы данных:**
   ```
   mysql -u mluser -p mobile_legends_cases < /путь/к/cms.sql
   mysql -u mluser -p mobile_legends_cases < /путь/к/mobile_legends_tables.sql
   ```

9. **Настройка конфигурации:**
   - Отредактируйте `/var/www/html/core/settings/DataBaseSet.php`
   - Запустите установку: `http://вашдомен.com/install.php`
   - После установки удалите файл `install.php`

## Администрирование

- Админ-панель: `http://вашдомен.com/admin`
- Логин: `admin`
- Пароль: задается при установке (по умолчанию `12345`) 