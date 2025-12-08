<?php

add_installer('opencase', 'opencase_tables_install');
add_uninstaller('opencase', 'opencase_tables_uninstall');

function opencase_tables_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_case` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификационный номер кейса",
		  `name` varchar(128) NOT NULL COMMENT "Название кейса",
		  `type` int(11) NOT NULL DEFAULT "0",
		  `image` varchar(255) NOT NULL COMMENT "Изображение кейса",
		  `item_image` varchar(255) NOT NULL COMMENT "Изображение предмета на кейсе",
		  `price` int(11) NOT NULL COMMENT "Цена кейса",
		  `sale` int(11) NOT NULL COMMENT "Скидка на кейс (%)",
		  `category` int(11) NOT NULL COMMENT "Категория кейса",
		  `position` int(11) NOT NULL COMMENT "Позиция кейса в категории",
		  `rarity` int(11) NOT NULL COMMENT "Редкость кейса",
		  `enable` tinyint(1) NOT NULL COMMENT "Включить - 1 / Отключить - 0 кейс",
		  `description` text NOT NULL COMMENT "Описание кейса",
		  `label` varchar(255) NOT NULL COMMENT "Ярлык кейса",
		  `chance` int(11) NOT NULL COMMENT "Шанс окупаемости",
		  `key` varchar(16) NOT NULL COMMENT "Уникальный ключ кейса",
		  `open_count` int(11) NOT NULL COMMENT "Количество открытий кейса",
		  `max_open_count` int(11) NOT NULL COMMENT "Максимально возможное количество открытий кейса",
		  `time_limit` datetime NULL COMMENT "Время до которого доступен кейс",
		  `dep_for_open` int(11) NOT NULL COMMENT "Минимальная сумма депозита для открытия",
		  `dep_open_count` int(11) NOT NULL COMMENT "Количество бесплатных открытий депозит кейса",
		  PRIMARY KEY (`id`),
		  UNIQUE KEY `key` (`key`),
		  KEY `category` (`category`),
		  KEY `enable` (`enable`)
		) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_category` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификационный номер категории",
		  `name` varchar(128) NOT NULL COMMENT "Название категории",
		  `pos` int(11) NOT NULL COMMENT "Позиция категории",
		  `disable` int(1) NOT NULL COMMENT "Отключение отображения категории",
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_items` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификационный номер предмета",
		  `appid` int(11) NOT NULL,
		  `name` varchar(128) NOT NULL COMMENT "Название предмета",
	   	  `image` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT "Изображение предмета",
		  `quality` int(11) NOT NULL COMMENT "Качество предмета",
		  `price` float NOT NULL,
		  PRIMARY KEY (`id`),
		  KEY `quality` (`quality`),
		  UNIQUE `name` (`name`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8  AUTO_INCREMENT=1;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_itemincase` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификационный номер",
		  `case_id` int(11) NOT NULL COMMENT "ID кейса",
		  `item_id` int(11) NOT NULL COMMENT "ID предмета",
		  `chance` int(11) NOT NULL COMMENT "Шанс выпадения",
		  `count_items` int(11) NOT NULL COMMENT "Количество возможных выпадений",
		  `position` int(11) NOT NULL COMMENT "Позиция предмета в кейсе",
		  `enabled` tinyint(1) NOT NULL COMMENT "Включен / Отключен",
		  `withdrawable`tinyint(1) NOT NULL DEFAULT "1",
		  `usable`tinyint(1) NOT NULL DEFAULT "1",
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_bot` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `steam_id` bigint(20) NOT NULL,
		  `name` varchar(64) NOT NULL,
		  `password` varchar(255) NOT NULL,
		  `shared_secret` varchar(255) NOT NULL,
		  `identity_secret` varchar(255) NOT NULL,
		  `api_key` varchar(255) NOT NULL,
		  `status` tinyint(1) NOT NULL,
		  `enabled` tinyint(1) NOT NULL,
		  `offer_url` varchar(128) NOT NULL,
		  `market_enable` tinyint(1) NOT NULL,
		  `market_key` varchar(255) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_invitems` (
		  `id` bigint(20) NOT NULL,
		  `classid` bigint(20) NOT NULL,
		  `instanceid` bigint(20) NOT NULL,
		  `amount` int(11) NOT NULL,
		  `pos` int(11) NOT NULL,
		  `appid` int(11) NOT NULL,
		  `icon_url` varchar(512) NOT NULL,
		  `icon_url_large` varchar(512) NOT NULL,
		  `icon_drag_url` varchar(512) NOT NULL,
		  `name` varchar(255) NOT NULL,
		  `market_hash_name` varchar(255) NOT NULL,
		  `market_name` varchar(255) NOT NULL,
		  `name_color` varchar(6) NOT NULL,
		  `background_color` varchar(6) NOT NULL,
		  `type` varchar(128) NOT NULL,
		  `tradable` int(11) NOT NULL,
		  `marketable` int(11) NOT NULL,
		  `commodity` int(11) NOT NULL,
		  `market_tradable_restriction` int(11) NOT NULL,
		  `contextid` int(11) NOT NULL,
		  `price` float NOT NULL,
		  `bot_id` int(11) NOT NULL,
		  `status` int(11) NOT NULL,
		  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
		  PRIMARY KEY (`id`),
		  KEY `bot_id` (`bot_id`),
		  KEY `status` (`status`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_botevents` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `bot_id` int(11) NOT NULL,
		  `event` int(11) NOT NULL,
		  `additional` text NOT NULL,
		  `items_id` text NOT NULL,
		  `status` int(11) NOT NULL,
		  `time_add` datetime NOT NULL,
		  `time_start` datetime NOT NULL,
		  `iteration` int(11) NOT NULL,
		  PRIMARY KEY (`id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_opencases` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `case_id` int(11) NOT NULL,
		  `item_id` int(11) NOT NULL,
		  `case_price` int(11) NOT NULL,
		  `time_open` datetime NOT NULL,
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`,`case_id`,`item_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_balancelog` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `change` float NOT NULL,
		  `comment` text NOT NULL,
		  `time` datetime NOT NULL,
		  `type` int(11) NOT NULL,
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`,`type`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_contracts` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `items_id` varchar(255) NOT NULL,
		  `item_id` int(11) NOT NULL,
		  `items_price` float NOT NULL,
		  `time_open` datetime NOT NULL,
		  `image` text NOT NULL,
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_droppeditems` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `item_id` int(11) NOT NULL,
		  `quality` int(11) NOT NULL,
		  `price` float NOT NULL,
		  `time_drop` datetime NOT NULL,
		  `status` int(11) NOT NULL,
		  `from` int(11) NOT NULL,
		  `fast` tinyint(1) NOT NULL,
		  `offer_id` bigint(20) NOT NULL,
		  `bot_id` int(11) NOT NULL,
		  `withdrawable`tinyint(1) NOT NULL DEFAULT "1",
		  `usable`tinyint(1) NOT NULL DEFAULT "1",
		  `error` VARCHAR(255) NULL DEFAULT NULL,
		  `analog_id` int(11) NULL DEFAULT NULL,
		  PRIMARY KEY (`id`),
		  KEY `id` (`id`),
		  KEY `user_id` (`user_id`),
		  KEY `status` (`status`),
		  KEY `bot_id` (`bot_id`),
		  KEY `fast` (`fast`)
		) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;');
}

function opencase_tables_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `opencase_case`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_category`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_items`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_itemincase`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_bot`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_invitems`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_botevents`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_opencases`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_balancelog`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_contracts`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_droppeditems`');
}
