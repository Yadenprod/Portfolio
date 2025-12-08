<?php
//todo VirKato - добавил поле для хранения vk_id
add_installer('opencase', 'opencase_userfields_install');
add_uninstaller('opencase', 'opencase_userfields_uninstall');

function opencase_userfields_install() {
    add_user_field('steam_id', 'string', '', 'Steam id пользователя');
    add_user_field('vk_id', 'string', '', 'VK id пользователя');
    add_user_field('image', 'string', '', 'Аватарка пользователя');
    add_user_field('timecreated', 'int', '', 'Дата регистрации в стим');
    add_user_field('balance', 'float', '0', 'Баланс пользователя');
    add_user_field('trade_link', 'string', '', 'Ссылка на обмен пользователя');
    add_user_field('chance', 'int', '100', 'Шанс открытия кейса');
    add_user_field('withdraw_disabled', 'bool', '0', 'Блокировка вывода');
    add_user_field('deposite_disabled', 'bool', '0', 'Блокировка депозита');
    add_user_field('status', 'int', '0', 'Статус пользователя');
    add_user_field('deposite_promo', 'string', '', 'Промокод введеный в форме пополнения баланса');
    add_user_field('top_disabled', 'bool', '0', 'Скрывать в топе');
    add_user_field('use_self_profit', 'bool', '0', 'Использовать личный профит');
    add_user_field('self_profit', 'int', '0', 'Личный профит для пользователя');
}

function opencase_userfields_uninstall() {
    delete_user_field('steam_id');
    delete_user_field('vk_id');
    delete_user_field('image');
    delete_user_field('timecreated');
    delete_user_field('balance');
    delete_user_field('trade_link');
    delete_user_field('chance');
    delete_user_field('withdraw_disabled');
    delete_user_field('deposite_disabled');
    delete_user_field('status');
    delete_user_field('deposite_promo');
    delete_user_field('top_disabled');
    delete_user_field('use_self_profit');
    delete_user_field('self_profit');
}
