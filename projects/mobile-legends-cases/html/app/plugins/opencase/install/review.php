<?php

add_installer('opencase', 'opencase_review_install');
add_uninstaller('opencase', 'opencase_review_uninstall');

function opencase_review_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_reviews` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `user_id` int(11) NOT NULL,
          `text` text NOT NULL,
          `item_id` int(11) NOT NULL,
          `moderate` tinyint(1) NOT NULL,
          `time_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`),
          KEY `user_id` (`user_id`),
          KEY `moderate` (`moderate`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;');
}

function opencase_review_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `opencase_reviews`');
}
