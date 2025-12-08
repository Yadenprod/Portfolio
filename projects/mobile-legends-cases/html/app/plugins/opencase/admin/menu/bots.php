<?php

add_admin_menu('opencase_plugin_bots_menu');

function opencase_plugin_bots_menu() {
	return array(
		'key' => 'botsmain',
		'icon' => 'fa-gears',
		'name' => 'Боты',
		'position' => 3.2,
		'menu' => array(
			array(
				'key' => 'bots',
				'icon' => 'fa-cog',
				'url' => ADMINURL . '/opencase/bots/',
				'text' => 'Управление ботами'
			),
			array(
				'key' => 'botadd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/opencase/botaddform/',
				'text' => 'Добавить бота'
			),
			array(
				'key' => 'botistems',
				'icon' => 'fa-briefcase',
				'url' => ADMINURL . '/opencase/botitems/',
				'text' => 'Инвентарь ботов'
			),
			array(
				'key' => 'botevents',
				'icon' => 'fa-server',
				'url' => ADMINURL . '/opencase/botevents/',
				'text' => 'Задачи ботов'
			)
		)
	);
}
