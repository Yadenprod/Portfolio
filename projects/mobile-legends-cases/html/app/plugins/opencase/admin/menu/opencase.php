<?php

add_admin_menu('opencase_plugin_main_menu');

function opencase_plugin_main_menu() {
	return array(
		'key' => 'opencasemain',
		'icon' => 'fa-bank',
		'name' => 'Опенкейс',
		'position' => 3.01,
		'menu' => array(
			array(
				'key' => 'opencasesettings',
				'icon' => 'fa-wrench',
				'url' => ADMINURL . '/opencase/settings/',
				'text' => 'Настройки'
			),
			array(
				'key' => 'opencaseopencases',
				'icon' => 'fa-suitcase',
				'url' => ADMINURL . '/opencase/opencases/',
				'text' => 'Открытые кейсы'
			),
			array(
				'key' => 'opencasecontracts',
				'icon' => 'fa-file-text-o',
				'url' => ADMINURL . '/opencase/contracts/',
				'text' => 'Контракты'
			),
			array(
				'key' => 'opencasedepoite',
				'icon' => 'fa-money',
				'url' => ADMINURL . '/opencase/deposite/',
				'text' => 'Депозиты'
			),
			array(
				'key' => 'opencasewithdraw',
				'icon' => 'fa-ticket',
				'url' => ADMINURL . '/opencase/withdraw/',
				'text' => 'Выводы'
			)
		)
	);
}
