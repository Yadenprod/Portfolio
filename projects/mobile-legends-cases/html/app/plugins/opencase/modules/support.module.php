<?php

function get_count_new_user_messge() {
	if (is_login()) {
		$user = get_user();
	} else {
		$user = new user();
	}
	$count = db()->query_once('select count(id) as cnt from ticket where user_id = "' . $user->get_data('steam_id') . '" and status = "3"');
	return $count['cnt'];
}
