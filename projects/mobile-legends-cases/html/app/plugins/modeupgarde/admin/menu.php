<?php

add_admin_menu('admin_menu_opencase_mode_upgrade');

function admin_menu_opencase_mode_upgrade() {
	return [
		'key' => 'upgrademodemenu',
		'name' => 'Апгрейд',
		'position' => 3.03,
		'icon' => 'fa-gamepad',
		'menu' => [
			[
				'key' => 'upgrademode',
				'icon' => 'fa-gamepad',
				'url' => ADMINURL . '/mode/upgrade/',
				'text' => 'Апгрейд'
			],
		]
	];
}
