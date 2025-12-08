<?php

add_post('/api/deposit/types/', 'opencase_get_avail_deposit_types');

function opencase_get_avail_deposit_types() {
	$json = ['success' => false];
	if (is_login()) {
		$count = db()->query_once('select max(num) from opencase_deposite where user_id=' . user()->get_id());
		$json['num'] = $count['max(num)'] + 1;
		$json['types'] = [
			'interkassa' => ['enable' => get_setval('deposite_interkassa_enable'), 'merchantId' => get_setval('deposite_interkassa_merchant_id')],
			'freekassa' => ['enable' => get_setval('deposite_freekassa_enable')],
			'qiwi' => ['enable' => get_setval('deposite_qiwi_enable')],
			'unitpay' => ['enable' => get_setval('deposite_unitpay_enable')]
		];
		$json['success'] = true;
	}
	echo_json($json);
}
