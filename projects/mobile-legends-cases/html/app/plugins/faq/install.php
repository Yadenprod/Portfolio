<?php

add_installer('faq', 'faq_plugin_install');
add_uninstaller('faq', 'faq_plugin_uninstall');

function faq_plugin_install() {
	db()->query_once('
			CREATE TABLE IF NOT EXISTS `faq` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `question` text NOT NULL,
			  `answer` text NOT NULL,
			  `enabled` tinyint(1) NOT NULL,
			  `position` int(11) NOT NULL,
			  PRIMARY KEY (`id`)
			) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
			');
	$pageData = [
		'namepage' => 'faq',
		'title' => 'FAQ',
		'title_page' => 'Вопрос-ответ',
		'meta_des' => "",
		'meta_key' => "",
		'content' => "",
		'tpl' => 'faq.php',
		'url' => '/faq/'
	];
	ins('webpage', $pageData);
}

function faq_plugin_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `faq`');
	db()->query_once("DELETE FROM `webpage` WHERE `namepage` IN ('faq')");
}
