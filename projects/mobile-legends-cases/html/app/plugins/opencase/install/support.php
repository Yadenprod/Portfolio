<?php

add_installer('opencase', 'opencase_support_install');
add_uninstaller('opencase', 'opencase_support_uninstall');

function opencase_support_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `ticket` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификатор записи",
		  `theme` varchar(255) NOT NULL COMMENT "Тема тикета",
		  `game_id` int(11) NOT NULL COMMENT "Номер игры",
		  `user_id` varchar(64) NOT NULL COMMENT "id пользователя (Steam id)",
		  `status` int(11) NOT NULL COMMENT "Статус заявки",
		  `assessment` int(11) NOT NULL COMMENT "Оценка",
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`),
		  KEY `status` (`status`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `ticket_message` (
		  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT "Идентификатор записи",
		  `ticket_id` int(11) NOT NULL COMMENT "Идентификатор тикита",
		  `text` text NOT NULL COMMENT "Текст тикета",
		  `attachment` text NOT NULL COMMENT "Прикрепленные файлы",
		  `time_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "Время сообщения",
		  `from` int(11) NOT NULL COMMENT "От кого сообщение (0 - пользователь/1 - администратор)",
		  PRIMARY KEY (`id`),
		  KEY `ticket_id` (`ticket_id`),
		  KEY `from` (`from`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;');
}

function opencase_support_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `ticket`');
	db()->query_once('DROP TABLE IF EXISTS `ticket_message`');
}
