<?php

const MARKET_SITE_URL = [730 => 'https://market.csgo.com', 570 => 'https://market.dota2.net'];
const MARKET_TRADE_STAGE_NEW = 1;
const MARKET_TRADE_STAGE_ITEM_GIVEN = 2;
const MARKET_TRADE_STAGE_TIMED_OUT = 5;
const LOCK_FILE_PATH = CMSFOLDER . '.market_event_lock';

function market_tick(&$error) {
	if (!isset(MARKET_SITE_URL[get_setval('opencase_gameid')])) {
		$error = 'Выбранная игра не поддреживает работу с маркетом';
		return false;
	} elseif (!is_file(LOCK_FILE_PATH) || (time() - filectime(LOCK_FILE_PATH)) > 180) {
		touch(LOCK_FILE_PATH);
		try {
			check_buyed_market_items();
			try_buy_and_send_market_items();
			unlink(LOCK_FILE_PATH);
			return true;
		} catch (\Exception $ex) {
			$error = $ex->getMessage();
			unlink(LOCK_FILE_PATH);
			return false;
		}
	} else {
		$error = 'Предыдущий запрос все еще в процессе';
		return false;
	}
}

function check_buyed_market_items() {
	$botEventInst = new botEvent();
	$allbotEvents = $botEventInst->get_botEvents('event = 50 AND status = 1');
	foreach ($allbotEvents as $botEvent) {
		$addition = $botEvent->get_parsed_additional();
		if (empty($addition->marketCustomId)) {
			update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, 3, 6, 'Не удалось вывести предмет. Повторите попытку позже.');
		} else {
			$info = get_market_buy_info_by_custom_id($botEvent->get_bot_class()->get_decrypted_market_key(), $addition->marketCustomId);
			if (!empty($info)) {
				if ($info['stage'] == MARKET_TRADE_STAGE_ITEM_GIVEN) {
					update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, 2, 2);
				} elseif ($info['stage'] == MARKET_TRADE_STAGE_TIMED_OUT) {
					update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, 3, 6, 'Не удалось вывести предмет. Повторите попытку позже.');
				}
			}
		}
	}
}

function try_buy_and_send_market_items() {
	$botEventInst = new botEvent();
	$allbotEvents = $botEventInst->get_botEvents('event = 50 AND status = 0');
	foreach ($allbotEvents as $botEvent) {
		$addition = $botEvent->get_parsed_additional();
		if (empty($addition->ditem)) {
			$botEvent->set_status(3);
			$botEvent->update_botEvent();
			continue;
		}
		$dItem = new droppedItem($addition->ditem);
		if ($dItem->get_id() == '') {
			$botEvent->set_status(3);
			$botEvent->update_botEvent();
			continue;
		}
		if (empty($addition->tradeUrl)) {
			update_bot_event_and_ditem_statuses($botEvent, $dItem, 3, 6, 'Не удалось вывести предмет. У вас указана некорректная ссылка на обмен');
			continue;
		}
		$queryStr = parse_url($addition->tradeUrl, PHP_URL_QUERY);
		$queryArray = [];
		parse_str($queryStr, $queryArray);
		if (!isset($queryArray['partner']) || !isset($queryArray['token'])) {
			update_bot_event_and_ditem_statuses($botEvent, $dItem, 3, 6, 'Не удалось вывести предмет. У вас указана некорректная ссылка на обмен');
			continue;
		}
		$item = $dItem->get_item_class();
		$currentPriceMul = 1;
		$marketItems = get_items_by_market_hash_name($botEvent->get_bot_class()->get_decrypted_market_key(), $item->get_name(), $currentPriceMul);
		if (empty($marketItems)) {
			check_bot_event_iteration_count($botEvent, $dItem);
			continue;
		}
		$marketItem = select_market_item_from_array($marketItems, $item->get_price() * $currentPriceMul);
		if (empty($marketItem)) {
			check_bot_event_iteration_count($botEvent, $dItem);
			continue;
		}
		$customId = $botEvent->get_id() . time();
		$error = '';
		$marketItemId = buy_market_item_for($botEvent->get_bot_class()->get_decrypted_market_key(), $marketItem, $queryArray['partner'], $queryArray['token'], $customId, $error);
		if (!$marketItemId) {
			if (!empty($error)) {
				update_bot_event_and_ditem_statuses($botEvent, $dItem, 3, 6, $error);
			} else {
				check_bot_event_iteration_count($botEvent, $dItem);
			}
			continue;
		}
		$addition->marketCustomId = $customId;
		$botEvent->set_additional(json_encode($addition));
		$botEvent->set_status(1);
		$botEvent->update_botEvent();
	}
}

