<?php

add_loader('online_loader');

function online_loader() {
	online_update();
}

function online_update() {
	$count = db()->query_once('select count(id) from online_users where user_hash = "' . get_user_online_hash() . '"');
	if ($count['count(id)'] > 0) {
		db()->query_once('UPDATE online_users SET `time_update` = NOW() WHERE user_hash = "' . get_user_online_hash() . '"');
	} else {
		db()->query_once('INSERT INTO online_users (user_hash, time_update) VALUES ("' . get_user_online_hash() . '", NOW())');
	}
}

function get_user_online_hash() {
	return md5(getip() . (isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : ''));
}
