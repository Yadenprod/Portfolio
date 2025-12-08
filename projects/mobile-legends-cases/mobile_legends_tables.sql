-- Структура таблицы для предметов Mobile Legends
CREATE TABLE IF NOT EXISTS `ml_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `type` varchar(32) NOT NULL COMMENT 'Тип предмета (скин, герой и т.д.)',
  `rarity` varchar(32) NOT NULL COMMENT 'Редкость предмета',
  `price` float NOT NULL DEFAULT 0,
  `image` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `date_added` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `type` (`type`),
  KEY `rarity` (`rarity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Структура таблицы для кейсов Mobile Legends
CREATE TABLE IF NOT EXISTS `ml_cases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `price` float NOT NULL DEFAULT 0,
  `image` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 1,
  `date_added` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Связь между кейсами и предметами
CREATE TABLE IF NOT EXISTS `ml_cases_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `case_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `drop_chance` float NOT NULL DEFAULT 0 COMMENT 'Вероятность выпадения в %',
  PRIMARY KEY (`id`),
  KEY `case_id` (`case_id`),
  KEY `item_id` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Добавление столбца для Mobile Legends в таблицу пользователей
ALTER TABLE `users` 
ADD COLUMN `ml_id` varchar(255) DEFAULT NULL COMMENT 'ID игрока в Mobile Legends' AFTER `email`,
ADD COLUMN `ml_username` varchar(255) DEFAULT NULL COMMENT 'Имя игрока в Mobile Legends' AFTER `ml_id`;

-- Изменение настроек для Mobile Legends
INSERT INTO `settings` (`setting`, `value`, `comment`, `type`) VALUES
('ml_currency_rate', '10', 'Курс обмена внутренней валюты на алмазы', 'float'),
('ml_min_withdraw', '50', 'Минимальная сумма для вывода алмазов', 'int'),
('ml_api_key', '', 'API ключ для интеграции с Mobile Legends', 'text'),
('ml_api_url', '', 'API URL для интеграции с Mobile Legends', 'text');

-- Добавление примера кейса и предметов для тестирования
INSERT INTO `ml_items` (`name`, `type`, `rarity`, `price`, `image`, `description`) VALUES
('Alucard', 'hero', 'rare', 100, 'alucard.jpg', 'Герой-боец ближнего боя'),
('Демонический охотник', 'skin', 'epic', 250, 'alucard_skin.jpg', 'Эпический скин для Alucard'),
('Задира', 'emote', 'common', 20, 'emote_1.jpg', 'Обычная эмоция для любого героя'),
('Рамка "Чемпион"', 'border', 'legendary', 500, 'border_champion.jpg', 'Легендарная рамка профиля');

INSERT INTO `ml_cases` (`name`, `price`, `image`, `description`) VALUES
('Начальный кейс', 50, 'starter_case.jpg', 'Кейс для новичков с базовыми предметами'),
('Эпический кейс', 200, 'epic_case.jpg', 'Кейс с эпическими предметами'),
('Легендарный кейс', 500, 'legendary_case.jpg', 'Кейс с шансом получить легендарные предметы');

-- Связываем предметы с кейсами
INSERT INTO `ml_cases_items` (`case_id`, `item_id`, `drop_chance`) VALUES
(1, 1, 30),
(1, 3, 70),
(2, 2, 40),
(2, 4, 10),
(2, 3, 50),
(3, 2, 60),
(3, 4, 40); 