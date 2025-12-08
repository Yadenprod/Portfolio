<?php

add_app('/profile/(([^\/]+)/)?', 'user_profile');
add_app('/case/([^\/]+)/', 'user_case');
add_app('/livetrade/', 'user_livetrade');
add_app('/top/', 'user_top');
add_app('/contracts/', 'user_contracts');

function user_profile($args) {
	set_content('');
	set_title('Профиль');
	set_title_page('Профиль');
	set_tpl('profile.php');
	add_data('steam_id', isset($args[1]) ? $args[1] : '');
}

function user_case($args) {
	set_content('');
	set_title('Кейс');
	set_title_page('Кейс');
	set_tpl('case.php');
	add_data('case_name', isset($args[0]) ? $args[0] : '');
}

function user_livetrade($args) {
	set_content('');
	set_title('Live-трейды');
	set_title_page('Live-трейды');
	set_tpl('livetrade.php');
}

function user_top($args) {
	set_content('');
	set_title('Топ');
	set_title_page('Топ');
	set_tpl('top.php');
}

function user_contracts($args) {
	set_content('');
	set_title('Контракты');
	set_title_page('Контракты');
	set_tpl('contracts.php');
}
