<?php

add_installer('online', 'online_plugin_install');
add_uninstaller('online', 'online_plugin_uninstall');

function online_plugin_install() {
	db()->query_once('
			CREATE TABLE IF NOT EXISTS `online_users` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `user_hash` varchar(32) NOT NULL,
			  `time_update` datetime NOT NULL,
			  PRIMARY KEY (`id`),
			  UNIQUE KEY `user_hash` (`user_hash`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	add_setval('online_time_before_reset', '180', 'Время (секунд) которое пользователь считается онайл', 'int');
}

function online_plugin_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `online_users`');
	delete_setval('online_time_before_reset');
}
