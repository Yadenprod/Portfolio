<?php

add_admin_menu('opencase_plugin_items_menu');

function opencase_plugin_items_menu() {
	return array(
		'key' => 'itemsmain',
		'icon' => 'fa-gavel',
		'name' => 'Предметы',
		'position' => 3.1,
		'menu' => array(
			array(
				'key' => 'items',
				'icon' => 'fa-gavel',
				'url' => ADMINURL . '/opencase/items/',
				'text' => 'Управление предметами'
			),
			array(
				'key' => 'itemadd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/opencase/itemaddform/',
				'text' => 'Добавить предмет'
			),
			array(
				'key' => 'itemsearch',
				'icon' => 'fa-search',
				'url' => ADMINURL . '/opencase/itemsearch/',
				'text' => 'Поиск предметов'
			)
		)
	);
}
