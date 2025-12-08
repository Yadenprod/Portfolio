<?php

add_admin_menu('opencase_plugin_review_menu');

function opencase_plugin_review_menu() {
	return array(
		'key' => 'reviewmain',
		'icon' => 'fa-pencil-square-o',
		'name' => 'Отзывы',
		'position' => 3.6,
		'menu' => array(
			array(
				'key' => 'review',
				'icon' => 'fa-pencil-square-o',
				'url' => ADMINURL . '/review/',
				'text' => 'Список отзывов'
			),
			array(
				'key' => 'reviewadd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/review/addform/',
				'text' => 'Добавить отзыв'
			)
		)
	);
}
