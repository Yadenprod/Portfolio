<?php

add_admin_menu('opencase_plugin_case_menu');

function opencase_plugin_case_menu() {
	return array(
		'key' => 'casemain',
		'icon' => 'fa-suitcase',
		'name' => 'Кейсы',
		'position' => 3.02,
		'menu' => array(
			array(
				'key' => 'case',
				'icon' => 'fa-suitcase',
				'url' => ADMINURL . '/opencase/case/',
				'text' => 'Управление кейсами'
			),
			array(
				'key' => 'caseadd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/opencase/caseaddform/',
				'text' => 'Добавить кейс'
			),
			array(
				'key' => 'casecategory',
				'icon' => 'fa-th-list',
				'url' => ADMINURL . '/opencase/category/',
				'text' => 'Категории кейсов'
			),
			array(
				'key' => 'caseposition',
				'icon' => 'fa-sort',
				'url' => ADMINURL . '/opencase/caseposition/',
				'text' => 'Управление позициями'
			)
		)
	);
}
