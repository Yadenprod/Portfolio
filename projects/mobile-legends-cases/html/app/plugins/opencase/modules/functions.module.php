<?php

function get_last_dropped_items() {
	$dItems = new droppedItem();
	return $dItems->get_newDroppedItems('', 'DESC', 40);
}

function get_case_category() {
	$caseCategory = new caseCategory();
	return $caseCategory->get_caseCategorys('', 'pos ASC');
}

function get_user_drops($user_id, $where = false, $page = 0, $count = 18) {
	$droppedItem = new droppedItem();
	return $droppedItem->get_droppedItems('user_id = ' . db()->nomysqlinj($user_id) . ($where ? ' and ' . $where : ''), '(status = 0 OR status = 6) DESC, id DESC', $count > 0 ? (db()->nomysqlinj($page) * $count) . ', ' . $count : '');
}

function get_user_contracts($user_id, $page = 0, $count = 8) {
	$contract = new contract();
	return $contract->get_contracts('user_id = ' . db()->nomysqlinj($user_id), 'id DESC', $count > 0 ? (db()->nomysqlinj($page) * $count) . ', ' . $count : '');
}

function get_last_trade($count = 20) {
	$droppedItem = new droppedItem();
	return $droppedItem->get_droppedItems('status = 2', 'id DESC', $count);
}

function get_top_users($limit = 50, $page = 0) {
	$sql = 'SELECT user_id, (SUM(CASE WHEN status = 2 THEN price ELSE 0 END) - (SELECT SUM(sum) FROM `opencase_deposite` WHERE user_id = opencase_droppeditems.user_id)) as profit, COUNT(CASE WHEN `from` > 0 THEN 1 END) as cases,  COUNT(CASE WHEN `from` = 0 THEN 1 END) as contracts FROM opencase_droppeditems WHERE user_id NOT IN (SELECT user_id FROM users_data WHERE value = 1 AND user_field_id = (SELECT id FROM user_fields WHERE `key` = "top_disabled" LIMIT 1)) GROUP BY user_id HAVING profit > 0 ORDER BY profit DESC LIMIT ' . ($page * $limit) . ', ' . $limit;
	$res = db()->query($sql);
	$users = [];
	foreach ($res as $row) {
		$user = new user($row['user_id']);
		$users[] = [
			'id' => $user->get_id(),
			'name' => $user->get_name(),
			'cases' => (int) $row['cases'],
			'contracts' => (int) $row['contracts'],
			'profit' => (int) $row['profit'],
			'steam_id' => $user->get_data('steam_id'),
			'image' => $user->get_data('image')
		];
	}
	return $users;
}

function sortItemInCasseByClass($a, $b) {
	if ($a->get_item_class()->get_quality() == $b->get_item_class()->get_quality()) {
		return 0;
	}
	return ($a->get_item_class()->get_quality() < $b->get_item_class()->get_quality()) ? -1 : 1;
}

function sortItemInCasseByPrice($a, $b) {
	if ($a->get_item_class()->get_price() == $b->get_item_class()->get_price()) {
		return 0;
	}
	return ($a->get_item_class()->get_price() < $b->get_item_class()->get_price()) ? 1 : -1;
}

function sortItemInCasseByPosition($a, $b) {
	if ($a->get_position() == $b->get_position()) {
		return 0;
	}
	return ($a->get_position() < $b->get_position()) ? -1 : 1;
}

function sortItemByPrice($a, $b) {
	if ($a['price'] == $b['price']) {
		return 0;
	}
	return ($a['price'] < $b['price']) ? -1 : 1;
}

function get_count_opencase($case_id, $user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user_id = user()->get_id();
		} else {
			return 0;
		}
	}
	$case_id = db()->nomysqlinj($case_id);
	$user_id = db()->nomysqlinj($user_id);
	$countCases = db()->query_once('select count(1) from opencase_opencases INNER JOIN opencase_droppeditems ON opencase_opencases.item_id = opencase_droppeditems.id where opencase_opencases.user_id = ' . $user_id . ' and opencase_opencases.case_id = ' . $case_id . ' and opencase_droppeditems.from > 0');
	return $countCases['count(1)'] ? intval($countCases['count(1)']) : 0;
}

function get_count_case_per_period($case_id, $user_id = false) {
	$user_id = $user_id ? $user_id : is_login() ? user()->get_id() : 0;
	$case_id = db()->nomysqlinj($case_id);
	$user_id = db()->nomysqlinj($user_id);
	$countCases = db()->query_once('select count(id) from opencase_opencases where user_id = ' . $user_id . ' and case_id = ' . $case_id . ' and time_open >= DATE_SUB(NOW(), INTERVAL '.get_setval('opencase_deposit_check_day').' DAY)');
	return $countCases['count(id)'] ? intval($countCases['count(id)']) : 0;
}

