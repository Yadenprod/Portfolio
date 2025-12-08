<?php

add_loader('apitheme_loader');

function apitheme_loader() {
	if ($_SERVER['REQUEST_METHOD'] != 'GET' || is_admin_uri()) {
		return;
	}
	$excepts = ['/api/', '/?login', '/steamauth/logout/', '/ref/i/', '/deposite/unicall'];
	$url = uri();
	foreach ($excepts as $except) {
		if (stripos($url, $except) === 0) {
			return;
		}
	}
	set_content('');
	set_tpl('index.php');
	wp()->render();
	wsexit();
}
