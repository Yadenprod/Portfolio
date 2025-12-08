<?php

add_admin_menu('opencase_plugin_support_menu');

function opencase_plugin_support_menu() {
	$countTickets = db()->query_once('select count(id) from ticket where status = 0 or status = 4');
	$countViewTickets = db()->query_once('select count(id) from ticket where status = 1');
	$countAdminsTickets = db()->query_once('select count(id) from ticket where status = 7');
	$countCloseTickets = db()->query_once('select count(id) from ticket where status = 5 or status = 6');
	$countActiveTickets = db()->query_once('select count(id) from ticket where status = 2 or status = 3 or status = 8');
	return array(
		'key' => 'supportmain',
		'icon' => 'fa-warning',
		'name' => 'Тех. поддержка (' . $countTickets['count(id)'] . ')',
		'position' => 3.4,
		'menu' => array(
			array(
				'key' => 'support',
				'icon' => 'fa-warning',
				'url' => ADMINURL . '/support/',
				'text' => 'Новые сообщения (' . $countTickets['count(id)'] . ')'
			),
			array(
				'key' => 'supportview',
				'icon' => 'fa-eye',
				'url' => ADMINURL . '/support/view/',
				'text' => 'Просмотренные (' . $countViewTickets['count(id)'] . ')'
			),
			array(
				'key' => 'supportadmins',
				'icon' => 'fa-user-secret',
				'url' => ADMINURL . '/support/admins/',
				'text' => 'Администратор (' . $countAdminsTickets['count(id)'] . ')'
			),
			array(
				'key' => 'supportactive',
				'icon' => 'fa-anchor',
				'url' => ADMINURL . '/support/active/',
				'text' => 'Активные (' . $countActiveTickets['count(id)'] . ')'
			),
			array(
				'key' => 'supportclose',
				'icon' => 'fa-lock',
				'url' => ADMINURL . '/support/close/',
				'text' => 'Закрытые (' . $countCloseTickets['count(id)'] . ')'
			)
		)
	);
}
