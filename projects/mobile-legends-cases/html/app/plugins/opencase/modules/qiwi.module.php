<?php

function qiwi_deposite_success($qiwi, $sum = false) {
	if ($qiwi['id'] > 0 && $qiwi['status'] == 0) {
		upd('deposite_qiwi_orders', array('status' => 1), array('id' => $qiwi['id']));
		$deposite = new deposite();
		$sum = $sum ? (int) $sum : (int) $qiwi['sum'];
		$user_id = (int) $qiwi['user_id'];
		$user = new user($user_id);
		$status = 3;
		$num = db()->nomysqlinj(str_replace('USER:' . $user_id . '_', '', $qiwi['order_id']));
		$deposite->set_parametrs('', $user->get_id(), $sum, $num, 3, $status);
		$deposite->add_deposite();
		inc_user_balance($user, $sum);
		add_balance_log($user->get_id(), $sum, 'Депозит через платежную систему: ' . $deposite->get_from_text() . '', 0);
		if (!empty($qiwi['promo'])) {
			use_percent_promocode($qiwi['promo'], $sum, $user->get_id());
		}
		$referrer = get_referrer($user->get_id());
		if ($referrer) {
			$refSum = round($sum * (get_setval('ref_referrer_rewards_from_deposite') / 100));
			inc_user_balance($referrer, $refSum);
			add_balance_log($referrer->get_id(), $refSum, 'Вознаграждение за депозит №' . $num . ' рефферала: ' . $user->get_name() . ' (' . $user->get_steam_id() . ')', 4);
		}
	}
}

function qiwi_deposite_fail($qiwi) {
	if ($qiwi['id'] > 0 && $qiwi['status'] == 0) {
		upd('deposite_qiwi_orders', array('status' => 2), array('id' => $qiwi['id']));
	}
}

function qiwi_history($nextTxnId = '', $nextTxnDate = '') {
	if (get_setval('deposite_qiwi_enable')) {
		$url = 'https://edge.qiwi.com/payment-history/v2/persons/' . get_setval('deposite_qiwi_merchant_id') . '/payments';
		$headers = array(
			'Accept: application/json',
			'Content-Type: application/json',
			'Authorization: Bearer ' . get_setval('deposite_qiwi_secret')
		);
		$params = array(
			'rows' => 50,
			'operation' => 'IN'
		);
		if (!empty($nextTxnId) && !empty($nextTxnDate)) {
			$params['nextTxnId'] = $nextTxnId;
			$params['nextTxnDate'] = $nextTxnDate;
		}
		$ch = curl_init($url . '?' . http_build_query($params));
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
		curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
		$output = curl_exec($ch);
		curl_close($ch);
		if ($output) {
			$output = json_decode($output, true);
			if (count($output['data']) <= 0) {
				$output = false;
			}
		}
		return $output;
	} else {
		return false;
	}
}
