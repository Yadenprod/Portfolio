<?php

add_post('/api/opencase/sale/([0-9]+)/', 'opencase_sale');
add_post('/api/opencase/sale/all/', 'opencase_sale_all');
add_post('/api/opencase/sale/all/info/', 'opencase_sale_all_data');
add_post('/api/opencase/sale/list/', 'opencase_sale_list');
add_post('/api/opencase/withdraw/([0-9]+)/', 'opencase_withdraw');
add_post('/api/opencase/withdraw/analogs/([0-9]+)/', 'opencase_withdraw_with_analogs');
add_post('/api/opencase/withdraw/admin/([0-9]+)/', 'opencase_withdraw_with_admin');
add_post('/api/opencase/open/([0-9]+)/', 'opencase_open');
add_post('/api/opencase/contracts/', 'opencase_contracts');
add_post('/api/opencase/savesettings/', 'opencase_savesettings');
add_post('/api/opencase/getstat/', 'opencase_getstat');
add_post('/api/opencase/getnewdrop/', 'opencase_getnewdrop');
add_post('/api/opencase/getuserdrops/', 'opencase_getuserdrops');
add_post('/api/opencase/getusercontracts/', 'opencase_getusercontracts');
add_post('/api/opencase/usepromocode/', 'opencase_usepromocode');
add_post('/api/opencase/open/multiply/([0-9]+)/', 'opencase_multiply_open');

/**
 * Подтверждение отправки админом
 * @param $args :int номер предмета (взят из URL)
 */
function opencase_withdraw_with_admin($args)
{
    $droppedItem = new droppedItem($args[0]);
    $droppedItem->set_status(2);
    $droppedItem->update_droppedItem();

    //TODO здесь произвести отправку предмета на аккаунт пользователя ($userReceiver - получатель)
    $userReceiver = $droppedItem->get_user_class();
    $link = $userReceiver->get_data('trade_link');
    $json['success'] = true;
    echo_json($json);
}


