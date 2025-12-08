<?php

add_post('/api/user/', 'opencase_get_current_user');
add_post('/api/user/availdrop/', 'opencase_get_avail_user_drop');
add_post('/api/user/profile/(([^\/]+)/)?', 'opencase_get_user_profile');
add_post('/api/user/top/', 'opencase_get_users_top');
add_post('/api/user/top/drop/', 'opencase_get_users_top_by_drop');

function opencase_get_current_user() {
	$user = user();
	$json = [
		'success' => true,
		'user' => [
			'login' => $user->is_login(),
			'id' => $user->get_id(),
			'name' => $user->get_name(),
			'image' => $user->get_data('image'),
			'steamId' => $user->get_data('steam_id'),
			'balance' => get_user_balance($user)
		]
	];
	echo_json($json);
}

function opencase_get_avail_user_drop() {
	$json = ['success' => false];
	if (is_login()) {
		$json['success'] = true;
		$json['items'] = [];
		$items = get_user_drops(user()->get_id(), 'usable = 1 AND (status = 0 OR status = 6)', 0, 0);
		foreach ($items as $item) {
			$json['items'][] = [
				'id' => $item->get_id(),
				'price' => $item->get_price(),
				'name' => $item->get_item_name(),
				'image' => $item->get_item_class()->get_steam_image(),
				'imageAlt' => $item->get_item_class()->get_name(),
				'rarity' => $item->get_item_class()->get_css_quality_class(),
			];
		}
	}
	echo_json($json);
}

function opencase_get_user_profile($args) {
	$json = ['success' => false];
	$steamId = isset($args[1]) ? $args[1] : '';
	$isOtherUserProfile = true;
	if (is_login() && (empty($steamId) || $steamId == user()->get_data('steam_id'))) {
		$user = user();
		$isOtherUserProfile = false;
	} else {
		$user = get_user_by_steam_id($steamId);
	}
	if ($user) {
		$json['success'] = true;
		$json['profile'] = [
			'isOther' => $isOtherUserProfile,
			'counts' => [
				'contract' => get_user_count_contracts($user),
				'case' => get_user_count_cases($user),
			],
			'id' => $user->get_id(),
			'name' => $user->get_name(),
			'steamId' => $user->get_data('steam_id'),
			'image' => $user->get_data('image'),
			'timeFromReg' => get_user_time_from_reg_text($user),
			'favoriteCase' => false,
			'bestDrop' => false
		];
		$json['profile']['counts'] = array_merge($json['profile']['counts'], stats::addAditionalUserStatsArray($user));
		if (!$isOtherUserProfile) {
			$json['profile']['tradeLink'] = $user->get_data('trade_link');
			$json['profile']['referral'] = [
				'count' => get_user_referrals_count(),
				'percent' => get_user_percent(),
				'deposit' => get_user_refferals_deposite(),
				'profit' => get_user_ref_profit(),
			];
		}
		$case = get_user_favorite_case($user);
		if ($case) {
			$json['profile']['favoriteCase'] = [
				'id' => $case->get_id(),
				'name' => $case->get_name(),
				'rarity' => $case->get_rarity_css(),
				'key' => $case->get_key(),
				'sale' => $case->get_total_sale(),
				'price' => $case->get_price(),
				'salePrice' => $case->get_sale_price(),
				'image' => $case->get_src_image() != '/uploads/' ? $case->get_src_image() : false,
			];
		}
		$bestDrop = get_user_best_drop($user);
		if ($bestDrop) {
			$json['profile']['bestDrop'] = [
				'id' => $bestDrop->get_id(),
				'price' => $bestDrop->get_price(),
				'name' => $bestDrop->get_item_name(),
				'image' => $bestDrop->get_item_class()->get_steam_image(),
				'imageAlt' => $bestDrop->get_item_class()->get_name(),
				'rarity' => $bestDrop->get_item_class()->get_css_quality_class(),
			];
		}
	}
	echo_json($json);
}

function opencase_get_users_top() {
	$limit = 10;
	$page = !empty($_POST['page']) ? ((int) $_POST['page']) : 0;
	$top = get_top_users($limit, $page);
	$json = [
		'success' => true,
		'top' => $top,
		'hasMore' => count($top) >= $limit
	];
	echo_json($json);
}

function opencase_get_users_top_by_drop() {
	$timeLimit = max((!empty($_POST['timeLimit']) ? ((int) $_POST['timeLimit']) : 0), 0);
	$limit = max(min((!empty($_POST['limit']) ? ((int) $_POST['limit']) : 5), 10), 1);
	$where = 'time_drop <= NOW()';
	if ($timeLimit > 0) {
		$where .= ' AND time_drop >= (DATE_SUB(NOW(), INTERVAL ' . $timeLimit . ' SECOND))';
	}
	$dItem = new droppedItem();
	$items = $dItem->get_droppedItems($where, 'price DESC', $limit);
	$json = [
		'success' => true,
		'top' => []
	];
	foreach ($items as $item) {
		$json['top'][] = [
			'id' => $item->get_id(),
			'price' => $item->get_price(),
			'name' => $item->get_item_name(),
			'image' => $item->get_item_class()->get_steam_image(),
			'rarity' => $item->get_item_class()->get_css_quality_class(),
			'user' => [
				'id' => $item->get_user_class()->get_id(),
				'name' => $item->get_user_class()->get_name(),
				'steam_id' => $item->get_user_class()->get_data('steam_id'),
				'image' => $item->get_user_class()->get_data('image')
			]
		];
	}
	echo_json($json);
}
