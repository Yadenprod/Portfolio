<?php

add_app('/deposite/intercall/', 'deposite_intercall');
add_app('/deposite/unicall.*', 'deposite_unicall');
add_app('/deposite/uniform/', 'deposite_uniform');
add_app('/deposite/freecall/', 'deposite_freecall');
add_app('/deposite/freeform/', 'deposite_freeform');
add_app('/deposite/qiwiform/', 'deposite_qiwiform');

function deposite_intercall() {
	if (get_setval('deposite_interkassa_enable')) {
		depositeLog();
		if (isset($_POST['ik_co_id']) && isset($_POST['ik_inv_st']) && isset($_POST['ik_x_user_id']) && isset($_POST['ik_am']) && isset($_POST['ik_sign']) && $_POST['ik_am'] > 0) {
			$dataSet = array();
			foreach ($_POST as $key => $post) {
				if (is_int(strripos($key, 'ik_')) && strripos($key, 'ik_') == 0) {
					$dataSet[$key] = $post;
				}
			}
			if ($_POST['ik_sign'] == getInterSignature($dataSet)) {
				$deposite = new deposite();
				$sum = isset($_POST['ik_am']) && $_POST['ik_am'] ? intval(db()->nomysqlinj($_POST['ik_am'])) : 0;
				$user_id = isset($_POST['ik_x_user_id']) && $_POST['ik_x_user_id'] ? db()->nomysqlinj($_POST['ik_x_user_id']) : 1;
				$user = new user($user_id);
				$status = 6;
				foreach ($deposite->get_status_key_array() as $key => $statusKey) {
					if ($statusKey == $_POST['ik_inv_st'])
						$status = $key;
				}
				$num = db()->nomysqlinj(str_replace($user_id . '_', '', $_POST['ik_pm_no']));
				$deposite->set_parametrs('', $user->get_id(), $sum, $num, 0, $status);
				$deposite->add_deposite();
				if ($status == 3) {
					inc_user_balance($user, $sum);
					add_balance_log($user->get_id(), $sum, 'Депозит через платежную систему: ' . $deposite->get_from_text() . '', 0);
					if (isset($_POST['ik_x_promo'])) {
						use_percent_promocode($_POST['ik_x_promo'], $sum, $user->get_id());
					}
					$referrer = get_referrer($user->get_id());
					if ($referrer) {
						$refSum = round($sum * (get_setval('ref_referrer_rewards_from_deposite') / 100));
						inc_user_balance($referrer, $refSum);
						add_balance_log($referrer->get_id(), $refSum, 'Вознаграждение за депозит №' . $num . ' рефферала: ' . $user->get_name() . ' (' . $user->get_data('steam_id') . ')', 4);
					}
				}
				exit();
			}
		}
	}
}

function deposite_unicall() {
	if (get_setval('deposite_freekassa_enable')) {
        $ips = array('168.119.157.136', '168.119.60.227', '138.201.88.124', '178.154.197.79');
		if (in_array(getip(), $ips)) {
			depositeLog();
			if (!empty($_POST['MERCHANT_ID']) && $_POST['MERCHANT_ID'] == get_setval('deposite_freekassa_merchant_id') && !empty($_POST['AMOUNT']) && !empty($_POST['MERCHANT_ORDER_ID']) && !empty($_POST['SIGN']) && $_POST['SIGN'] == getFreeSignature($_POST['AMOUNT'], $_POST['MERCHANT_ORDER_ID']) && !empty($_POST['us_uid']) && !empty($_POST['intid'])) {
				$deposite = new deposite();
				$sum = (int) $_POST['AMOUNT'];
				$user_id = (int) $_POST['us_uid'];
				$user = new user($user_id);
				$status = 3;
				$num = db()->nomysqlinj(str_replace($user_id . '_', '', $_POST['MERCHANT_ORDER_ID']));
				$deposite->set_parametrs('', $user->get_id(), $sum, $num, 2, $status);
				$deposite->add_deposite();
				inc_user_balance($user, $sum);
				add_balance_log($user->get_id(), $sum, 'Депозит через платежную систему: ' . $deposite->get_from_text() . '', 0);
				if (!empty($_POST['us_promo'])) {
					use_percent_promocode($_POST['us_promo'], $sum, $user->get_id());
				}
				$referrer = get_referrer($user->get_id());
				if ($referrer) {
					$refSum = round($sum * (get_setval('ref_referrer_rewards_from_deposite') / 100));
					inc_user_balance($referrer, $refSum);
					add_balance_log($referrer->get_id(), $refSum, 'Вознаграждение за депозит №' . $num . ' рефферала: ' . $user->get_name() . ' (' . $user->get_data('steam_id') . ')', 4);
				}
			}
			exit();
		}
	}
}

