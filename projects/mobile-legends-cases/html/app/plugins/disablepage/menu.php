<?php

add_admin_menu('admin_menu_disablepage');

function admin_menu_disablepage() {
	return array(
		'key' => 'disablesitemain',
		'name' => 'Отключение сайта',
		'position' => 4,
		'icon' => 'fa-shield',
		'menu' => array(
			array(
				'key' => 'disablesite',
				'icon' => 'fa-shield',
				'url' => ADMINURL . '/disablepage/',
				'text' => 'Настройки'
			)
		)
	);
}
