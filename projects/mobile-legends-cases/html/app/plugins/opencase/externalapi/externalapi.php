<?php

add_post('/api/activity/(([0-9]+)/)?(([0-9]+)/)?', 'externalapi_api_activity');
add_post('/api/botinventories/update/', 'externalapi_api_botinventories_update');
add_post('/api/botinventory/update/([0-9]+)/', 'externalapi_api_botinventory_update');
add_post('/api/fakeopen/', 'externalapi_api_fakeopen');
add_post('/api/qiwi/check/', 'externalapi_api_qiwi_check');
add_post('/api/itemlist/update/', 'externalapi_api_upload_items');
add_post('/api/currencies/rates/update/', 'externalapi_api_update_currencies_rates');
add_post('/api/market/tick/', 'externalapi_api_market_tick');
add_post('/api/botevents/get/', 'externalapi_api_get_bot_events');
add_post('/api/bots/get/', 'externalapi_api_get_bots');
add_post('/api/botevent/update/([0-9]+)/', 'externalapi_api_botevent_update');
add_post('/api/get/gameid/', 'externalapi_api_get_gameid');
add_post('/api/check/', 'externalapi_api_check');

function externalapi_api_check_auth() {
	if (!empty($authKey = getheader('Authorization'))) {
		if (stripos($authKey, 'basic ') === 0) {
			$authKey = substr($authKey, 6);
			if ($authKey == get_setval('api_scretkey')) {
				return;
			}
		}
	}
	header_error(401);
	$json = ['success' => false, 'error' => 'Неверный или отсутсвующий ключ'];
	echo_json($json);
}

function externalapi_api_botevent_update($args) {
	externalapi_api_check_auth();
	if (!isset($_POST['status'])) {
		$json = ['success' => false, 'error' => 'Не указан статус'];
	} else {
		$status = (int) $_POST['status'];
		if ($status < 0 || $status > 4) {
			$json = ['success' => false, 'error' => 'Указан некорректный статус'];
		} else {
			$botEvent = new botEvent($args[0]);
			if ($botEvent->get_id() != '') {
				$addition = $botEvent->get_parsed_additional();
				switch ($status) {
					case 0:
						update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, $status, 1);
						break;
					case 1:
						$botEvent->set_status($status);
						$botEvent->update_botEvent();
						break;
					case 2:
						update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, $status, 2);
						break;
					case 3:
					case 4:
						if ($status == 4) {
							$status = 3;
							$dItemStatus = 0;
							$error = 'Не удалось вывести предмет. Вы не приняли обмен.';
						} else {
							$dItemStatus = 6;
							$error = 'Не удалось вывести предмет. Повторите попытку позже.';
						}
						$itemsIds = $botEvent->get_items_array();
						foreach ($itemsIds as $itemId) {
							$invItem = new invItems($itemId);
							if ($invItem->get_id() != '') {
								$invItem->set_status(0);
								$invItem->update_invItems();
							}
						}
						update_bot_event_and_ditem_statuses_by_addition($botEvent, $addition, $status, $dItemStatus, $error);
						break;
				}
				$json = ['success' => true, 'msg' => 'Статус успешно обновлен'];
			} else {
				$json = ['success' => false, 'error' => 'Эвент с id ' . $args[0] . ' не найден'];
			}
		}
	}
	echo_json($json);
}

function externalapi_api_get_bots($args) {
	externalapi_api_check_auth();
	$bots = db()->query('SELECT * FROM opencase_bot');
	$json = ['success' => true, 'bots' => $bots];
	echo_json($json);
}

function externalapi_api_get_bot_events($args) {
	externalapi_api_check_auth();
	$needStatuses = [];
	if (isset($_POST['status'])) {
		$statuses = explode(',', $_POST['status']);
		foreach ($statuses as $status) {
			$needStatuses[(int) $status] = (int) $status;
		}
	}
	if (empty($needStatuses)) {
		$needStatuses[0] = 0;
	}
	$events = db()->query('SELECT * FROM opencase_botevents WHERE status IN (' . implode(', ', $needStatuses) . ')');
	$json = ['success' => true, 'events' => $events];
	echo_json($json);
}

function externalapi_api_market_tick($args) {
	externalapi_api_check_auth();
	$error = '';
	if (market_tick($error)) {
		$json = ['success' => true];
	} else {
		$json = ['success' => false, 'error' => $error];
	}
	echo_json($json);
}

function externalapi_api_upload_items($args) {
	externalapi_api_check_auth();
	$item = new item();
	$error = '';
	$success = $item->update_items_list($error);
	if ($success) {
		$json = ['success' => true, 'msg' => 'Предметы успешно обновлены.'];
	} else {
		$json = ['success' => false, 'error' => $error];
	}
	echo_json($json);
}