function deposite_uniform() {
	if (is_login() && get_setval('deposite_freekassa_enable')) {
		$count = db()->query_once('select max(num) from opencase_deposite where user_id = ' . user()->get_id());
		$count = $count['max(num)'] + 1;
		$data = array(
			'm=' . get_setval('deposite_freekassa_merchant_id'),
			'oa=' . (int) $_POST['amount'],
			'o=' . user()->get_id() . '_' . $count,
            'currency=RUB',
			's=' . getFreeFormSignature((int) $_POST['amount'], user()->get_id() . '_' . $count),
			'us_uid=' . user()->get_id()
		);
		if (!empty($_POST['ik_x_promo'])) {
			array_push($data, 'us_promo=' . $_POST['ik_x_promo']);
		}
		redirect('https://pay.freekassa.ru/?' . implode('&', $data));
	} else {
		redirect('/');
	}
}

function deposite_freecall() {
	if (get_setval('deposite_freekassa_enable')) {
		$ips = array('168.119.157.136', '168.119.60.227', '138.201.88.124', '178.154.197.79');
		if (in_array(getip(), $ips)) {
			depositeLog();
			if (!empty($_POST['MERCHANT_ID']) && $_POST['MERCHANT_ID'] == get_setval('deposite_freekassa_merchant_id') && !empty($_POST['AMOUNT']) && !empty($_POST['MERCHANT_ORDER_ID']) && !empty($_POST['SIGN']) && $_POST['SIGN'] == getFreeSignature($_POST['AMOUNT'], $_POST['MERCHANT_ORDER_ID']) && !empty($_POST['us_uid']) && !empty($_POST['intid'])) {
				$deposite = new deposite();
				$sum = (int) $_POST['AMOUNT'];
				$user_id = (int) $_POST['us_uid'];
				$user = new user($user_id);
				$status = 3;
				$num = db()->nomysqlinj(str_replace($user_id . '_', '', $_POST['MERCHANT_ORDER_ID']));
				$deposite->set_parametrs('', $user->get_id(), $sum, $num, 2, $status);
				$deposite->add_deposite();
				inc_user_balance($user, $sum);
				add_balance_log($user->get_id(), $sum, 'Депозит через платежную систему: ' . $deposite->get_from_text() . '', 0);
				if (!empty($_POST['us_promo'])) {
					use_percent_promocode($_POST['us_promo'], $sum, $user->get_id());
				}
				$referrer = get_referrer($user->get_id());
				if ($referrer) {
					$refSum = round($sum * (get_setval('ref_referrer_rewards_from_deposite') / 100));
					inc_user_balance($referrer, $refSum);
					add_balance_log($referrer->get_id(), $refSum, 'Вознаграждение за депозит №' . $num . ' рефферала: ' . $user->get_name() . ' (' . $user->get_data('steam_id') . ')', 4);
				}
			}
			exit();
		}
	}
}

