<?php

add_post('/api/mainpromo/', 'opencase_get_main_promo');
add_post('/api/percent/promo/check/', 'opencase_check_percent_promo');

function opencase_get_main_promo() {
	$promo = get_main_promo();
	if ($promo->get_id() != '' && $promo->get_enable()) {
		$json = [
			'success' => true,
			'promo' => [
				'value' => $promo->get_value(),
				'left' => $promo->get_left(),
				'count' => $promo->get_count(),
				'code' => $promo->get_code(),
			]
		];
	} else {
		$json = ['success' => false];
	}
	echo_json($json);
}

function opencase_check_percent_promo() {
	$json = ['success' => false];
	if (is_login()) {
		if (!empty($_POST['promo'])) {
			$promo = new promocode();
			$promo->get_from_code($_POST['promo']);
			if ($promo->get_code() != '' && $promo->get_enable() && $promo->get_type() == promocode::TYPE_PERCENT) {
				if ($promo->get_use() < $promo->get_count()) {
					if ($promo->user_can_use(user()->get_id())) {
						$json['success'] = true;
						$json['percent'] = $promo->get_value();
						$json['msg'] = 'Бонус ' . $promo->get_value() . '% к сумме пополнения';
					} else {
						$json['error'] = 'Вы уже использовали этот код';
					}
				} else {
					$json['error'] = 'Промокод уже был активирован максимальное количество раз';
				}
			} else {
				$json['error'] = 'Такого промокода не существует';
			}
		} else {
			$json['error'] = 'Вы не ввели промокод';
		}
	} else {
		$json['error'] = 'Вы не авторизовались на сайте';
	}
	echo_json($json);
}
