<?php

add_installer('modeupgarde', 'modeupgarde_plugin_install');
add_uninstaller('modeupgarde', 'modeupgarde_plugin_uninstall');

function modeupgarde_plugin_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_upgrades` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `item_id` int(11) NOT NULL,
		  `source_id` int(11) NOT NULL,
		  `target_id` int(11) NOT NULL,
		  `status` int(11) NOT NULL,
		  `image` text NOT NULL,
		  `balance` int(11) NOT NULL,
		  `created_at` datetime NOT NULL DEFAULT NOW(),
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	add_setval('opencase_count_upgrades', '0', 'Количество проведенных апгрейдов', 'int');
}

function modeupgarde_plugin_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `opencase_upgrades`');
	delete_setval('opencase_count_upgrades');
}
