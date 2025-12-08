<?php

const DROPPED_ITEM_STATUS_UPGRADED = 10;
const DROPPED_ITEM_FROM_UPGRADE = -1;

function get_avail_upgrade_result_list($page, $limit, $minPrice, $search = '', $maxPrice = 0, $order = 'ASC') {
	$itemInst = new item();
	$where = [];
	if ($minPrice > 0) {
		$where[] = 'price >= ' . db()->nomysqlinj($minPrice);
	}
	if ($maxPrice > 0 && $maxPrice >= $minPrice) {
		$where[] = 'price <= ' . db()->nomysqlinj($maxPrice);
	}
	if (!empty($search)) {
		$where[] = 'name LIKE "%' . db()->nomysqlinj($search) . '%"';
	}
	if (get_setval('opencase_gameid') == 730) {
		$where[] = 'quality IN (2,3,4,5,6,12)';
	}
	return $itemInst->get_items(implode(' AND ', $where), 'price ' . $order, ($page - 1) * $limit . ', ' . $limit);
}

//function get_user_count_upgrades($user) {
//	$count = db()->query_once('select count(id) from opencase_upgrades where user_id = "' . $user->get_id() . '"');
//	return $count['count(id)'];
//}

function get_user_count_upgrades($user) {
	$count = db()->query_once('SELECT 
		COUNT(CASE WHEN status = ' . upgrade::STATUS_SUCCESS . ' THEN 1 ELSE NULL END) AS won,
		COUNT(CASE WHEN status = ' .upgrade::STATUS_FAIL . ' THEN 1 ELSE NULL END) AS lost
		FROM opencase_upgrades WHERE user_id = "' . $user->get_id() .'"'
	);
	return [
		'won' => $count['won'],
		'lost' => $count['lost']
	];
}