function check_bot_event_iteration_count($botEvent, $dItem) {
	$iteration = $botEvent->get_iteration() + 1;
	$botEvent->set_iteration($iteration);
	if ($iteration >= 10) {
		update_bot_event_and_ditem_statuses($botEvent, $dItem, 3, 6, 'Не удалось вывести предмет. Повторите попытку позже.');
	} else {
		$botEvent->update_botEvent();
	}
}

function select_market_item_from_array($marketItems, $currentPrice) {
	$minPrice = PHP_INT_MAX;
	$currentItem = null;
	foreach ($marketItems as $marketItem) {
		if ($marketItem['price'] < $minPrice) {
			$minPrice = $marketItem['price'];
			$currentItem = $marketItem;
		}
	}
	if (empty($currentItem) || $currentItem['price'] > $currentPrice * 1.25) {
		return false;
	}
	return $currentItem;
}

function get_market_buy_info_by_custom_id($marketApiKey, $customId) {
	$params = [
		'custom_id' => $customId
	];
	$result = market_api_call($marketApiKey, '/api/v2/get-buy-info-by-custom-id', $params);
	if ($result && $result['success'] == true && !empty($result['data'])) {
		return $result['data'];
	}
	return false;
}

function get_items_by_market_hash_name($marketApiKey, $hashName, &$currentPriceMul) {
	$params = [
		'hash_name' => $hashName
	];
	$result = market_api_call($marketApiKey, '/api/v2/search-item-by-hash-name', $params);
	if ($result && $result['success'] == true && $result['currency'] == 'RUB' && !empty($result['data'])) {
		switch ($result['currency']) {
			case 'RUB':
				$currentPriceMul = 100;
				break;
			case 'EUR':
				$currentPriceMul = 1000 / get_setval('opencase_eur_cost');
				break;
			case 'USD':
				$currentPriceMul = 1000 / get_setval('opencase_usd_cost');
				break;
			default:
				return false;
		}
		return $result['data'];
	}
	return false;
}

function buy_market_item_for($marketApiKey, $marketItem, $partner, $token, $customId, &$error) {
	$params = [
		'hash_name' => $marketItem['market_hash_name'],
		'price' => $marketItem['price'],
		'partner' => $partner,
		'token' => $token,
		'custom_id' => $customId
	];
	$result = market_api_call($marketApiKey, '/api/v2/buy-for', $params);
	if ($result) {
		if ($result['success'] == true) {
			return $result['id'];
		}
		if (!empty($result['error'])) {
			$error = $result['error'];
		}
	}
	return false;
}

function market_api_call($marketApiKey, $endpoint, $params = []) {
	usleep(200000);
	$params['key'] = $marketApiKey;
	$url = MARKET_SITE_URL[get_setval('opencase_gameid')] . $endpoint . '?' . http_build_query($params, '', '&');
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
	curl_setopt($ch, CURLOPT_HEADER, false);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_REFERER, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
	$result = curl_exec($ch);
	$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	curl_close($ch);
	if ($httpcode != 200) {
		return false;
	}
	return json_decode($result, true);
}

function check_market_api_key($marketApiKey) {
	$result = market_api_call($marketApiKey, '/api/v2/test');
	if ($result && $result['success'] == true) {
		return true;
	}
	return false;
}

function update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, $botEventStatus, $dItemStatus, $error = '') {
	$botEvent->set_status($botEventStatus);
	$botEvent->update_botEvent();
	if (!empty($addition->ditem)) {
		$dItem = new droppedItem($addition->ditem);
		if ($dItem->get_id() != '') {
			$dItem->set_status($dItemStatus);
			$dItem->set_error($error);
			$dItem->update_droppedItem();
		}
	}
}

function update_bot_event_and_ditem_statuses($botEvent, $dItem, $botEventStatus, $dItemStatus, $error = '') {
	$botEvent->set_status($botEventStatus);
	$botEvent->update_botEvent();
	$dItem->set_status($dItemStatus);
	$dItem->set_error($error);
	$dItem->update_droppedItem();
}
