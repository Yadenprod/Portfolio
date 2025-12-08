<?php

add_installer('modebattlesolo', 'modebattle_plugin_install');
add_uninstaller('modebattlesolo', 'modebattle_plugin_uninstall');

function modebattle_plugin_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_battle` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `creator_id` int(11) NOT NULL,
		  `participant_id` int(11) NULL DEFAULT NULL,
		  `winner_id` int(11) NULL DEFAULT NULL,
		  `case_id` int(11) NOT NULL,
		  `additional` text NOT NULL,
		  `status` int(11) NOT NULL,
		  `price` int(11) NOT NULL,
		  `finished_at` datetime NULL,
		  PRIMARY KEY (`id`),
		  KEY `creator_id` (`creator_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_battle_cases` (
		  `case_id` int(11) NOT NULL,
		  `position` int(11) NOT NULL,
		  PRIMARY KEY (`case_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;');
	add_setval('opencase_count_battles', '0', 'Количество проведенных битв за кейсы', 'int');
}

function modebattle_plugin_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `opencase_battle`');
	db()->query_once('DROP TABLE IF EXISTS `opencase_battle_cases`');
	delete_setval('opencase_count_battles');
}
