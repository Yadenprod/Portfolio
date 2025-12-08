<?php

// переходим на VK авторизацию
//add_app('/\?login.*', 'steamauth_login');
add_app('/steamauth/logout/', 'steamauth_logout');

function steamauth_login() {
    try {
        $openid = new LightOpenID('https://' . get_setval('steamauth_loginDomen'));

        if (!$openid->mode) {
            if (isset($_GET['login'])) {
                $openid->identity = 'https://steamcommunity.com/openid';
                header('Location: ' . $openid->authUrl());
                wsexit();
            }
        } elseif ($openid->mode == 'cancel') {

        } else {

            if ($openid->validate()) {
                $id = $openid->identity;
                $ptn = "/^https:\/\/steamcommunity\.com\/openid\/id\/(7[0-9]{15,25}+)$/";
                preg_match($ptn, $id, $matches);

                $url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=' . get_setval('steamauth_apiKey') . '&steamids=' . $matches[1];
                $json_object = file_get_contents($url);
                $json_decoded = json_decode($json_object);

                foreach ($json_decoded->response->players as $player) {
                    user_login_steam($player); // todo было user_login до добавления файла vkauth.php
                }
            } else {
                add_log('', 'Not valid enter');
                redirect_srv_msg('', '/');
            }
        }
    } catch (ErrorException $e) {
        echo $e->getMessage();
    }
}

function steamauth_logout() {
    user_logout_steam(); // todo было user_logout до добавления файла vkauth.php
    redirect_srv_msg('', '/');
}

//function get_user() { // todo остался только в vkauth.php
//    if (is_login()) {
//        return user();
//    }
//    return false;
//}

function user_login_steam($user) { // todo было user_login до добавления файла vkauth.php
    if (($authuser = get_user_by_steam_id($user->steamid))) {
        $authuser->set_name(mysqli_real_escape_string(db()->db, $user->personaname));
        $authuser->set_data('image', $user->avatarfull);
        $authuser->set_data('timecreated', $user->timecreated);
        $authuser->update();
        add_log($user->steamid, 'login');
    } else {
        $authuser = new user();
        $authuser->set_name(mysqli_real_escape_string(db()->db, $user->personaname));
        $authuser->add();
        $authuser->set_data('steam_id', $user->steamid);
        $authuser->set_data('image', $user->avatarfull);
        $authuser->set_data('timecreated', $user->timecreated);
        $authuser->update();
        if (get_setval('opencase_regbalance') > 0 && !test_vacbanned($authuser->get_data('steam_id'), 'reg_bonus_referral_test_vacban') && test_csgo($authuser->get_data('steam_id'), 'reg_bonus_referral_test_csgo') && test_user_lvl($authuser->get_data('steam_id'), 'reg_bonus_referral_min_lvl') && test_time_from_reg($authuser->get_id(), 'reg_bonus_referral_test_time_create', 'reg_bonus_referral_mintime_from_create')) {
            set_user_balance($authuser, get_setval('opencase_regbalance'));
            add_balance_log($authuser->get_id(), get_setval('opencase_regbalance'), 'Стартовый баланс при регистрации', 7);
        }
        add_log($user->steamid, 'firstlogin');
        update_setval('opencase_count_users', get_setval('opencase_count_users') + 1);
        centrifugo::sendStats();
        if (function_exists('is_have_referrer_code') && is_have_referrer_code()) {
            get_bonus($authuser->get_id());
        }
    }
    if (!$authuser->get_banned()) {
        $authuser->set_auth_cookie();
        redirect_srv_msg('', '/');
    } else {
        user_logout_steam(); // todo было user_logout до добавления файла vkauth.php
        exit('Вы заблокированны на этом сайте');
    }
}

function user_logout_steam() { // todo было user_logout до добавления файла vkauth.php
    if (($user = get_user())) {
        $user->clear_auth_cookie();
    }
}

function get_user_by_steam_id($steam_id) {
    $userdata = db()->query_once('SELECT user_id from users_data INNER JOIN user_fields ON user_fields.id = users_data.user_field_id WHERE user_fields.key = \'steam_id\' AND users_data.value = "' . db()->nomysqlinj($steam_id) . '"');
    if ($userdata['user_id']) {
        return new user($userdata['user_id']);
    }
    return false;
}