function externalapi_api_update_currencies_rates($args) {
	externalapi_api_check_auth();
	if (isset($_POST['eur'])) {
		update_setval('opencase_eur_cost', $_POST['eur']);
	}
	if (isset($_POST['usd'])) {
		update_setval('opencase_usd_cost', $_POST['usd']);
	}
	$json = ['success' => true, 'usd' => get_setval('opencase_usd_cost'), 'eur' => get_setval('opencase_eur_cost')];
	echo_json($json);
}

function externalapi_api_qiwi_check($args) {
	externalapi_api_check_auth();
	$json = array('success' => false);
	if (get_setval('deposite_qiwi_enable') == 1) {
		$nextTxnId = '';
		$nextTxnDate = '';
		do {
			$history = qiwi_history($nextTxnId, $nextTxnDate);
			if (empty($history)) {
				break;
			}
			$nextTxnId = $history['nextTxnId'];
			$nextTxnDate = $history['nextTxnDate'];
			foreach ($history['data'] as $row) {
				if ($row['status'] == 'WAITING' || empty($row['comment'])) {
					continue;
				}
				$order = selo('deposite_qiwi_orders', array('order_id' => $row['comment'], 'status' => 0), false, 1);
				if ($order['id'] > 0) {
					if ($row['status'] == 'SUCCESS') {
						$sum = $row['sum']['amount'] * $row['currencyRate'];
						qiwi_deposite_success($order, $sum);
					} else {
						qiwi_deposite_fail($order);
					}
				}
			}
		} while (!empty($nextTxnId) && !empty($nextTxnDate));
		$json['success'] = true;
	} else {
		$json['error'] = 'Платежи черезе qiwi выключены';
	}
	echo_json($json);
}

function externalapi_api_activity($args) {
	externalapi_api_check_auth();
	$json = array('success' => false);
	$interval = isset($args[1]) ? db()->nomysqlinj($args[1]) : 10;
	$count = isset($args[3]) ? db()->nomysqlinj($args[3]) : 60;
	$startTime = db()->query_once('select TIME_TO_SEC(NOW()) - TIME_TO_SEC(NOW()) % (' . $interval . ') as dat');
	$startTime = $startTime['dat'];
	$intervalsQuery = db()->query('SELECT COUNT(id) as cn, MAX(`time_drop`) AS `dt`, TIME_TO_SEC(`time_drop`) - TIME_TO_SEC(`time_drop`) % (' . $interval . ') AS `dat` FROM `opencase_droppeditems` GROUP BY `dat` ORDER BY `dt` DESC LIMIT ' . $count);
	$intevals = array();
	foreach ($intervalsQuery as $intevalQuery) {
		$intevals[$intevalQuery['dat']] = $intevalQuery;
	}
	$result = array();
	for ($i = 0; $i < $count; $i++) {
		$time = $startTime - $i * $interval;
		if (isset($intevals[$time])) {
			$result[] = array('count' => $intevals[$time]['cn'], 'dat' => $intevals[$time]['dat']);
		} else {
			$result[] = array('count' => 0, 'dat' => $time);
		}
		$json['success'] = true;
		$json['data'] = $result;
	}
	echo_json($json);
}

function externalapi_api_botinventories_update($args) {
	externalapi_api_check_auth();
	$json = array('success' => false);
	$botIns = new bot();
	$allBots = $botIns->get_bots();
	$json['bots'] = [];
	foreach ($allBots as $bot) {
		if ($bot->update_inventory_from_steam()) {
			$json['bots'][$bot->get_steam_id()] = 'Инвентарь успешно обновлен';
		} else {
			$json['bots'][$bot->get_steam_id()] = 'Не удалось обновить инвентарь бота';
		}
	}
	$json['success'] = true;
	echo_json($json);
}

function externalapi_api_botinventory_update($args) {
	externalapi_api_check_auth();
	$json = array('success' => false);

	$data = db()->query_once('select * from opencase_bot where steam_id = "' . db()->nomysqlinj($args[0]) . '"');
	if (isset($data['id'])) {
		$bot = new bot($data['id']);
		if ($bot->get_id() != '') {
			if ($bot->update_inventory_from_steam()) {
				$json['success'] = true;
				$json['msg'] = 'Инвентарь успешно обновлен';
			} else {
				$json['error'] = 'Не удалось обновить инвентарь бота';
			}
		} else {
			$json['error'] = 'Бот с id ' . $args[0] . ' не найден';
		}
	} else {
		$json['error'] = 'Бот с id ' . $args[0] . ' не найден';
	}
	echo_json($json);
}

function externalapi_api_fakeopen($args) {
	externalapi_api_check_auth();
	$json = array('success' => false);
	$user_ids = get_user_ids_by_status(100, 'rand()', 1);
	foreach ($user_ids as $i => $user_id) {
		bot_fake_open($user_id, 1, 0, 0);
	}
	$json['success'] = true;
	echo_json($json);
}

function externalapi_api_get_gameid($args) {
	externalapi_api_check_auth();
	$json = ['success' => true, 'gameid' => get_setval('opencase_gameid')];
	echo_json($json);
}

function externalapi_api_check() {
	externalapi_api_check_auth();
	$json = ['success' => true];
	echo_json($json);
}