function opencase_sale($args)
{
    $user = user();
    $json = array('success' => false);
    $droppedItem = new droppedItem($args[0]);
    if ($user->get_id() != '' && $user->is_login()) {
        if ($droppedItem->get_user_id() == $user->get_id()) {
            if ($droppedItem->get_status() == 0 || $droppedItem->get_status() == 6) {
                $droppedItem->set_status(3);
                $droppedItem->update_droppedItem();
                inc_user_balance($user, $droppedItem->get_price());
                add_balance_log($user->get_id(), $droppedItem->get_price(), 'Продажа предмета №' . $droppedItem->get_id() . ' (' . $droppedItem->get_item_class()->get_name() . ')', 2);
                $json['success'] = true;
                $json['price'] = $droppedItem->get_price();
                $json['balance'] = get_user_balance($user);
                $json['msg'] = 'Предмет успешно продан';
            } else {
                $json['error'] = 'Этот предмет уже продан или выведен';
            }
        } else {
            $json['error'] = 'Этот предмет не может быть продан';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}

function opencase_withdraw($args)
{
    $user = user();
    $json = array('success' => false);
    $droppedItem = new droppedItem($args[0]);
    if ($user->get_id() != '' && $user->is_login()) {
        if ($user->get_data('trade_link') != '') {
            $queryStr = parse_url($user->get_data('trade_link'));
            $queryArray = [];
            parse_str($queryStr, $queryArray);
            if (isset($queryArray['partner']) && isset($queryArray['token'])) {
                if ($user->get_data('withdraw_disabled') != 1) {
                    if ($droppedItem->get_withdrawable() && $droppedItem->get_user_id() == $user->get_id() && ($droppedItem->get_status() == 0 || $droppedItem->get_status() == 6)) {
                        $countWithDraw = db()->query_once('SELECT count(id) from opencase_droppeditems where user_id = ' . $user->get_id() . ' and status = 1');
                        if ($countWithDraw['count(id)'] < 5) {
                            $botEvent = new botEvent();
                            $dataReady = false;
                            if (get_setval('opencase_withdraw_type') != WITHDRAW_TYPE_ONLY_MARKET) {
                                $invItem = new invItems();
                                $invItem = $invItem->get_invItemss('market_hash_name = "' . $droppedItem->get_item_name_alt() . '" and status = 0 and tradable = 1 and created_at < (NOW() - INTERVAL 5 MINUTE)', '', 1);
                                if (count($invItem) > 0) {
                                    $invItem = $invItem[0];
                                    $invItem->set_status(1);
                                    $invItem->update_invItems();
                                    $droppedItem->set_status(1);
                                    $droppedItem->set_bot_id($invItem->get_bot_id());
                                    $droppedItem->update_droppedItem();
                                    $additional = array(
                                        'msg' => '',
                                        'tradeUrl' => $user->get_data('trade_link'),
                                        'ditem' => $droppedItem->get_id(),
                                        'appid' => get_setval('opencase_gameid')
                                    );
                                    $botEvent->set_parametrs('', $invItem->get_bot_id(), 1, json_encode($additional), $invItem->get_id(), 0, '', '');
                                    $botEvent->add_botEvent();
                                    $json['success'] = true;
                                    $json['quick'] = true;
                                    $json['msg'] = 'Предмет подготовлен к получению, в течение 2 минут наш бот отправит его Вам.';
                                    $dataReady = true;
                                }
                            }
                            if (!$dataReady && get_setval('opencase_withdraw_type') != WITHDRAW_TYPE_ONLY_BOT) {
                                $hasError = true;
                                $botId = db()->query_once('SELECT id FROM opencase_bot WHERE market_enable = 1 ORDER BY RAND() LIMIT 1');
                                if (isset($botId['id'])) {
                                    $bot = new bot($botId['id']);
                                    if ($bot->get_id() != '' && $bot->get_market_enable()) {
                                        $item = $droppedItem->get_item_class();
                                        $currentPriceMul = 1;
                                        $marketItems = get_items_by_market_hash_name($bot->get_decrypted_market_key(), $item->get_name(), $currentPriceMul);
                                        if (!empty($marketItems)) {
                                            $marketItem = select_market_item_from_array($marketItems, $item->get_price() * $currentPriceMul);
                                            if (!empty($marketItem)) {
                                                $botEvent = new botEvent();
                                                $botEvent->add_botEvent();
                                                $botEvent = new botEvent(db()->get_last_id());
                                                if ($botEvent->get_id() != '') {
                                                    $customId = $botEvent->get_id() . time();
                                                    $error = '';
                                                    $marketItemId = buy_market_item_for($bot->get_decrypted_market_key(), $marketItem, $queryArray['partner'], $queryArray['token'], $customId, $error);
                                                    if ($marketItemId) {
                                                        $hasError = false;
                                                        $droppedItem->set_status(1);
                                                        $droppedItem->set_bot_id($bot->get_id());
                                                        $droppedItem->update_droppedItem();
                                                        $additional = array(
                                                            'msg' => '',
                                                            'tradeUrl' => $user->get_data('trade_link'),
                                                            'ditem' => $droppedItem->get_id(),
                                                            'appid' => get_setval('opencase_gameid'),
                                                            'marketCustomId' => $customId
                                                        );
                                                        $botEvent->set_bot_id($bot->get_id());
                                                        $botEvent->set_event(50);
                                                        $botEvent->set_additional(json_encode($additional));
                                                        $botEvent->set_status(1);
                                                        $botEvent->update_botEvent();
                                                        $json['success'] = true;
                                                        $json['quick'] = false;
                                                        $json['msg'] = 'Вывод оформлен, ожидайте обмена.';
                                                    } else {
                                                        $botEvent->delete_botEvent();
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                                if ($hasError) {
                                    if (get_setval('opencase_gameid') == 730) {
                                        $domain = 'market.csgo.com';
                                    } elseif (get_setval('opencase_gameid') == 570) {
                                        $domain = 'market.dota2.net';
                                    } else {
                                        $domain = 'маркете';
                                    }
                                    $json['error'] = 'К сожалению в данный момент мы не смогли подобрать нужный лот для покупки на ' . $domain . ', попробуйте позже!';
                                }
                                $dataReady = true;
                            }
                            if (!$dataReady) {
                                $json['error'] = 'В данный момент этот предмет не может быть отправлен';
                            }
                        } else {
                            $json['error'] = 'У Вас есть неполученные предметы. Прежде чем продолжить выводить предметы, получите все отправленные обмены.';
                        }
                    } else {
                        $json['error'] = 'Этот предмет не может быть отправлен';
                    }
                } else {
                    $json['error'] = 'Вывод предметов для Вас заблокирован';
                }
            } else {
                $json['msg'] = 'Предмет подготовлен к получению, в течение 10 минут наш бот отправит его Вам';
                //ТУТ ПИСАТЬ ЛОГИКУ ВЫВОДА ПРОЩЕ БУДЕТ
            }
        } else {
            $json['error'] = 'У Вас не установлен UserID ZoneID';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}

function opencase_open($args)
{
    $timeStart = microtime(true);
    $user = user();
    $json = array('success' => false);
    $case = new ocase($args[0]);
    if ($case->get_id() != '') {
        if (!is_locked_user($user)) {
            lock_user($user);
            if ($user->get_id() != '' && $user->is_login()) {
                if ($case->is_available()) {
                    $casePrice = $case->get_final_price();
                    if (get_user_balance($user) >= $casePrice) {
                        $availOpen = false;
                        $notAvailError = '';
                        switch ($case->get_type()) {
                            case ocase::TYPE_DEFAULT:
                                if ($case->get_price() > 0) {
                                    $availOpen = true;
                                } else {
                                    $notAvailError = 'В данный момент, этот кейс недоступен';
                                }
                                break;
                            case ocase::TYPE_PROMOCODE:
                                $promo = isset($_POST['promo']) ? $_POST['promo'] : '';
                                if (!empty($promo)) {
                                    $ispromo = new promocode();
                                    $ispromo->get_from_code($promo);
                                    if ($ispromo->get_code() != '' && $ispromo->get_enable() && $ispromo->get_type() == promocode::TYPE_CASE) {
                                        if ($ispromo->get_use() < $ispromo->get_count()) {
                                            if ($ispromo->user_can_use($user->get_id())) {
                                                if ($case->get_dep_for_open() <= 0 || get_count_deposite_per_period($user->get_id()) >= $case->get_dep_for_open()) {
                                                    $availOpen = true;
                                                } else {
                                                    $depositDays = get_setval('opencase_deposit_check_day');
                                                    if ($depositDays == 1) {
                                                        $strEnd = 'сутки';
                                                    } else {
                                                        $strEnd = $depositDays . ' дней';
                                                    }
                                                    $notAvailError = 'Для открытия промокейса необходимо пополнить баланс на ' . $case->get_dep_for_open() . ' руб за последние ' . $strEnd;
                                                }
                                            } else {
                                                $notAvailError = 'Вы уже использовали этот код';
                                            }
                                        } else {
                                            $notAvailError = 'Промокод уже был активирован максимальное количество раз';
                                        }
                                    } else {
                                        $notAvailError = 'Такого промокода не существует';
                                    }
                                } else {
                                    $notAvailError = 'Вы не ввели промокод';
                                }
                                break;
                            case ocase::TYPE_DEPOSITE:
                                if (can_open_free_case($case)) {
                                    $availOpen = true;
                                } else {
                                    $notAvailError = 'Вы не можете открыть бесплатный кейс, т.к. у Вас не выполнены все условия';
                                }
                                break;
                        }
                        if ($availOpen) {
                            $userProfit = get_avail_user_profit($user);
                            $available = ($casePrice) * (float)(get_setval('opencase_chance') / 100) + $userProfit;
                            $enabledItems = db()->query('select * from opencase_itemincase where case_id = "' . $case->get_id() . '" and (count_items = -1 or count_items > 0) and enabled = 1 and chance > 0 order by chance DESC');
                            $item_names = array();
                            $totalChance = (float)($user->get_data('chance') / 100) * (float)($case->get_chance() / 100);
                            $checkItemsPrice = $casePrice > 0 ? $casePrice : 100;
                            $items = [];
                            $otherItems = [];
                            foreach ($enabledItems as $item) {
                                $tmpItem = new item($item['item_id']);
                                $itemChanse = $item['chance'];
                                if ($tmpItem->get_price() <= $checkItemsPrice) {
                                    if ($totalChance > 0) {
                                        $itemChanse /= $totalChance;
                                    }
                                } else {
                                    if ($totalChance <= 0) {
                                        $otherItems[] = array('itemincase_id' => $item['id'], 'name' => $tmpItem->get_name(), 'chance' => $itemChanse, 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'rarity' => $tmpItem->get_css_quality_class(), 'quality' => $tmpItem->get_quality(), 'price' => $tmpItem->get_price());
                                        continue;
                                    }
                                    $itemChanse *= $totalChance;
                                }
                                $items[] = array('itemincase_id' => $item['id'], 'name' => $tmpItem->get_name(), 'chance' => $itemChanse, 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'rarity' => $tmpItem->get_css_quality_class(), 'quality' => $tmpItem->get_quality(), 'price' => $tmpItem->get_price());
                            }
                            if (empty($items)) {
                                $items = $otherItems;
                            }

                            $haveItems = array();

                            if (count($enabledItems) > 0) {
                                foreach ($items as $item) {
                                    if ($item['price'] <= $available)
                                        $haveItems[] = $item;
                                }

                                if (get_setval('opencase_drop_only_have') == 1) {
                                    $botItems = db()->query('select * from opencase_invitems where status = 0');
                                    $haveItemTmp = $haveItems;
                                    foreach ($haveItems as $key => $hItem) {
                                        $find = false;
                                        foreach ($botItems as $botItem) {
                                            if ($hItem['name'] == $botItem['market_hash_name'] && !$find) {
                                                $find = true;
                                            }
                                        }
                                        if (!$find) {
                                            unset($haveItems[$key]);
                                        }
                                    }
                                    if (count($haveItems) == 0) {
                                        $haveItems = $haveItemTmp;
                                    }
                                }

                                $isMinPrice = false;
                                if (count($haveItems) == 0) {
                                    $isMinPrice = true;
                                    $haveItems = $items;
                                    usort($haveItems, 'sortItemByPrice');
                                }

                                $sum = 0;
                                foreach ($haveItems as $key => $hItem) {
                                    $sum += $hItem['chance'];
                                }

                                if (count($haveItems) > 0) {
                                    $chance = rand(0, $sum - 1);
                                    $i = 0;
                                    $find = false;
                                    $item = false;
                                    foreach ($haveItems as $hItem) {
                                        if ($chance >= $i && $chance < $i + (int)$hItem['chance'] && !$find) {
                                            $item = $hItem;
                                            $find = true;
                                        } else {
                                            $i += (int)$hItem['chance'];
                                        }
                                    }

                                    if ($isMinPrice)
                                        $item = $haveItems[0];

                                    if ($item) {
                                        if (isset($ispromo) && $ispromo) {
                                            $ispromo->use_promocode($user->get_id());
                                        }
                                        $dItem = new droppedItem();
                                        $itemPrice = round($item['price']);
                                        $fast = isset($_POST['fast']) ? 1 : 0;
                                        $dItem->set_parametrs('', $user->get_id(), $item['item_id'], 5, $itemPrice, '', 0, $case->get_id(), $fast, 0, 0, '', $item['withdrawable'], $item['usable']);
                                        $time = $dItem->add_droppedItem();
                                        $itemID = $dItem->get_id();
                                        $openCase = new openCase();
                                        $openCase->set_parametrs('', $user->get_id(), $case->get_id(), $itemID, $casePrice, '');
                                        $openCase->add_openCase();
                                        $case->inc_open_count();
                                        $itemincase = new itemincase($item['itemincase_id']);
                                        if ($itemincase->get_count_items() > 0) {
                                            $itemincase->set_count_items($itemincase->get_count_items() - 1);
                                            $itemincase->update_itemincase();
                                        }
                                        $needProfit = $casePrice * (1 - (float)(get_setval('opencase_chance') / 100));
                                        $profit = $casePrice - $itemPrice;
                                        $descProfit = $profit - $needProfit;
                                        dec_user_balance($user, $casePrice);
                                        add_balance_log($user->get_id(), -$casePrice, 'Открытие кейса №' . $case->get_id() . ' (' . $case->get_name() . ')', 1);
                                        set_avail_user_profit($user, round($userProfit + $descProfit));
                                        update_setval('opencase_count_open_case', get_setval('opencase_count_open_case') + 1);

                                        $json['success'] = true;
                                        $json['item'] = array('ID' => $itemID, 'name' => $item['name'], 'shortName' => $item['name'], 'quality' => $item['quality'] ?? '', 'image' => $item['image'], 'price' => $itemPrice, 'rarity' => $item['rarity'] ?? '', 'usable' => ((bool)$item['usable']));
                                        centrifugo::sendItem($dItem, $time);
                                        centrifugo::sendStats();
                                    } else {
                                        $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                                    }
                                } else {
                                    $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                                }
                            } else {
                                $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                            }
                        } else {
                            $json['error'] = $notAvailError;
                        }
                    } else {
                        $json['error'] = 'У Вас недостаточно средств для открытия этого кейса';
                    }
                } else {
                    $json['error'] = 'В данный момент, этот кейс недоступен';
                }
            } else {
                $json['error'] = 'Вы не авторизованны на сайте';
            }
            unlock_user($user);
        } else {
            $json['error'] = 'Вы не можете выполнить это действие, т.к. в данный момент выполняется другое действие';
        }
    } else {
        $json['error'] = 'Такого кейса не существует';
    }
    $timeEnd = microtime(true);
    $json['speed'] = $timeEnd - $timeStart;
    echo_json($json);
}

function opencase_contracts()
{
    $user = user();
    $json = array('success' => false);
    if (!is_locked_user($user)) {
        lock_user($user);
        if ($user->get_id() != '' && $user->is_login()) {
            $itemsIds = explode(';', $_POST['items'] ?? '');
            $items = [];
            foreach ($itemsIds as $value) {
                $itemId = (int)$value;
                $items[$itemId] = $itemId;
            }
            if (count($items) >= 3 && count($items) <= 10) {
                $userProfit = get_avail_user_profit($user);
                $contractPrice = 0;
                $forbiden = false;
                foreach ($items as $item) {
                    $droppedItem = new droppedItem(intval($item));
                    $contractPrice += $droppedItem->get_price();
                    if ($droppedItem->get_user_id() != $user->get_id() || !$droppedItem->get_usable() || ($droppedItem->get_status() != 0 && $droppedItem->get_status() != 6)) {
                        $forbiden = true;
                    }
                }
                if (!$forbiden) {
                    $minPrice = $contractPrice / 3;
                    $maxPrice = $contractPrice * 3;
                    $userChanse = (float)($user->get_data('chance') / 100);
                    if ($userChanse > 1) {
                        $minPrice = min($contractPrice, $minPrice * $userChanse);
                    } else {
                        $maxPrice = max($contractPrice, $maxPrice * $userChanse);
                    }
                    $available = ($contractPrice) * (float)(get_setval('opencase_chance') / 100) + $userProfit;
                    $haveItem = db()->query('select * from opencase_items where price <= ' . $available . ' and price >= ' . $minPrice . ' and price <= ' . $maxPrice . ' order by price DESC');

                    if (get_setval('opencase_drop_only_have') == 1) {
                        $botItems = db()->query('select * from opencase_invitems where status = 0');
                        $haveItemTmp = $haveItem;
                        foreach ($haveItem as $key => $hItem) {
                            $find = false;
                            foreach ($botItems as $botItem) {
                                if ($hItem['name'] == $botItem['market_hash_name'] && !$find) {
                                    $find = true;
                                }
                            }
                            if (!$find) {
                                unset($haveItem[$key]);
                            }
                        }
                        if (count($haveItem) == 0) {
                            $haveItem = $haveItemTmp;
                        }
                    }

                    if (count($haveItem) > 0) {
                        $item = $haveItem[array_rand($haveItem)];
                        $dItem = new droppedItem();
                        $itemPrice = round($item['price']);
                        $dItem->set_parametrs('', $user->get_id(), $item['id'], 5, $itemPrice, '', 0, 0, 0, 0, 0);
                        $time = $dItem->add_droppedItem();
                        $itemID = $dItem->get_id();
                        $image = !empty($_POST['image']) ? db()->nomysqlinj(str_replace(' ', '+', $_POST['image'])) : '';
                        $contract = new contract();
                        $contract->set_parametrs('', $user->get_id(), $_POST['items'], $itemID, $contractPrice, '', $image);
                        $contract->add_contract();
                        $needProfit = $contractPrice * (1 - (float)(get_setval('opencase_chance') / 100));
                        $profit = $contractPrice - $itemPrice;
                        $descProfit = $profit - $needProfit;
                        set_avail_user_profit($user, round($userProfit + $descProfit));
                        update_setval('opencase_count_contracts', get_setval('opencase_count_contracts') + 1);
                        foreach ($items as $key => $drItem) {
                            $droppedItem = new droppedItem($drItem);
                            $droppedItem->set_status(4);
                            $droppedItem->update_droppedItem();
                        }
                        $json['success'] = true;
                        $json['item'] = array('ID' => $itemID, 'name' => $item['name'], 'shortName' => $item['name'], 'quality' => '', 'image' => $item['image'], 'price' => $itemPrice, 'rarity' => $dItem->get_item_class()->get_css_quality_class());
                        centrifugo::sendItem($dItem, $time);
                        centrifugo::sendStats();
                    } else {
                        $json['error'] = 'При создании контракта возникла ошибка, попробуйте повторить операцию позже';
                    }
                } else {
                    $json['error'] = 'Данные предметы недоступны для добавления в контракт';
                }
            } else {
                $json['error'] = 'Контракт может состоять минимум из трех и максимум из десяти предметов';
            }
        } else {
            $json['error'] = 'Вы не авторизованны на сайте';
        }
        unlock_user($user);
    } else {
        $json['error'] = 'Вы не можете выполнить это действие, т.к. в данный момент выполняется другое действие';
    }
    echo_json($json);
}

function opencase_savesettings()
{
    $json = array('success' => false);
    $user = user();
    if ($user->get_id() != '' && $user->is_login()) {
        if (isset($_POST['url']) && $_POST['url'] != '') {
            if (preg_match('/^[ 0-9]+$/', $_POST['url'])) {
                $user->upd_data('trade_link', urldecode($_POST['url']));
                $json['success'] = true;
            } else {
                $json['error'] = 'Неверный формат ссылки';
            }
        } else {
            $json['error'] = 'Вы не ввели UserID|ZoneID';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}

function opencase_getstat()
{
    $json = array(
        'success' => true,
        'count_open_case' => get_count_open_cases(),
        'count_create_contracts' => get_count_create_contracts(),
        'count_reg_users' => get_count_reg_users(),
        'online' => get_count_onlie(),
        'today_online' => get_count_today_online(),
        'today_count_open_case' => get_count_today_open_cases(),
        'today_count_create_contracts' => get_count_today_create_contracts(),
    );
    $json = array_merge($json, stats::getAdditionalStatsArray());
    echo_json($json);
}

function opencase_getnewdrop()
{
    $json = array('success' => false);
    $needGoodItem = false;
    if (!empty($_POST['lastupdate']) && is_sqldate($_POST['lastupdate'])) {
        $lastUpdate = $_POST['lastupdate'];
        $dItems = new droppedItem();
        $dItems = $dItems->get_newDroppedItems($lastUpdate, 'DESC', 20);
    } else {
        $dItems = get_last_dropped_items();
        $needGoodItem = true;
    }
    $users = [];
    if (count($dItems) > 0) {
        $items = array();
        foreach ($dItems as $dItem) {
            if (empty($users[$dItem->get_user_id()])) {
                $users[$dItem->get_user_id()] = $dItem->get_user_class();
            }
            $user = $users[$dItem->get_user_id()];
            $item = array(
                'id' => $dItem->get_id(),
                'rarity' => $dItem->get_item_class()->get_css_quality_class(),
                'from' => $dItem->get_from(),
                'image' => $dItem->get_item_class()->get_steam_image(),
                'name' => $dItem->get_item_name(),
                'short_name' => $dItem->get_item_class()->get_name_no_stattrack_no_quality(),
                'time' => $dItem->get_time_drop(),
                'price' => $dItem->get_price(),
                'alt_name' => $dItem->get_item_name_alt(),
                'user_id' => $user->get_data('steam_id'),
                'user_img' => $user->get_data('image'),
                'user_name' => $user->get_name(),
                'source_img' => $dItem->get_source_image(),
                'source_img_alt' => $dItem->get_source_image_alt(),
                'source_css_class' => $dItem->get_source_css_class(),
                'source_link' => $dItem->get_source_link(),
            );
            if ($needGoodItem && $dItem->get_price() >= 1000) {
                $json['goodItem'] = $item;
                $needGoodItem = false;
            }
            array_push($items, $item);
        }
        $json['success'] = true;
        $json['items'] = $items;
        if ($needGoodItem) {
            $dItemInst = new droppedItem();
            $goodItems = $dItemInst->get_droppedItems('time_drop <= NOW() AND price >= 1000', 'id DESC', '1');
            if (!empty($goodItems)) {
                $dItem = array_shift($goodItems);
                $json['goodItem'] = array(
                    'id' => $dItem->get_id(),
                    'rarity' => $dItem->get_item_class()->get_css_quality_class(),
                    'from' => $dItem->get_from(),
                    'image' => $dItem->get_item_class()->get_steam_image(),
                    'name' => $dItem->get_item_name(),
                    'short_name' => $dItem->get_item_class()->get_name_no_stattrack_no_quality(),
                    'time' => $dItem->get_time_drop(),
                    'price' => $dItem->get_price(),
                    'alt_name' => $dItem->get_item_name_alt(),
                    'user_id' => $user->get_data('steam_id'),
                    'user_img' => $user->get_data('image'),
                    'user_name' => $user->get_name(),
                    'source_img' => $dItem->get_source_image(),
                    'source_img_alt' => $dItem->get_source_image_alt(),
                    'source_css_class' => $dItem->get_source_css_class(),
                    'source_link' => $dItem->get_source_link(),
                );
            }
        }
    }
    echo_json($json);
}

function opencase_getuserdrops()
{
    $json = array('success' => false, 'not_items' => true);
    if (isset($_POST['page']) && isset($_POST['user_id'])) {
        $where = [];
        if (!empty($_POST['min'])) {
            $where[] = 'price >= "' . db()->nomysqlinj($_POST['min']) . '"';
        }
        if (!empty($_POST['max'])) {
            $where[] = 'price <= "' . db()->nomysqlinj($_POST['max']) . '"';
        }
        if (isset($_POST['notSaled']) && $_POST['notSaled']) {
            $where[] = '(status = 0 OR status = 6)';
        }
        $dropItems = get_user_drops($_POST['user_id'], (!empty($where) ? implode(' AND ', $where) : false), $_POST['page']);
        if (count($dropItems) > 0) {
            $other = true;
            if (is_login() && user()->get_id() == $_POST['user_id']) {
                $other = false;
            }
            $items = array();
            foreach ($dropItems as $dItem) {
                $item = array(
                    'id' => $dItem->get_id(),
                    'rarity' => $dItem->get_item_class()->get_css_quality_class(),
                    'from' => $dItem->get_from(),
                    'status' => $dItem->get_status(),
                    'image' => $dItem->get_item_class()->get_steam_image(),
                    'name' => $dItem->get_item_name(),
                    'alt_name' => $dItem->get_item_name_alt(),
                    'other' => $other,
                    'price' => $dItem->get_price(),
                    'source_img' => $dItem->get_source_image(),
                    'source_img_alt' => $dItem->get_source_image_alt(),
                    'source_css_class' => $dItem->get_source_css_class(),
                    'source_link' => $dItem->get_source_link(),
                    'withdrawable' => (bool)$dItem->get_withdrawable(),
                    'usable' => (bool)$dItem->get_usable(),
                    'error' => $other ? false : (empty($dItem->get_error()) ? false : $dItem->get_error())
                );
                if (!$other && get_setval('opencase_auto_sell') && $dItem->get_status() == 0 && $dItem->time_left() >= 0) {
                    $time = $dItem->time_left();
                    $item['timer'] = [
                        'hour' => intval($time / 3600) < 10 ? '0' . intval($time / 3600) : intval($time / 3600),
                        'minutes' => intval($time / 60 % 60) < 10 ? '0' . intval($time / 60 % 60) : intval($time / 60 % 60),
                        'seconds' => intval($time % 60) < 10 ? '0' . intval($time % 60) : intval($time % 60)
                    ];
                } else {
                    $item['timer'] = false;
                }
                array_push($items, $item);
            }
            if (count($dropItems) > 17) {
                $json['not_items'] = false;
            }
            $json['success'] = true;
            $json['items'] = $items;
        } else {
            $json['error_code'] = 'Not items';
        }
    } else {
        $json['error_code'] = 'Invalid parameters';
        $json['not_items'] = false;
    }
    echo_json($json);
}

function opencase_getusercontracts()
{
    $json = array('success' => false, 'not_items' => true);
    if (isset($_POST['page']) && isset($_POST['user_id'])) {
        $where = [];
        if (!empty($_POST['min'])) {
            $where[] = 'item.price >= "' . db()->nomysqlinj($_POST['min']) . '"';
        }
        if (!empty($_POST['max'])) {
            $where[] = 'item.price <= "' . db()->nomysqlinj($_POST['max']) . '"';
        }
        if (isset($_POST['notSaled']) && $_POST['notSaled']) {
            $where[] = '(item.status = 0 OR item.status = 6)';
        }
        if (empty($where)) {
            $contracts = get_user_contracts($_POST['user_id'], $_POST['page']);
        } else {
            $countPerPage = 8;
            $sql = 'SELECT contract.id FROM opencase_contracts contract '
                . 'INNER JOIN opencase_droppeditems item ON contract.item_id = item.id '
                . 'WHERE contract.user_id = ' . db()->nomysqlinj($_POST['user_id']) . ' AND ' . implode(' AND ', $where) . ' '
                . 'ORDER BY id DESC '
                . 'LIMIT ' . (db()->nomysqlinj($_POST['page']) * $countPerPage) . ', ' . $countPerPage;
            $contractsArray = db()->query($sql);
            $contracts = [];
            if (is_array($contractsArray)) {
                foreach ($contractsArray as $contractElement) {
                    $contract = new contract($contractElement['id']);
                    array_push($contracts, $contract);
                }
            }
        }
        if (count($contracts) > 0) {
            $other = true;
            if (is_login() && user()->get_id() == $_POST['user_id']) {
                $other = false;
            }
            $items = array();
            foreach ($contracts as $contract) {
                $dItem = $contract->get_item_class();
                $item = array(
                    'id' => $dItem->get_id(),
                    'rarity' => $dItem->get_item_class()->get_css_quality_class(),
                    'from' => $dItem->get_from(),
                    'status' => $dItem->get_status(),
                    'image' => $dItem->get_item_class()->get_steam_image('200f', '100'),
                    'name' => $dItem->get_item_name(),
                    'alt_name' => $dItem->get_item_name_alt(),
                    'other' => $other,
                    'price' => $dItem->get_price(),
                    'withdrawable' => (bool)$dItem->get_withdrawable(),
                    'usable' => (bool)$dItem->get_usable(),
                    'error' => $other ? false : (empty($dItem->get_error()) ? false : $dItem->get_error())
                );
                $contractItems = array();
                foreach ($contract->get_items_class() as $cItem) {
                    $contractItem = array(
                        'rarity' => $cItem->get_item_class()->get_css_quality_class(),
                        'image' => $cItem->get_item_class()->get_steam_image('100f', '60'),
                        'name' => $cItem->get_item_name(),
                        'alt_name' => $cItem->get_item_name_alt()
                    );
                    array_push($contractItems, $contractItem);
                }
                $item['contract_items'] = $contractItems;
                $item['contract_price'] = round($contract->get_items_price());
                array_push($items, $item);
            }
            if (count($contracts) > 7) {
                $json['not_items'] = false;
            }
            $json['success'] = true;
            $json['items'] = $items;
        } else {
            $json['error_code'] = 'Not items';
        }
    } else {
        $json['error_code'] = 'Invalid parameters';
        $json['not_items'] = false;
    }
    echo_json($json);
}

function opencase_usepromocode()
{
    $json = ['success' => false];
    $user = user();
    if ($user->get_id() != '' && $user->is_login()) {
        if (isset($_POST['code']) && $_POST['code'] != '') {
            $promo = new promocode();
            $promo->get_from_code($_POST['code']);
            if ($promo->get_code() != '' && $promo->get_enable() && $promo->get_type() == promocode::TYPE_SUM) {
                if ($promo->user_can_use($user->get_id())) {
                    if ($promo->get_use() < $promo->get_count()) {
                        $promo->use_promocode($user->get_id());
                        if ($promo->get_value() > 0) {
                            $promoSum = $promo->get_value();
                            $json['msg'] = 'Промокод успешно активирован. Баланс увеличен на ' . $promoSum . ' руб';
                            $json['balance'] = $promoSum;
                            inc_user_balance($user, $promoSum);
                            add_balance_log($user->get_id(), $promoSum, 'Бонус за использование промокода на сумму: ' . $promo->get_code(), 5);
                        }
                        $json['success'] = true;
                    } else {
                        $json['error'] = 'Промокод уже был активирован максимальное количество раз';
                    }
                } else {
                    $json['error'] = 'Вы уже использовали этот код';
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

function opencase_sale_all()
{
    $user = user();
    $json = ['success' => false];
    if ($user->get_id() != '' && $user->is_login()) {
        $items = get_user_drops($user->get_id(), '(status = 0 OR status = 6)', 0, 0);
        if (count($items) > 0) {
            foreach ($items as $droppedItem) {
                $droppedItem->set_status(3);
                $droppedItem->update_droppedItem();
                inc_user_balance($user, $droppedItem->get_price());
                add_balance_log($user->get_id(), $droppedItem->get_price(), 'Продажа предмета №' . $droppedItem->get_id() . ' (' . $droppedItem->get_item_class()->get_name() . ')', 2);
            }
            $json['success'] = true;
            $json['balance'] = get_user_balance($user);
            $json['msg'] = 'Все предметы успешно проданы';
        } else {
            $json['error'] = 'Нет предметов для продажи';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}

function opencase_sale_list()
{
    $user = user();
    $json = ['success' => false];
    if ($user->get_id() != '' && $user->is_login()) {
        $ids = [];
        if (!empty($_POST['ids'])) {
            foreach ($_POST['ids'] as $id) {
                $ids[] = (int)$id;
            }
        }
        if (!empty($ids)) {
            $items = get_user_drops($user->get_id(), 'id IN (' . implode(',', $ids) . ')  AND (status = 0 OR status = 6)', 0, 0);
            if (count($items) > 0) {
                foreach ($items as $droppedItem) {
                    $droppedItem->set_status(3);
                    $droppedItem->update_droppedItem();
                    inc_user_balance($user, $droppedItem->get_price());
                    add_balance_log($user->get_id(), $droppedItem->get_price(), 'Продажа предмета №' . $droppedItem->get_id() . ' (' . $droppedItem->get_item_class()->get_name() . ')', 2);
                }
                $json['success'] = true;
                $json['balance'] = get_user_balance($user);
                $json['msg'] = 'Все предметы успешно проданы';
            } else {
                $json['error'] = 'Нет предметов для продажи';
            }
        } else {
            $json['error'] = 'Нет предметов для продажи';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}

function opencase_multiply_open($args)
{
    $timeStart = microtime(true);
    $user = user();
    $json = array('success' => false);
    $case = new ocase($args[0]);
    if ($case->get_id() != '') {
        if (!is_locked_user($user)) {
            lock_user($user);
            if ($user->get_id() != '' && $user->is_login()) {
                $caseCount = isset($_POST['count']) ? (min(10, ((int)$_POST['count']))) : 1;
                if ($case->is_available() && $case->allow_open_case_num($caseCount)) {
                    if ($case->get_type() == ocase::TYPE_DEFAULT) {
                        if ($case->get_price() > 0) {
                            $totalPrice = 0;
                            $userBalance = get_user_balance($user);
                            $userProfit = get_avail_user_profit($user);
                            $profitChance = (float)(get_setval('opencase_chance') / 100);
                            $enabledItems = db()->query('select * from opencase_itemincase where case_id = "' . $case->get_id() . '" and (count_items = -1 or count_items > 0) and enabled = 1 and chance > 0 order by chance DESC');
                            $totalChance = (float)($user->get_data('chance') / 100) * (float)($case->get_chance() / 100);
                            $checkItemsPrice = $case->get_price();
                            $items = [];
                            $otherItems = [];
                            foreach ($enabledItems as $item) {
                                $tmpItem = new item($item['item_id']);
                                $itemChanse = $item['chance'];
                                if ($tmpItem->get_price() <= $checkItemsPrice) {
                                    if ($totalChance > 0) {
                                        $itemChanse /= $totalChance;
                                    }
                                } else {
                                    if ($totalChance <= 0) {
                                        $otherItems[$item['id']] = array('itemincase_id' => $item['id'], 'count_items' => $item['count_items'], 'name' => $tmpItem->get_name(), 'chance' => $itemChanse, 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'rarity' => $tmpItem->get_css_quality_class(), 'quality' => $tmpItem->get_quality(), 'price' => $tmpItem->get_price());
                                        continue;
                                    }
                                    $itemChanse *= $totalChance;
                                }
                                $items[$item['id']] = array('itemincase_id' => $item['id'], 'count_items' => $item['count_items'], 'name' => $tmpItem->get_name(), 'chance' => $itemChanse, 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'rarity' => $tmpItem->get_css_quality_class(), 'quality' => $tmpItem->get_quality(), 'price' => $tmpItem->get_price());
                            }
                            if (empty($items)) {
                                $items = $otherItems;
                            }
                            if (count($items) > 0) {
                                $checkOnlyHave = false;
                                if (get_setval('opencase_drop_only_have') == 1) {
                                    $botItems = db()->query('select * from opencase_invitems where status = 0');
                                    $checkOnlyHave = true;
                                }
                                $fast = isset($_POST['fast']) ? 1 : 0;
                                $result = [];
                                for ($countKey = 0; $countKey < $caseCount; $countKey++) {
                                    if (count($items) > 0) {
                                        $casePrice = $case->get_final_price();
                                        $totalPrice += $casePrice;
                                        if ($userBalance >= $totalPrice) {
                                            $availProfit = $casePrice * $profitChance + $userProfit;
                                            $haveItems = [];
                                            foreach ($items as $item) {
                                                if ($item['price'] <= $availProfit) {
                                                    $haveItems[] = $item;
                                                }
                                            }
                                            if ($checkOnlyHave) {
                                                $haveItemTmp = $haveItems;
                                                foreach ($haveItems as $key => $hItem) {
                                                    foreach ($botItems as $bKey => $botItem) {
                                                        if ($hItem['name'] == $botItem['market_hash_name']) {
                                                            unset($botItems[$bKey]);
                                                            continue 2;
                                                        }
                                                    }
                                                    unset($haveItems[$key]);
                                                }
                                                if (empty($haveItems)) {
                                                    $haveItems = $haveItemTmp;
                                                }
                                            }
                                            $item = false;
                                            if (empty($haveItems)) {
                                                $haveItems = $items;
                                                usort($haveItems, 'sortItemByPrice');
                                                $item = array_shift($haveItems);
                                            } else {
                                                $sum = 0;
                                                foreach ($haveItems as $key => $hItem) {
                                                    $sum += $hItem['chance'];
                                                }
                                                $chance = rand(0, $sum - 1);
                                                $i = 0;
                                                foreach ($haveItems as $hItem) {
                                                    if ($chance >= $i && $chance < $i + (int)$hItem['chance']) {
                                                        $item = $hItem;
                                                        break;
                                                    }
                                                    $i += (int)$hItem['chance'];
                                                }
                                            }
                                            if ($item) {
                                                if ($items[$item['itemincase_id']]['count_items'] > 0) {
                                                    $items[$item['itemincase_id']]['count_items']--;
                                                    if ($items[$item['itemincase_id']]['count_items'] == 0) {
                                                        unset($items[$item['itemincase_id']]);
                                                    }
                                                }
                                                $result[] = [
                                                    'item' => $item,
                                                    'price' => $casePrice
                                                ];
                                                $changeProfit = $casePrice * ((float)(get_setval('opencase_chance') / 100)) - round($item['price']);
                                                $userProfit = max(0, round($userProfit + $changeProfit));
                                            } else {
                                                $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                                                break;
                                            }
                                        } else {
                                            $json['error'] = 'У Вас недостаточно средств для открытия этого кейса';
                                            break;
                                        }
                                    } else {
                                        $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                                        break;
                                    }
                                }
                                if (!empty($result)) {
                                    $json['items'] = [];
                                    foreach ($result as $res) {
                                        $item = $res['item'];
                                        $itemPrice = round($item['price']);
                                        $dItem = new droppedItem();
                                        $dItem->set_parametrs('', $user->get_id(), $item['item_id'], 5, $itemPrice, '', 0, $case->get_id(), $fast, 0, 0, '', $item['withdrawable'], $item['usable']);
                                        $time = $dItem->add_droppedItem();
                                        $itemID = $dItem->get_id();
                                        $openCase = new openCase();
                                        $openCase->set_parametrs('', $user->get_id(), $case->get_id(), $itemID, $res['price'], '');
                                        $openCase->add_openCase();
                                        $itemincase = new itemincase($item['itemincase_id']);
                                        if ($itemincase->get_count_items() > 0) {
                                            $itemincase->set_count_items($itemincase->get_count_items() - 1);
                                            $itemincase->update_itemincase();
                                        }
                                        dec_user_balance($user, $res['price']);
                                        add_balance_log($user->get_id(), -$res['price'], 'Открытие кейса №' . $case->get_id() . ' (' . $case->get_name() . ')', 1);
                                        $json['items'][] = ['ID' => $itemID, 'name' => $item['name'], 'shortName' => $item['name'], 'quality' => $item['quality'] ?? '', 'image' => $item['image'], 'price' => $itemPrice, 'rarity' => $item['rarity'] ?? '', 'usable' => ((bool)$item['usable'])];
                                        centrifugo::sendItem($dItem, $time);
                                    }
                                    $case->set_open_count($case->get_open_count() + $caseCount);
                                    $case->update_ocase();
                                    set_avail_user_profit($user, $userProfit);
                                    update_setval('opencase_count_open_case', get_setval('opencase_count_open_case') + $caseCount);
                                    centrifugo::sendStats();
                                    $json['success'] = true;
                                }
                            } else {
                                $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                            }
                        } else {
                            $json['error'] = 'В данный момент, этот кейс недоступен';
                        }
                    } else {
                        $json['error'] = 'Этот кейс можно открывать только один раз';
                    }
                } else {
                    $json['error'] = 'В данный момент, этот кейс недоступен';
                }
            } else {
                $json['error'] = 'Вы не авторизованны на сайте';
            }
            unlock_user($user);
        } else {
            $json['error'] = 'Вы не можете выполнить это действие, т.к. в данный момент выполняется другое действие';
        }
    } else {
        $json['error'] = 'Такого кейса не существует';
    }
    $timeEnd = microtime(true);
    $json['speed'] = $timeEnd - $timeStart;
    echo_json($json);
}

/**
 * Пользователь запросил вывод предмета
 * @param $args
 * @return void
 */
function opencase_withdraw_with_analogs($args)
{
    $user = user();
    $json = array('success' => false);
    if ($user->get_data('trade_link') != '') {
        $droppedItem = new droppedItem($args[0]);

        //TODO отправить уведомление через телеграм-бота админу
        $link = $user->get_data('trade_link');
        $TELEGRAM_TOKEN = '5882696012:AAHvN-L4fUzkJI4JawRQcyB0GleP-3kkAcg'; // токен бота
        $TELEGRAM_CHATID = '6183351309'; // ваш внутренний ID
        $USER_ID = explode(" ", $link)[0]; // userId
        $ZONE_ID = explode(" ", $link)[1]; // zoneId
        $PRICE = $droppedItem->get_price(); // price
        $send_bot_message = "*Заявка на получение алмазов*\n_userId_: ```".$USER_ID."```\n_zoneId_: ```".$ZONE_ID."```\n_price_: *".$PRICE.'*';
        $website = 'https://api.telegram.org/bot'.$TELEGRAM_TOKEN;
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL,$website."/sendMessage");
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query(array(
            'chat_id' => $TELEGRAM_CHATID,
            'parse_mode' => 'markdown',
            'text' => $send_bot_message
        )));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // Не возвращать ответ
        curl_exec($ch);
        curl_close($ch);

        // тупо меняем статус предмета
        $droppedItem->set_status(1);
        $droppedItem->update_droppedItem();

        $json['success'] = true;
        $json['quick'] = true;
        $json['msg'] = 'Предмет подготовлен к получению, в течении 5-10минут наш бот отправит его Вам.';
    } else {
        $json['error'] = 'У Вас не установлен UserID|ZoneID';
    }

    if (false) { // отключили стандартное поведение при запросе вывода
        if ($user->get_id() != '' && $user->is_login()) {
            if ($user->get_data('trade_link') != '') {
                $queryStr = parse_url($user->get_data('trade_link'), PHP_URL_QUERY);
                $queryArray = [];
                parse_str($queryStr, $queryArray);
                if (!isset($queryArray['partner']) && !isset($queryArray['token'])) {
                    if ($user->get_data('withdraw_disabled') != 1) {
                        if ($droppedItem->get_withdrawable() && $droppedItem->get_user_id() == $user->get_id() && ($droppedItem->get_status() == 0 || $droppedItem->get_status() == 6)) {
                            $countWithDraw = db()->query_once('SELECT count(id) from opencase_droppeditems where user_id = ' . $user->get_id() . ' and status = 1');
                            if ($countWithDraw['count(id)'] < 5) {
                                $botEvent = new botEvent();
                                $dataReady = false;
                                if (get_setval('opencase_withdraw_type') != WITHDRAW_TYPE_ONLY_ADMIN_VIVOD) {
                                    $json['msg'] = 'Предмет подготовлен к получению, в течение 2 минут наш бот отправит его Вам.';
                                }
                                if (get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_ONLY_BOT) {
                                    $invItem = new invItems();
                                    $invItem = $invItem->get_invItemss('market_hash_name = "' . $droppedItem->get_item_name_alt() . '" and status = 0 and tradable = 1 and created_at < (NOW() - INTERVAL 5 MINUTE)', '', 1);
                                    if (count($invItem) > 0) {
                                        $invItem = $invItem[0];
                                        $invItem->set_status(1);
                                        $invItem->update_invItems();
                                        $droppedItem->set_status(1);
                                        $droppedItem->set_bot_id($invItem->get_bot_id());
                                        $droppedItem->update_droppedItem();
                                        $additional = array(
                                            'msg' => '',
                                            'tradeUrl' => $user->get_data('trade_link'),
                                            'ditem' => $droppedItem->get_id(),
                                            'appid' => get_setval('opencase_gameid')
                                        );
                                        $botEvent->set_parametrs('', $invItem->get_bot_id(), 1, json_encode($additional), $invItem->get_id(), 0, '', '');
                                        $botEvent->add_botEvent();
                                        $json['success'] = true;
                                        $json['quick'] = true;
                                        $json['msg'] = 'Предмет подготовлен к получению, в течение 2 минут наш бот отправит его Вам.';
                                        $dataReady = true;
                                    }
                                }
                                if (!$dataReady && get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_ONLY_MARKET) {
                                    $hasError = true;
                                    $botId = db()->query_once('SELECT id FROM opencase_bot WHERE market_enable = 1 ORDER BY RAND() LIMIT 1');
                                    if (isset($botId['id'])) {
                                        $bot = new bot($botId['id']);
                                        if ($bot->get_id() != '' && $bot->get_market_enable()) {
                                            $needCheckAnalogs = true;
                                            $isAnalog = false;
                                            $item = $droppedItem->get_item_class();
                                            if (!empty($_POST['analog'])) {
                                                $needCheckAnalogs = false;
                                                if ($_POST['analog'] == $droppedItem->get_analog_id()) {
                                                    $item = new item($droppedItem->get_analog_id());
                                                    $isAnalog = true;
                                                }
                                            }
                                            $currentPriceMul = 1;
                                            $marketItems = get_items_by_market_hash_name($bot->get_decrypted_market_key(), $item->get_name(), $currentPriceMul);
                                            if (!empty($marketItems)) {
                                                $marketItem = select_market_item_from_array($marketItems, $item->get_price() * $currentPriceMul);
                                                if (!empty($marketItem)) {
                                                    $botEvent = new botEvent();
                                                    $botEvent->add_botEvent();
                                                    $botEvent = new botEvent(db()->get_last_id());
                                                    if ($botEvent->get_id() != '') {
                                                        $customId = $botEvent->get_id() . time();
                                                        $error = '';
                                                        $marketItemId = buy_market_item_for($bot->get_decrypted_market_key(), $marketItem, $queryArray['partner'], $queryArray['token'], $customId, $error);
                                                        if ($marketItemId) {
                                                            $needCheckAnalogs = false;
                                                            $hasError = false;
                                                            $droppedItem->set_status(1);
                                                            $droppedItem->set_bot_id($bot->get_id());
                                                            $droppedItem->update_droppedItem();
                                                            $additional = array(
                                                                'msg' => '',
                                                                'tradeUrl' => $user->get_data('trade_link'),
                                                                'ditem' => $droppedItem->get_id(),
                                                                'appid' => get_setval('opencase_gameid'),
                                                                'marketCustomId' => $customId
                                                            );
                                                            $botEvent->set_bot_id($bot->get_id());
                                                            $botEvent->set_event(50);
                                                            $botEvent->set_additional(json_encode($additional));
                                                            $botEvent->set_status(1);
                                                            $botEvent->update_botEvent();
                                                            if ($isAnalog) {
                                                                $addBalance = $droppedItem->get_price() - $item->get_price();
                                                                if ($addBalance > 0) {
                                                                    inc_user_balance($user, $addBalance);
                                                                    add_balance_log($user->get_id(), $addBalance, 'Разница стоимости при выводе аналога (' . $item->get_name() . ') для предмета ' . $droppedItem->get_id() . ' (' . $droppedItem->get_item_class()->get_name() . ')', 2);
                                                                }
                                                            }
                                                            $json['success'] = true;
                                                            $json['quick'] = false;
                                                            $json['msg'] = 'Вывод оформлен, ожидайте обмена.';
                                                        } else {
                                                            $botEvent->delete_botEvent();
                                                        }
                                                    }
                                                }
                                            }
                                            if ($needCheckAnalogs) {
                                                $itemIns = new item();
                                                $analogsItems = $itemIns->get_items('price <= ' . $droppedItem->get_price() . ' AND id <> ' . $droppedItem->get_item_class()->get_id(), 'price DESC', '3');
                                                foreach ($analogsItems as $analogsItem) {
                                                    $currentPriceMul = 1;
                                                    $marketItems = get_items_by_market_hash_name($bot->get_decrypted_market_key(), $analogsItem->get_name(), $currentPriceMul);
                                                    if (!empty($marketItems)) {
                                                        $marketItem = select_market_item_from_array($marketItems, $analogsItem->get_price() * $currentPriceMul);
                                                        if (!empty($marketItem)) {
                                                            $hasError = false;
                                                            $json['success'] = true;
                                                            $json['analog'] = [
                                                                'id' => $analogsItem->get_id(),
                                                                'name' => $analogsItem->get_name(),
                                                                'rarity' => $analogsItem->get_css_quality_class(),
                                                                'image' => $analogsItem->get_steam_image(),
                                                                'price' => $analogsItem->get_price(),
                                                            ];
                                                            $json['addBalance'] = $droppedItem->get_price() - $analogsItem->get_price();
                                                            $droppedItem->set_analog_id($analogsItem->get_id());
                                                            $droppedItem->update_droppedItem();
                                                            break;
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    if (!$hasError) {
                                        if (get_setval('opencase_gameid') == 730) {
                                            $domain = 'market.csgo.com';
                                        } elseif (get_setval('opencase_gameid') == 570) {
                                            $domain = 'market.dota2.net';
                                        } else {
                                            $domain = 'маркете';
                                        }
                                        $json['error'] = 'К сожалению в данный момент мы не смогли подобрать нужный лот для покупки на ' . $domain . ', попробуйте позже!';
                                    }
                                    $dataReady = true;
                                }
                                if (!$dataReady) {
                                    $user = user();
                                    $json = array('success' => false);
                                    $droppedItem = new droppedItem($args[0]);
                                    if ($user->get_id() != '' && $user->is_login()) {
                                        if ($droppedItem->get_user_id() == $user->get_id()) {
                                            if ($droppedItem->get_status() == 0 || $droppedItem->get_status() == 6) {
                                                $droppedItem->set_status(1);
                                                $droppedItem->update_droppedItem();

                                                //TODO здесь произвести отправку предмета на аккаунт пользователя ($userReceiver - получатель)
                                                $userReceiver = $droppedItem->get_user_class();
                                                $link = $userReceiver->get_data('trade_link');
                                                $json = array('success' => true);
                                                $json['msg'] = 'Предмет подготовлен к получению, в течение 5 минут наш бот отправит его Вам.';
                                            } else {
                                                $json['error'] = '1';
                                            }
                                        } else {
                                            $json['error'] = '2';
                                        }
                                    } else {
                                        $json['error'] = '3';
                                    }

                                    $json['success'] = true;
                                    $json['quick'] = false;
                                    $json['msg'] = 'Предмет подготовлен к получению, в течение 5-10 минут наш бот отправит его Вам.';
                                }
                            } else {
                                $json['error'] = 'У Вас есть неполученные предметы. Прежде чем продолжить выводить предметы, получите все отправленные предметы.';
                            }
                        } else {
                            $json['error'] = 'Этот предмет не может быть отправлен';
                        }
                    } else {
                        $json['error'] = 'Вывод предметов для Вас заблокирован';
                    }
                } else {
                    $json['error'] = ' У вас указана некорректная ссылка на обмен';
                }
            } else {
                $json['error'] = 'У Вас не установлена ссылка на обмен';
            }
        } else {
            $json['error'] = 'Вы не авторизованны на сайте';
        }
    }
    echo_json($json);
}

function opencase_sale_all_data()
{
    $user = user();
    $json = ['success' => false];
    if ($user->get_id() != '' && $user->is_login()) {
        $items = get_user_drops($user->get_id(), '(status = 0 OR status = 6)', 0, 0);
        if (count($items) > 0) {
            $price = 0;
            foreach ($items as $droppedItem) {
                $price += $droppedItem->get_price();
            }
            $json['success'] = true;
            $json['data'] = [
                'count' => count($items),
                'price' => $price
            ];
        } else {
            $json['error'] = 'Нет предметов для продажи';
        }
    } else {
        $json['error'] = 'Вы не авторизованны на сайте';
    }
    echo_json($json);
}
