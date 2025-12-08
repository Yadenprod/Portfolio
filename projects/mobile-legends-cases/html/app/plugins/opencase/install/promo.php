<?php

add_installer('opencase', 'opencase_promo_install');
add_uninstaller('opencase', 'opencase_promo_uninstall');

function opencase_promo_install() {
	db()->query_once('
			CREATE TABLE IF NOT EXISTS `promo_code` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `code` varchar(64) NOT NULL,
			  `type` int(11) NOT NULL DEFAULT "0",
			  `value` int(11) NOT NULL,
			  `count` int(11) NOT NULL,
			  `use` int(11) NOT NULL,
			  `enable` tinyint(1) NOT NULL,
			  `case_id` int(11) NULL DEFAULT NULL,
			  PRIMARY KEY (`id`),
			  UNIQUE KEY `code` (`code`),
			  KEY `enable` (`enable`)
			) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
			CREATE TABLE IF NOT EXISTS `promo_use` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `promo_id` int(11) NOT NULL,
			  `user_id` int(11) NOT NULL,
			  PRIMARY KEY (`id`),
			  KEY `promo_id` (`promo_id`,`user_id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	add_setval('promo_active_code', '0', 'Активный промокод', 'int');
}

function opencase_promo_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `promo_code`');
	db()->query_once('DROP TABLE IF EXISTS `promo_use`');
	delete_setval('promo_active_code');
}
