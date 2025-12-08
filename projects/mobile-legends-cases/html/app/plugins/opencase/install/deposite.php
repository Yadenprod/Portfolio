<?php

add_installer('opencase', 'deposite_plugin_install');
add_uninstaller('opencase', 'deposite_plugin_uninstall');

function deposite_plugin_install() {
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `opencase_deposite` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `sum` float NOT NULL,
		  `num` int(11) NOT NULL,
		  `from` int(11) NOT NULL,
		  `status` int(11) NOT NULL,
		  `time_add` datetime NOT NULL, 
		  PRIMARY KEY (`id`),
		  KEY `user_id` (`user_id`)
		) ENGINE=InnoDB  DEFAULT CHARSET=utf8;
		');
	db()->query_once('
		CREATE TABLE IF NOT EXISTS `deposite_qiwi_orders` (
		  `id` int(11) NOT NULL AUTO_INCREMENT,
		  `user_id` int(11) NOT NULL,
		  `sum` int(11) NOT NULL,
		  `order_id` varchar(64) NOT NULL,
		  `status` int(11) NOT NULL,
		  `promo` varchar(255) NOT NULL,
		  `time_add` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
		  `time_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
		  PRIMARY KEY (`id`),
		  UNIQUE KEY `order_id` (`order_id`),
		  KEY `user_id` (`user_id`)
		) ENGINE=InnoDB DEFAULT CHARSET=utf8;
		');
	add_setval('deposite_qiwi_enable', '0', 'Включить способ оплаты Qiwi', 'bool');
	add_setval('deposite_qiwi_secret', '', 'Секретный ключ Qiwi', 'text');
	add_setval('deposite_qiwi_merchant_id', '', 'Номер Qiwi кошелька', 'text');
	add_setval('deposite_interkassa_enable', '0', 'Включить способ оплаты Interkassa', 'bool');
	add_setval('deposite_interkassa_merchant_id', '', 'ID магазина Interkassa', 'text');
	add_setval('deposite_interkassa_secret', '', 'Секретный ключ Interkassa', 'text');
	add_setval('deposite_unitpay_enable', '0', 'Включить способ оплаты Unipay', 'bool');
	add_setval('deposite_unitpay_merchant_id', '', 'ID магазина Unipay', 'text');
	add_setval('deposite_unitpay_secret', '', 'Секретный ключ Unipay', 'text');
	add_setval('deposite_freekassa_enable', '0', 'Включить способ оплаты Freekassa', 'bool');
	add_setval('deposite_freekassa_merchant_id', '', 'ID магазина Freekassa', 'text');
	add_setval('deposite_freekassa_secret_1', '', 'Секретный ключ №1 Freekassa', 'text');
	add_setval('deposite_freekassa_secret_2', '', 'Секретный ключ №2 Freekassa', 'text');
}

function deposite_plugin_uninstall() {
	db()->query_once('DROP TABLE IF EXISTS `opencase_deposite`');
	db()->query_once('DROP TABLE IF EXISTS `deposite_qiwi_orders`');
	delete_setval('deposite_qiwi_enable');
	delete_setval('deposite_qiwi_secret');
	delete_setval('deposite_qiwi_merchant_id');
	delete_setval('deposite_interkassa_enable');
	delete_setval('deposite_interkassa_merchant_id');
	delete_setval('deposite_interkassa_secret');
	delete_setval('deposite_unitpay_enable');
	delete_setval('deposite_unitpay_merchant_id');
	delete_setval('deposite_unitpay_secret');
	delete_setval('deposite_freekassa_enable');
	delete_setval('deposite_freekassa_merchant_id');
	delete_setval('deposite_freekassa_secret_1');
	delete_setval('deposite_freekassa_secret_2');
}