function get_time_before_deposit_case_free_open($case_id, $user_id = false) {
	$user_id = $user_id ? $user_id : is_login() ? user()->get_id() : 0;
	$case_id = db()->nomysqlinj($case_id);
	$user_id = db()->nomysqlinj($user_id);
	$dateData = db()->query_once('select TIMESTAMPDIFF(SECOND, NOW(), DATE_ADD(time_open, INTERVAL '.get_setval('opencase_deposit_check_day').' DAY)) as before_open from opencase_opencases where user_id = ' . $user_id . ' and case_id = ' . $case_id . ' and time_open >= DATE_SUB(NOW(), INTERVAL '.get_setval('opencase_deposit_check_day').' DAY) ORDER BY time_open ASC LIMIT 1');
	return max(0, $dateData['before_open'] ? intval($dateData['before_open']) : 0);
}

function get_count_deposite_per_period($user_id = false) {
	$user_id = $user_id ? $user_id : is_login() ? user()->get_id() : 0;
	$user_id = db()->nomysqlinj($user_id);
	$sumDep = db()->query_once('select sum(`sum`) as sm from opencase_deposite where user_id = ' . $user_id . ' and time_add >=  DATE_SUB(NOW(), INTERVAL '.get_setval('opencase_deposit_check_day').' DAY)');
	return $sumDep['sm'] ? intval($sumDep['sm']) : 0;
}

function can_open_free_case($case, $count_open = false, $sum_deposite = false, $user_id = false) {
	$case_id = $case->get_id();
	$user_id = $user_id ? $user_id : is_login() ? user()->get_id() : 0;
	$user_id = db()->nomysqlinj($user_id);
	if (!$count_open)
		$count_open = get_count_case_per_period($case_id, $user_id);
	if (!$sum_deposite) {
		$sum_deposite = get_count_deposite_per_period($user_id);
	}
	return $count_open < $case->get_dep_open_count() && $sum_deposite >= $case->get_dep_for_open();
}

function get_count_open_cases() {
	return number_format(get_setval('opencase_count_open_case'), 0, '', ' ');
}

function get_count_create_contracts() {
	return number_format(get_setval('opencase_count_contracts'), 0, '', ' ');
}

function get_count_reg_users() {
	return number_format(get_setval('opencase_count_users'), 0, '', ' ');
}

function get_count_onlie() {
	if (function_exists('get_online')) {
		return get_online();
	} else {
		return 0;
	}
}

function get_count_today_online() {
	if (function_exists('get_today_online')) {
		return get_today_online();
	} else {
		return 0;
	}
}

function get_count_today_open_cases() {
	$count = db()->query_once('SELECT COUNT(1) FROM opencase_droppeditems WHERE `from` > 0 && time_drop > CURDATE()');
	return $count['COUNT(1)'] ?? 0;
}

function get_count_today_create_contracts() {
	$count = db()->query_once('SELECT COUNT(1) FROM opencase_droppeditems WHERE `from` = 0 && time_drop > CURDATE()');
	return $count['COUNT(1)'] ?? 0;
}

function is_escrow($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user_id = user()->get_id();
		} else {
			$user_id = 0;
		}
	}
	$user = new user($user_id);
	if ($user->get_id() != '') {
		$url_part = explode('&', $user->get_data('trade_link'));
		if (empty($url_part[0])) {
			return false;
		}
		$partner_url = explode('?partner=', $url_part[0]);
		
		$token = explode('=', end($url_part));
		if ($token[0] == 'token') {
			$token = end($token);
			$urljson = file_get_contents('https://api.steampowered.com/IEconService/GetTradeHoldDurations/v1/?key=' . get_setval('steamauth_apiKey') . '&format=json&steamid_target=' . $partner . '&trade_offer_access_token=' . $token);
			$data = json_decode($urljson)->response;
			if (isset($data->their_escrow)) {
				$escrow = (int) $data->their_escrow->escrow_end_duration_seconds;
				if ($escrow == 0) {
					return true;
				} else {
					return true;
				}
			} else {
				return false;
			}
		} else {
			return false;
		}
	} else {
		return false;
	}
}

function get_pre_delete_category() {
	$category = new caseCategory();
	$category->set_parametrs(-1, 'Удаленные кейсы', 10000, 1);
	return $category;
}

function file_get_contents_https($url) {
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
	curl_setopt($ch, CURLOPT_HEADER, false);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_REFERER, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
	$result = curl_exec($ch);
	curl_close($ch);
	return $result;
}

function get_weighted_arithmetic_mean($data) {
	$avg = array_sum($data) / count($data);
	$sumErr = 0;
	$err = [];
	foreach ($data as $key => $price) {
		$err[$key] = ($avg - $price) ** 2;
		$sumErr += $err[$key];
	}
	if ($sumErr == 0) {
		return $avg;
	}
	$newSum = 0;
	$sumQ = 0;
	foreach ($data as $key => $price) {
		$q = (1 - ($err[$key] / $sumErr)) ** 6;
		$sumQ += $q;
		$newSum += $price * $q;
	}
	return $newSum / $sumQ;
}
