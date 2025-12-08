<?php

function get_online() {
	$count = db()->query_once('select count(id) from online_users where time_update > Now()- INTERVAL ' . get_setval('online_time_before_reset') . ' SECOND');
	return $count['count(id)'] ? $count['count(id)'] : 0;
}

function get_today_online() {
	$count = db()->query_once('select count(id) from online_users where time_update > CURDATE()');
	return $count['count(id)'] ? $count['count(id)'] : 0;
}
