<?php

add_admin_menu('opencase_plugin_users_menu');

function opencase_plugin_users_menu() {
	return array(
		'key' => 'usersmain',
		'icon' => 'fa-users',
		'name' => 'Пользователи',
		'position' => 3.3,
		'menu' => array(
			array(
				'key' => 'users',
				'icon' => 'fa-users',
				'url' => ADMINURL . '/opencase/users/',
				'text' => 'Управление пользов.'
			),
			array(
				'key' => 'useradd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/opencase/useraddform/',
				'text' => 'Добавить пользователя'
			),
			array(
				'key' => 'usersearch',
				'icon' => 'fa-search',
				'url' => ADMINURL . '/opencase/usersearch/',
				'text' => 'Поиск пользователей'
			),
			array(
				'key' => 'userfake',
				'icon' => 'fa-gift',
				'url' => ADMINURL . '/opencase/fakeopen/',
				'text' => 'Фейк открытия'
			)
		)
	);
}
