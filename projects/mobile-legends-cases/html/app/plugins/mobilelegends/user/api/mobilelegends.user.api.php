<?php

add_api_url('/api/mobilelegends/getcases/', 'ml_get_cases_api');
add_api_url('/api/mobilelegends/getitems/', 'ml_get_items_api');
add_api_url('/api/mobilelegends/opencase/', 'ml_open_case_api');
add_api_url('/api/mobilelegends/profile/', 'ml_profile_api');
add_api_url('/api/mobilelegends/withdraw/', 'ml_withdraw_api');
add_api_url('/api/mobilelegends/sell/', 'ml_sell_item_api');

function ml_get_cases_api() {
    global $user;
    
    $cases = sel('ml_cases', "WHERE active = 1 ORDER BY price ASC");
    
    foreach ($cases as &$case) {
        $case['image_url'] = '/uploads/ml_cases/' . $case['image'];
    }
    
    api_response(true, ['cases' => $cases]);
}

function ml_get_items_api() {
    global $user;
    
    $page = isset($_POST['page']) ? intval($_POST['page']) : 0;
    $limit = 20;
    $offset = $page * $limit;
    
    $items = sel('ml_items', "ORDER BY price DESC LIMIT {$offset}, {$limit}");
    
    foreach ($items as &$item) {
        $item['image_url'] = '/uploads/ml_items/' . $item['image'];
        $item['type_name'] = ml_items::$item_types[$item['type']];
        $item['rarity_name'] = ml_items::$item_rarity[$item['rarity']];
    }
    
    $hasMore = count($items) == $limit;
    
    api_response(true, [
        'items' => $items,
        'hasMore' => $hasMore
    ]);
}

function ml_open_case_api() {
    global $user;
    
    // Проверяем авторизацию
    if (!$user->is_login()) {
        api_response(false, ['error' => 'Необходимо авторизоваться']);
    }
    
    // Проверяем параметры
    if (!isset($_POST['case_id'])) {
        api_response(false, ['error' => 'Не указан ID кейса']);
    }
    
    $case_id = intval($_POST['case_id']);
    
    // Получаем информацию о кейсе
    $case = sel1('ml_cases', "WHERE id = {$case_id}");
    
    if (!$case) {
        api_response(false, ['error' => 'Кейс не найден']);
    }
    
    // Проверяем баланс
    if ($user->get_balance() < $case['price']) {
        api_response(false, ['error' => 'Недостаточно средств']);
    }
    
    // Списываем средства
    $user->update_balance(-$case['price']);
    
    // Получаем предметы из кейса и их шансы
    $items = sel('ml_cases_items', "WHERE case_id = {$case_id}");
    
    if (empty($items)) {
        api_response(false, ['error' => 'Кейс пуст']);
    }
    
    // Определяем выпавший предмет на основе шансов
    $total_chance = 0;
    foreach ($items as $item) {
        $total_chance += $item['drop_chance'];
    }
    
    $rand = mt_rand(1, 100) / 100 * $total_chance;
    $current_chance = 0;
    $won_item_id = 0;
    
    foreach ($items as $item) {
        $current_chance += $item['drop_chance'];
        if ($rand <= $current_chance) {
            $won_item_id = $item['item_id'];
            break;
        }
    }
    
    // Получаем информацию о выпавшем предмете
    $won_item = sel1('ml_items', "WHERE id = {$won_item_id}");
    
    if (!$won_item) {
        api_response(false, ['error' => 'Ошибка при получении предмета']);
    }
    
    // Добавляем предмет в инвентарь пользователя
    qryo("INSERT INTO user_items (user_id, item_id, item_type, date_added) VALUES ({$user->get_id()}, {$won_item_id}, 'ml', NOW())");
    $user_item_id = sel1('LAST_INSERT_ID()');
    
    // Формируем ответ
    $won_item['image_url'] = '/uploads/ml_items/' . $won_item['image'];
    $won_item['type_name'] = ml_items::$item_types[$won_item['type']];
    $won_item['rarity_name'] = ml_items::$item_rarity[$won_item['rarity']];
    $won_item['user_item_id'] = $user_item_id;
    
    // Логируем открытие кейса
    qryo("INSERT INTO logs (ip, event, type, data) VALUES ('{$_SERVER['REMOTE_ADDR']}', 'Открытие кейса Mobile Legends', 'ml_case', '" . 
        json_encode(['user_id' => $user->get_id(), 'case_id' => $case_id, 'item_id' => $won_item_id]) . "')");
    
    api_response(true, [
        'item' => $won_item,
        'case' => $case
    ]);
}

