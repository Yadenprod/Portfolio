<?php

add_app('/ref/i/((.+)/)?', 'ref_i');

function ref_i($args) {
	$steam_id = isset($args[1]) ? $args[1] : false;
	if ($steam_id && !is_login()) {
		$referrer = get_user_by_steam_id(mb_strtolower($steam_id));
		if ($referrer) {
			setcookie('referrer', $referrer->get_id(), time() + get_setval('cookies_life_time'), '/', $_SERVER['HTTP_HOST']);
		}
		redirect_srv_msg('', '/');
	} else {
		redirect_srv_msg('', '/');
	}
	exit();
}
