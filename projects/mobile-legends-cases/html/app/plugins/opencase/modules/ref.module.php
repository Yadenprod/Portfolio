<?php

function get_bonus($user_id) {
	$referral = new user($user_id);
	$referrer = new user($_COOKIE['referrer']);
	if ($referrer && !test_vacbanned($referral->get_data('steam_id')) && test_csgo($referral->get_data('steam_id')) && test_user_lvl($referral->get_data('steam_id')) && test_time_from_reg($referral->get_id()) && $referral->get_id() != $referrer->get_id()) {
		db()->query_once('INSERT INTO `referral_user` (`referrer_id`, `referral_id`) VALUES ("' . $referrer->get_id() . '", "' . $referral->get_id() . '");');
		if (get_setval('ref_referral_rewards') > 0) {
			inc_user_balance($referral, get_setval('ref_referral_rewards'));
			add_balance_log($referral->get_id(), get_setval('ref_referral_rewards'), 'Вознаграждение нового пользователя, пришедшего по реферальному коду пользователя №' . $referrer->get_id(), 3);
		}
		if (get_setval('ref_referrer_rewards') > 0) {
			inc_user_balance($referrer, get_setval('ref_referrer_rewards'));
			add_balance_log($referrer->get_id(), get_setval('ref_referrer_rewards'), 'Вознаграждение реферера, за привлечение пользователя №' . $referral->get_id(), 4);
		}
	}
}

function get_referrer($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user = get_user();
			$user_id = $user->get_id();
		} else {
			return false;
		}
	}
	$referrer = db()->query_once('select * from referral_user where referral_id = "' . $user_id . '"');
	if ($referrer['id'] != '') {
		$user = new user($referrer['referrer_id']);
		return $user;
	} else {
		return false;
	}
}

function is_have_referrer_code() {
	return isset($_COOKIE['referrer']) && $_COOKIE['referrer'] != '' && !get_referrer($_COOKIE['referrer']);
}

function get_user_lvl($steam_id) {
	$urljson = file_get_contents('http://api.steampowered.com/IPlayerService/GetSteamLevel/v1?key=' . get_setval('steamauth_apiKey') . '&steamid=' . $steam_id);
	$data = (array) json_decode($urljson)->response;
	if (is_array($data) && isset($data['player_level'])) {
		return $data['player_level'];
	} else {
		return false;
	}
}

function get_ref_have_csgo($steam_id) {
	$urljson = file_get_contents('http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=' . get_setval('steamauth_apiKey') . '&steamid=' . $steam_id);
	$data = (array) json_decode($urljson)->response;
	if (isset($data['games']) && is_array($data['games'])) {
		$haveCSGO = false;
		foreach ($data['games'] as $game) {
			if ($game->appid == 730) {
				$haveCSGO = true;
			}
		}
		return $haveCSGO;
	} else {
		return false;
	}
}

function get_vacbanned($steam_id) {
	$urljson = file_get_contents('http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=' . get_setval('steamauth_apiKey') . '&steamids=' . $steam_id);
	$data = (array) json_decode($urljson)->players;
	if (is_array($data) && isset($data[0])) {
		return $data[0]->VACBanned;
	} else {
		return false;
	}
}

function test_vacbanned($steam_id, $setting = 'ref_referral_test_vacban') {
	if (get_setval($setting) == 1) {
		return get_vacbanned($steam_id);
	} else {
		return false;
	}
}

function test_csgo($steam_id, $setting = 'ref_referral_test_csgo') {
	if (get_setval($setting) == 1) {
		return get_ref_have_csgo($steam_id);
	} else {
		return true;
	}
}

function test_time_from_reg($user_id, $setting_enabled = 'ref_referral_test_time_create', $setting_min_time = 'ref_referral_mintime_from_create') {
	$user = new user($user_id);
	if (get_setval($setting_enabled) == 1) {
		return ((((time() - $user->get_data('timecreated')) / 60) / 60) / 24) > get_setval($setting_min_time);
	} else {
		return true;
	}
}

function test_user_lvl($steam_id, $setting = 'ref_referral_min_lvl') {
	return get_user_lvl($steam_id) >= get_setval($setting);
}

function get_user_referrals_count($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user = get_user();
			$user_id = $user->get_id();
		}
	}
	$count = db()->query_once('select count(id) from referral_user where `referrer_id` = ' . db()->nomysqlinj($user_id));
	return $count['count(id)'] ? $count['count(id)'] : 0;
}

function get_user_percent($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user = get_user();
			$user_id = $user->get_id();
		}
	}
	return get_setval('ref_referrer_rewards_from_deposite');
}

function get_user_refferals_deposite($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user = get_user();
			$user_id = $user->get_id();
		}
	}
	$usersQ = db()->query('select referral_id from referral_user where referrer_id = ' . $user_id);
	$users = array();
	foreach ($usersQ as $userQ) {
		array_push($users, $userQ['referral_id']);
	}
	if (count($users) > 0) {
		$sum = db()->query_once('select sum(`sum`) as sm from opencase_deposite where user_id in (' . implode(',', $users) . ')');
		$sum = $sum['sm'] ? $sum['sm'] : 0;
	} else {
		$sum = 0;
	}
	return $sum;
}

function get_user_ref_profit($user_id = false) {
	if (!$user_id) {
		if (is_login()) {
			$user = get_user();
			$user_id = $user->get_id();
		}
	}
	$sum = db()->query_once('select sum(`change`) as ch from opencase_balancelog where `user_id` = ' . db()->nomysqlinj($user_id) . ' and `type` = 4');
	return $sum['ch'] ? $sum['ch'] : 0;
}