function ml_profile_api() {
    global $user;
    
    // Проверяем авторизацию
    if (!$user->is_login()) {
        api_response(false, ['error' => 'Необходимо авторизоваться']);
    }
    
    // Получаем предметы пользователя
    $page = isset($_POST['page']) ? intval($_POST['page']) : 0;
    $limit = 20;
    $offset = $page * $limit;
    
    $items_query = "
        SELECT ui.id as user_item_id, mi.* 
        FROM user_items ui 
        JOIN ml_items mi ON ui.item_id = mi.id 
        WHERE ui.user_id = {$user->get_id()} AND ui.item_type = 'ml' 
        ORDER BY ui.date_added DESC 
        LIMIT {$offset}, {$limit}
    ";
    
    $items = sel($items_query);
    
    foreach ($items as &$item) {
        $item['image_url'] = '/uploads/ml_items/' . $item['image'];
        $item['type_name'] = ml_items::$item_types[$item['type']];
        $item['rarity_name'] = ml_items::$item_rarity[$item['rarity']];
    }
    
    $hasMore = count($items) == $limit;
    
    // Получаем настройки Mobile Legends
    $ml_settings = [
        'currency_rate' => get_setval('ml_currency_rate'),
        'min_withdraw' => get_setval('ml_min_withdraw')
    ];
    
    api_response(true, [
        'items' => $items,
        'hasMore' => $hasMore,
        'settings' => $ml_settings
    ]);
}

function ml_withdraw_api() {
    global $user;
    
    // Проверяем авторизацию
    if (!$user->is_login()) {
        api_response(false, ['error' => 'Необходимо авторизоваться']);
    }
    
    // Проверяем параметры
    if (!isset($_POST['ml_id']) || !isset($_POST['ml_username'])) {
        api_response(false, ['error' => 'Не указан ID или имя игрока Mobile Legends']);
    }
    
    $ml_id = $_POST['ml_id'];
    $ml_username = $_POST['ml_username'];
    
    // Обновляем данные пользователя
    qryo("UPDATE users SET ml_id = '{$ml_id}', ml_username = '{$ml_username}' WHERE id = {$user->get_id()}");
    
    api_response(true, ['message' => 'Данные аккаунта Mobile Legends сохранены']);
}

function ml_sell_item_api() {
    global $user;
    
    // Проверяем авторизацию
    if (!$user->is_login()) {
        api_response(false, ['error' => 'Необходимо авторизоваться']);
    }
    
    // Проверяем параметры
    if (!isset($_POST['user_item_id'])) {
        api_response(false, ['error' => 'Не указан ID предмета']);
    }
    
    $user_item_id = intval($_POST['user_item_id']);
    
    // Получаем информацию о предмете
    $query = "
        SELECT ui.id as user_item_id, mi.* 
        FROM user_items ui 
        JOIN ml_items mi ON ui.item_id = mi.id 
        WHERE ui.id = {$user_item_id} AND ui.user_id = {$user->get_id()} AND ui.item_type = 'ml'
    ";
    
    $item = sel1($query);
    
    if (!$item) {
        api_response(false, ['error' => 'Предмет не найден или не принадлежит вам']);
    }
    
    // Определяем сумму продажи (например, 70% от стоимости)
    $sell_price = round($item['price'] * 0.7, 2);
    
    // Удаляем предмет из инвентаря
    qryo("DELETE FROM user_items WHERE id = {$user_item_id}");
    
    // Начисляем средства пользователю
    $user->update_balance($sell_price);
    
    // Логируем продажу
    qryo("INSERT INTO logs (ip, event, type, data) VALUES ('{$_SERVER['REMOTE_ADDR']}', 'Продажа предмета Mobile Legends', 'ml_sell', '" . 
        json_encode(['user_id' => $user->get_id(), 'item_id' => $item['id'], 'price' => $sell_price]) . "')");
    
    api_response(true, [
        'message' => 'Предмет успешно продан',
        'price' => $sell_price,
        'balance' => $user->get_balance()
    ]);
} 