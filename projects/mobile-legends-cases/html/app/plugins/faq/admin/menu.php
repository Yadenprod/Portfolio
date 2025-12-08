<?php

add_admin_menu('admin_menu_faq');

function admin_menu_faq() {
	return array(
		'key' => 'faqmain',
		'name' => 'FAQ',
		'position' => 4,
		'icon' => 'fa-question',
		'menu' => array(
			array(
				'key' => 'faq',
				'icon' => 'fa-question',
				'url' => ADMINURL . '/faq/',
				'text' => 'FAQ'
			),
			array(
				'key' => 'faqadd',
				'icon' => 'fa-plus',
				'url' => ADMINURL . '/faqaddform/',
				'text' => 'Добавить вопрос'
			),
		)
	);
}
