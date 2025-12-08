<?php

add_post('/api/livetrade/', 'opencase_get_livetrades');

function opencase_get_livetrades() {
	$json = [
		'success' => true,
		'trades' => []
	];
	$limit = 10;
	$page = !empty($_POST['page']) ? ((int) $_POST['page']) : 0;
	$items = get_last_trade(($page * $limit) . ', ' . $limit);
	foreach ($items as $item) {
		$json['trades'][] = [
			'id' => $item->get_id(),
			'image' => $item->get_item_class()->get_steam_image('54f', '32f'),
			'name' => $item->get_item_class()->get_name(),
			'rarity' => $item->get_item_class()->get_css_quality_class(),
			'timeDrop' => $item->get_format_time_drop(),
			'botSteamId' => $item->get_bot_class()->get_steam_id(),
			'user' => [
				'steamId' => $item->get_user_class()->get_data('steam_id'),
				'image' => $item->get_user_class()->get_data('image'),
				'name' => $item->get_user_class()->get_name()
			],
		];
	}
	$json['hasMore'] = count($items) >= $limit;
	echo_json($json);
}
