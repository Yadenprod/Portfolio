<?php

add_post('/api/opencase/upgrade/', 'opencase_upgrade');
add_post('/api/opencase/upgrade/getavaillist/', 'opencase_avail_upgrade_result_list');
add_post('/api/opencase/getuserupgrades/', 'opencase_getuserupgrades');

function opencase_upgrade() {
	$user = user();
	$json = ['success' => false];
	if (!is_locked_user($user)) {
		lock_user($user);
		if ($user->get_id() != '' && $user->is_login()) {
			if ((isset($_POST['source']) || !(empty($_POST['balance']) && $_POST['balance'] > 0)) && isset($_POST['target'])) {
				$additionalBalance = (!(empty($_POST['balance'])) && $_POST['balance'] > 0) ? ((int) $_POST['balance']) : 0;
				if (get_user_balance($user) >= $additionalBalance) {
					$sourceItem = false;
					if (isset($_POST['source'])) {
						$sourceItem = new droppedItem($_POST['source']);
					}
					if (!$sourceItem || $sourceItem->get_id() != '' && $sourceItem->get_user_id() == $user->get_id() && $sourceItem->get_usable() && ($sourceItem->get_status() == 0 || $sourceItem->get_status() == 6)) {
						$targetItem = new item($_POST['target']);
						$sourcePrice = $additionalBalance;
						if ($sourceItem) {
							$sourcePrice += $sourceItem->get_price();
						}
						if ($sourcePrice > 0) {
							if ($targetItem->get_id() != '' && floor($sourcePrice * 1.25) <= $targetItem->get_price()) {
								$wonPercent = min(0.75, $sourcePrice / $targetItem->get_price() * 0.93);						
								$randomPercent = lcg_value();
								$userChanse = (float) ($user->get_data('chance') / 100);
								$checkWonPercent = $wonPercent;
								if ($userChanse >= 1) {
									$checkWonPercent = min((1 - (1 - $checkWonPercent) / $userChanse), ($checkWonPercent * $userChanse));
								} else {
									$checkWonPercent *= $userChanse;
								}
								$userProfit = get_avail_user_profit($user);
								$availableProfit = ($sourcePrice) * (float) (get_setval('opencase_chance') / 100) + $userProfit;
								$wonItemId = 0;
								if ($targetItem->get_price() > $availableProfit) {
									$lostPercent = 1 - $wonPercent - 0.01;
									$randomPercent = 1 - $randomPercent * $lostPercent;
									$isWon = false;
									$realProfit = $sourcePrice;
								} elseif ($randomPercent <= $checkWonPercent) {
									if ($randomPercent > $wonPercent) {
										$randomPercent *= $wonPercent;
									}
									$isWon = true;
									$realProfit = $sourcePrice - $targetItem->get_price();
									$dItem = new droppedItem();
									$itemPrice = round($targetItem->get_price());
									$dItem->set_parametrs('', $user->get_id(), $targetItem->get_id(), 5, $itemPrice, '', 0, DROPPED_ITEM_FROM_UPGRADE, 0, 0, 0);
									$time = $dItem->add_droppedItem(4);
									$wonItemId = $dItem->get_id();
								} else {
									if ($randomPercent <= $wonPercent) {
										$lostPercent = 1 - $wonPercent - 0.01;
										$randomPercent = 1 - $randomPercent * $lostPercent;
									}
									$isWon = false;
									$realProfit = $sourcePrice;
								}
								$upgrade = new upgrade();
								$upgrade->setUserId($user->get_id());
								$upgrade->setItemId($wonItemId);
								if ($sourceItem) {
									$upgrade->setSourceId($sourceItem->get_id());
								} else {
									$upgrade->setSourceId(-1);
								}
								$upgrade->setTargetId($targetItem->get_id());
								$upgrade->setImage(!empty($_POST['image']) ? db()->nomysqlinj(str_replace(' ', '+', $_POST['image'])) : '');
								$upgrade->setStatus($isWon ? upgrade::STATUS_SUCCESS : upgrade::STATUS_FAIL);
								$upgrade->setAdditionalBalance($additionalBalance);
								$upgrade->save();
								if ($additionalBalance > 0) {
									$upgradeId = db()->get_last_id();
									dec_user_balance($user, $additionalBalance);
									add_balance_log($user->get_id(), -$additionalBalance, 'Добавление баланса к апгрейду №' . $upgradeId, 1);
								}
								if ($sourceItem) {
									$sourceItem->set_status(DROPPED_ITEM_STATUS_UPGRADED);
									$sourceItem->update_droppedItem();
								}
								$needProfit = $sourcePrice * (1 - (float) (get_setval('opencase_chance') / 100));
								$descProfit = $realProfit - $needProfit;
								set_avail_user_profit($user, round($userProfit + $descProfit));
								update_setval('opencase_count_upgrades', get_setval('opencase_count_upgrades') + 1);
								centrifugo::sendStats();
								$json['item'] = ['ID' => $wonItemId, 'name' => $targetItem->get_name(), 'quality' => $targetItem->get_quality(), 'image' => $targetItem->get_image(), 'price' => $targetItem->get_price(), 'price' => $targetItem->get_price(), 'rarity' => $targetItem->get_css_quality_class()];
								$json['percent'] = $randomPercent;
								$json['won'] = $isWon;
								$json['success'] = true;
								if (isset($dItem) && isset($time)) {
									centrifugo::sendItem($dItem, $time);
								}
							} else {
								$json['error'] = 'Вы не можете улучшить в этот предмет';
							}
						} else {
							$json['error'] = 'Вы не выбрали предметы';
						}
					} else {
						$json['error'] = 'Вы не можете улучшить этот предмет';
					}
				} else {
					$json['error'] = 'У Вас недостаточно средств';
				}
			} else {
				$json['error'] = 'Вы не выбрали предметы';
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

function opencase_avail_upgrade_result_list() {
	$json = ['success' => false];
	if (isset($_POST['page']) && isset($_POST['limit']) && isset($_POST['minprice']) && isset($_POST['search'])) {
		$allitems = get_avail_upgrade_result_list((int) $_POST['page'], (int) $_POST['limit'], (intval($_POST['minprice'])), $_POST['search'], (!empty($_POST['maxprice']) ? intval($_POST['maxprice']) : 0), (empty($_POST['order']) ? 'ASC' : 'DESC'));
		$json['items'] = [];
		foreach ($allitems as $value) {
			array_push($json['items'], [
				'id' => $value->get_id(),
				'name' => $value->get_name(),
				'quality' => $value->get_css_quality_class(),
				'rarity' => $value->get_css_quality_class(),
				'image' => $value->get_steam_image(),
				'price' => $value->get_price(),
			]);
		}
		$json['success'] = true;
	}
	echo_json($json);
}

function opencase_getuserupgrades() {
	$json = array('success' => false, 'not_items' => true);
	if (isset($_POST['page']) && isset($_POST['user_id'])) {
		$where = [];
		if (!empty($_POST['min'])) {
			$where[] = 'item.price >= "' . db()->nomysqlinj($_POST['min']) . '"';
		}
		if (!empty($_POST['max'])) {
			$where[] = 'item.price <= "' . db()->nomysqlinj($_POST['max']) . '"';
		}
		$notSaled = false;
		if (isset($_POST['notSaled']) && $_POST['notSaled']) {
			$where[] = '(item.status = 0 OR item.status = 6)';
			$notSaled = true;
		}
		$countPerPage = 8;
		$sql = 'SELECT upgrade.id FROM opencase_upgrades upgrade '
				. (empty($where) ? '' : ($notSaled ? 'INNER JOIN opencase_droppeditems item ON upgrade.item_id = item.id ' : 'INNER JOIN opencase_items item ON upgrade.target_id = item.id '))
				. 'WHERE upgrade.user_id = ' . db()->nomysqlinj($_POST['user_id']) . (empty($where) ? '' : (' AND ' . implode(' AND ', $where))) . ' '
				. 'ORDER BY id DESC '
				. 'LIMIT ' . (db()->nomysqlinj($_POST['page']) * $countPerPage) . ', ' . $countPerPage;

		$upgradesArray = db()->query($sql);
		$upgrades = [];
		if (is_array($upgradesArray)) {
			foreach ($upgradesArray as $upgradeElement) {
				$upgrade = new upgrade($upgradeElement['id']);
				array_push($upgrades, $upgrade);
			}
		}
		if (count($upgrades) > 0) {
			$other = true;
			if (is_login() && user()->get_id() == $_POST['user_id']) {
				$other = false;
			}
			$items = array();
			foreach ($upgrades as $upgrade) {
				$source = $upgrade->getSource();
				$target = $upgrade->getTarget();
				$item = [
					'status' => $upgrade->getStatus(),
					'from' => [
						'image' => $source->get_item_class()->get_steam_image('200f', '100'),
						'rarity' => $source->get_item_class()->get_css_quality_class(),
						'name' => $source->get_item_name(),
						'price' => $source->get_price(),
					],
					'to' => [
						'image' => $target->get_steam_image('200f', '100'),
						'rarity' => $target->get_css_quality_class(),
						'name' => $target->get_name(),
						'price' => $target->get_price(),
					],
				];
				array_push($items, $item);
			}
			if (count($upgrades) >= $countPerPage) {
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