function deposite_freeform() {
	if (is_login() && get_setval('deposite_freekassa_enable')) {
		$count = db()->query_once('select max(num) from opencase_deposite where user_id = ' . user()->get_id());
		$count = $count['max(num)'] + 1;
		$data = array(
			'm=' . get_setval('deposite_freekassa_merchant_id'),
			'oa=' . (int) $_POST['amount'],
			'o=' . user()->get_id() . '_' . $count,
			's=' . getFreeFormSignature((int) $_POST['amount'], user()->get_id() . '_' . $count),
			'us_uid=' . user()->get_id()
		);
		if (!empty($_POST['ik_x_promo'])) {
			array_push($data, 'us_promo=' . $_POST['ik_x_promo']);
		}
		redirect('https://pay.freekassa.ru/merchant/cash.php?' . implode('&', $data));
	} else {
		redirect('/');
	}
}

function deposite_qiwiform() {
	if (is_login() && get_setval('deposite_qiwi_enable')) {
		$count = db()->query_once('select count(id) from deposite_qiwi_orders where user_id = ' . user()->get_id());
		$count = $count['count(id)'] + 1;
		$sum = !empty($_POST['amount']) && (int) $_POST['amount'] > 0 ? (int) $_POST['amount'] : 100;
		$oreder_id = 'USER:' . user()->get_id() . '_' . $count;
		$data = array(
			'amountInteger=' . $sum,
			'amountFraction=0',
			'currency=643',
			'extra[\'comment\']=' . $oreder_id,
			'extra[\'account\']=' . get_setval('deposite_qiwi_merchant_id'),
			'blocked[0]=account',
			'blocked[1]=comment'
		);
		$promo = '';
		if (!empty($_POST['ik_x_promo'])) {
			$promo = $_POST['ik_x_promo'];
		}
		ins('deposite_qiwi_orders', array('status' => 0, 'sum' => $sum, 'user_id' => user()->get_id(), 'order_id' => $oreder_id, 'promo' => $promo));
		redirect('https://qiwi.com/payment/form/99?' . implode('&', $data));
	} else {
		redirect('/');
	}
}

function getInterSignature($dataSet) {
	$secretKey = get_setval('deposite_interkassa_secret');
	unset($dataSet['ik_sign']);
	ksort($dataSet, SORT_STRING);
	array_push($dataSet, $secretKey);
	$signString = implode(':', $dataSet);
	$sign = base64_encode(md5($signString, true));
	return $sign;
}

function getUniSignature($method, $dataSet) {
	$secretKey = get_setval('deposite_unitpay_secret');
	ksort($dataSet);
	unset($dataSet['sign']);
	unset($dataSet['signature']);
	array_push($dataSet, $secretKey);
	array_unshift($dataSet, $method);
	return hash('sha256', join('{up}', $dataSet));
}

function getUniFormSignature($account, $currency, $desc, $sum) {
	$hashStr = $account . '{up}' . $currency . '{up}' . $desc . '{up}' . $sum . '{up}' . get_setval('deposite_unitpay_secret');
	return hash('sha256', $hashStr);
}

function getFreeSignature($sum, $order_id) {
	return md5(get_setval('deposite_freekassa_merchant_id') . ':' . $sum . ':' . get_setval('deposite_freekassa_secret_2') . ':' . $order_id);
}

function getFreeFormSignature($sum, $order_id) {
	return md5(get_setval('deposite_freekassa_merchant_id') . ':' . $sum . ':' . get_setval('deposite_freekassa_secret_1') . ':RUB:' . $order_id);
}

function depositeLog() {
	$log = 'GET : {';
	foreach ($_GET as $key => $value) {
		if (!is_array($value))
			$log .= $key . ' : ' . $value . ', ';
		else {
			$log .= $key . ' : {';
			foreach ($value as $elemKey => $elem) {
				$log .= $elemKey . ' : ' . $elem . ', ';
			}
			$log .= '}';
		}
	}
	$log .= '}, POST : {';
	foreach ($_POST as $key => $value) {
		if (!is_array($value))
			$log .= $key . ' : ' . $value . ', ';
		else {
			$log .= $key . ' : {';
			foreach ($value as $elemKey => $elem) {
				$log .= $elemKey . ' : ' . $elem . ', ';
			}
			$log .= '}';
		}
	}
	$log .= '}';
}