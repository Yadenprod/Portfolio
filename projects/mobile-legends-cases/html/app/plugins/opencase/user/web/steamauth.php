<?php

add_app('/\?login.*', 'vkauth_login');
add_app('/steamauth/logout/', 'vkauth_logout');

function vkauth_login() {
    if (isset($_GET['code'])) {
        $params = array(
            'client_id' => '8220240',
            'client_secret' => 'x2SBvD9jKKIkjXgowC3A',
            'code' => $_GET['code'],
            'redirect_uri' => 'https://m-legends-drop.ru/?login&',
            'v' => '5.131'
        );

        $token = json_decode(file_get_contents('https://oauth.vk.com/access_token/?' . urldecode(http_build_query($params))), true);

        if (isset($token['access_token'])) {
            $params = array(
                'user_ids' => $token['user_id'],
                'fields' => 'screen_name,sex,bdate,photo_big',
                'access_token' => $token['access_token'],
                'v' => '5.131'
            );

            $userInfo = json_decode(file_get_contents('https://api.vk.com/method/users.get?' . urldecode(http_build_query($params))), true);
            if (isset($userInfo['response'][0]['id'])) {
                $user = $userInfo['response'][0];
                user_login($user);
            }
        } else {
            add_log('', 'Not valid enter');
            redirect_srv_msg('', '/');
        }
    } else {
        $params = array(
            'client_id' => '8220240',
            'redirect_uri' => 'https://m-legends-drop.ru/?login&',
            'response_type' => 'code',
            'v' => '5.131'
        );

        header('Location: https://oauth.vk.com/authorize?' . urldecode(http_build_query($params)));
        exit(); // нейронка рекомендовала exit() // было wsexit
    }
}

function get_user_by_vk_id($vk_id) {
    $userdata = db()->query_once('SELECT user_id from users_data INNER JOIN user_fields ON user_fields.id = users_data.user_field_id WHERE user_fields.key = \'vk_id\' AND users_data.value = "' . db()->nomysqlinj($vk_id) . '"');
    if ($userdata['user_id']) {
        return new user($userdata['user_id']);
    }
    return false;
}

function user_login($user) {
    if (($authuser = get_user_by_vk_id($user['id']))) {
        $authuser->set_name(mysqli_real_escape_string(db()->db, $user['first_name'] . ' ' . $user['last_name']));
        $authuser->set_data('image', $user['photo_big']);
        $authuser->update();
        add_log($user['id'], 'login');
    } else {
        $authuser = new user();
        $authuser->set_name(mysqli_real_escape_string(db()->db, $user['first_name'] . ' ' . $user['last_name']));
        $authuser->add();
        $authuser->set_data('vk_id', $user['id']);
        $authuser->set_data('image', $user['photo_big']);
        $authuser->update();
        if (get_setval('opencase_regbalance') > 0 && !test_vacbanned($authuser->get_data('vk_id'), 'reg_bonus_referral_test_vacban') && test_csgo($authuser->get_data('vk_id'), 'reg_bonus_referral_test_csgo') && test_user_lvl($authuser->get_data('vk_id'), 'reg_bonus_referral_min_lvl') && test_time_from_reg($authuser->get_id(), 'reg_bonus_referral_test_time_create', 'reg_bonus_referral_mintime_from_create')) {
            set_user_balance($authuser, get_setval('opencase_regbalance'));
            add_balance_log($authuser->get_id(), get_setval('opencase_regbalance'), 'Стартовый баланс при регистрации', 7);
        }
        add_log($user['id'], 'firstlogin');
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
        user_logout();
        exit('Вы заблокированны на этом сайте');
    }
}

function vkauth_logout() {
    user_logout();
    redirect_srv_msg('', '/');
}

function get_user() {
    if (is_login()) {
        return user();
    }
    return false;
}

function user_logout() {
    if (($user = get_user())) {
        $user->clear_auth_cookie();
    }
}
