<?php

function get_main_promo() {
	return new promocode(get_setval('promo_active_code'));
}

function is_promo($code, $type, $user_id = false) {
	if (!$user_id && is_login()) {
		$user_id = user()->get_id();
	}
	if ($user_id) {
		$promo = new promocode();
		$promo->get_from_code($code);
		if ($promo->get_code() != '' && $promo->get_enable() && $promo->get_type() == $type) {
			if ($promo->user_can_use($user_id)) {
				return $promo;
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

function use_percent_promocode($code, $sum = 0, $user_id = false) {
	if (!$user_id && is_login()) {
		$user_id = user()->get_id();
	}
	if ($user_id) {
		$promo = is_promo($code, promocode::TYPE_PERCENT, $user_id);
		if ($promo && $promo->get_use() < $promo->get_count()) {
			$user = new user($user_id);
			$promo->use_promocode($user->get_id());
			if ($sum > 0) {
				$promoSum = round($sum * ($promo->get_value() / 100));
				inc_user_balance($user, $promoSum);
				add_balance_log($user->get_id(), $promoSum, 'Бонус за использование процентного промокода: ' . $promo->get_code(), 5);
			}
			return true;
		} else {
			return false;
		}
	} else {
		return false;
	}
}
