<?php

add_post('/api/opencase/battle/cases/list/', 'opencase_battle_cases_list');
add_post('/api/opencase/battle/create/([0-9]+)/', 'opencase_battle_create');
add_post('/api/opencase/battle/join/([0-9]+)/', 'opencase_battle_join');
add_post('/api/opencase/battle/repeat/([0-9]+)/', 'opencase_battle_repeat');
add_post('/api/opencase/battle/([0-9]+)/', 'opencase_battle_info');
add_post('/api/opencase/checkbattle/([0-9]+)/', 'opencase_battle_check');
add_post('/api/opencase/battle/cancel/([0-9]+)/', 'opencase_battle_cancel');
add_post('/api/opencase/getuserbattles/', 'opencase_getuserbattles');

function opencase_battle_cases_list() {
	$json = ['success' => true, 'cases' => []];
	$cases = battle::getAvailForBattleCases();
	$activeCount = battle::getActiveBattlesByCaseCount();
	foreach ($cases as $case) {
		$json['cases'][] = [
			'caseId' => $case->get_id(),
			'active' => $activeCount[$case->get_id()] ?? 0,
			'key' => $case->get_key(),
			'name' => $case->get_name(),
			'image' => ($case->get_src_image() != '/uploads/' ? $case->get_src_image() : ($case->get_src_item_image() != '/uploads/' ? $case->get_src_item_image() : '')),
			'sale' => $case->get_total_sale(),
			'price' => $case->get_price(),
			'salePrice' => $case->get_sale_price(),
		];
	}
	if (is_login()) {
		$json['userStats'] = get_user_count_battles(user());
	}
	$json['stats'] = get_count_battles();
	$json['lastBattle'] = get_last_battle();
	echo_json($json);
}

function opencase_battle_create($args) {
	$caseId = (int) $args[0];
	$json = ['success' => false];
	$user = user();
	if (!is_locked_user($user)) {
		lock_user($user);
		if ($user->get_id() != '' && $user->is_login()) {
			if (battle::isAvailForBattleCase($caseId)) {
				$battle = new battle();
				$battle->setCreatorId($user->get_id());
				$battle->setCaseId($caseId);
				if ($battle->getPrice() > 0) {
					if ($battle->getPrice() <= get_user_balance($user)) {
						$battle->save();
						$json['success'] = true;
						$json['id'] = $battle->getId();
						battleCentrifugo::updateBattlesList();
					} else {
						$json['error'] = 'У Вас недостаточно средств';
					}
				} else {
					$json['error'] = 'Произошла ошибка при создании сражения';
				}
			} else {
				$json['error'] = 'Произошла ошибка при создании сражения';
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

function opencase_battle_join($args) {
	$caseId = (int) $args[0];
	$user = user();
	$battle = battle::getActiveBattleByCaseId($caseId, $user->get_id());
	$json = ['success' => false];
	if (!is_null($battle)) {
		if (!is_locked_user($user)) {
			lock_user($user);
			if ($user->get_id() != '' && $user->is_login()) {
				if ($battle->getCreatorId() != $user->get_id()) {
					if (get_user_balance($user) >= $battle->getPrice()) {
						$battle->addParticipant($user);
						$json['success'] = true;
						$json['id'] = $battle->getId();
						battleCentrifugo::updateBattlesList();
						battleCentrifugo::updateBattleStatus($battle);
					} else {
						$json['error'] = 'У Вас недостаточно средств';
					}
				} else {
					$json['success'] = true;
					$json['id'] = $battle->getId();
				}
			} else {
				$json['error'] = 'Вы не авторизованны на сайте';
			}
			unlock_user($user);
		} else {
			$json['error'] = 'Вы не можете выполнить это действие, т.к. в данный момент выполняется другое действие';
		}
	} else {
		$json['error'] = 'Не удалось найти активное сражение';
	}
	echo_json($json);
}

function opencase_battle_repeat($args) {
	$caseId = (int) $args[0];
	$battle = battle::getActiveBattleByCaseId($caseId);
	if (!is_null($battle)) {
		opencase_battle_join($args);
	} else {
		opencase_battle_create($args);
	}
}

function opencase_battle_info($args) {
	$json = ['success' => false];
	$battle = new battle($args[0]);
	if ($battle->getId() != '' && $battle->getStatus() != battle::STATUS_CANCEL) {
		$case = $battle->getCase();
		$json['battle'] = [
			'id' => $battle->getId(),
			'creator' => $battle->getUserData($battle->getCreator()),
			'participant' => $battle->getUserData($battle->getParticipant()),
			'case' => [
				'caseId' => $case->get_id(),
				'key' => $case->get_key(),
				'name' => $case->get_name(),
				'image' => ($case->get_src_image() != '/uploads/' ? $case->get_src_image() : ($case->get_src_item_image() != '/uploads/' ? $case->get_src_item_image() : '')),
				'items' => $battle->getItemsInCase()
			],
			'status' => $battle->getStatus(),
			'price' => $battle->getPrice(),
			'winnerId' => $battle->getWinnerId()
		];
		if ($battle->getStatus() == battle::STATUS_PROGRESS) {
			$result = $battle->getAdditional();
			if ($result) {
				$json['result'] = $result;
			}
		}
		$json['success'] = true;
	}
	echo_json($json);
}

function opencase_battle_check($args) {
	$json = ['success' => false];
	$battle = new battle($args[0]);
	if ($battle->getId() != '') {
		$json['creator'] = $battle->getUserData($battle->getCreator());
		$json['participant'] = $battle->getUserData($battle->getParticipant());
		$status = $battle->getStatus();
		$json['status'] = $status;
		if ($status == battle::STATUS_PROGRESS) {
			$result = $battle->getAdditional();
			if ($result) {
				$json['result'] = $result;
			}
			$json['winnerId'] = $battle->getWinnerId();
		}
		$json['success'] = true;
	} else {
		$json['error'] = 'Указанная игра не существует';
	}
	echo_json($json);
}

function opencase_battle_cancel($args) {
	$json = ['success' => false];
	$battle = new battle($args[0]);
	if ($battle->getId() != '') {
		$user = user();
		if ($user->get_id() != '' && $user->is_login()) {
			if ($battle->getStatus() == battle::STATUS_WAITING) {
				if ($user->get_id() == $battle->getCreatorId()) {
					$battle->cancelGame();
					$json['success'] = true;
					battleCentrifugo::updateBattlesList();
					battleCentrifugo::updateBattleStatus($battle);
				} else {
					$json['error'] = 'Эта игра создана не вами';
				}
			} else {
				$json['error'] = 'Эта игра уже запущена';
			}
		} else {
			$json['error'] = 'Вы не авторизованны на сайте';
		}
	} else {
		$json['error'] = 'Указанная игра не существует';
	}
	echo_json($json);
}

function opencase_getuserbattles() {
	$json = array('success' => false, 'not_items' => true);
	if (isset($_POST['page']) && isset($_POST['user_id'])) {
		$userId = (int) $_POST['user_id'];
		$countPerPage = 8;
		$battles = battle::getBattles('status = ' . battle::STATUS_FINISHED . ' AND (creator_id = "' . $userId . '" OR participant_id = "' . $userId . '")', '', (((int) $_POST['page']) * $countPerPage) . ', ' . $countPerPage);
		if (count($battles) > 0) {
			$battlesData = [];
			foreach ($battles as $battle) {
				$case = $battle->getCase();
				$battlesData[] = [
					'creator' => $battle->getUserData($battle->getCreator()),
					'participant' => $battle->getUserData($battle->getParticipant()),
					'winnerId' => $battle->getWinnerId(),
					'status' => $battle->getStatus(),
					'price' => $battle->getPrice(),
					'case' => [
						'caseId' => $case->get_id(),
						'key' => $case->get_key(),
						'name' => $case->get_name(),
						'image' => ($case->get_src_image() != '/uploads/' ? $case->get_src_image() : ($case->get_src_item_image() != '/uploads/' ? $case->get_src_item_image() : '')),
						'items' => $battle->getItemsInCase()
					]
				];
			}
			if (count($battles) >= $countPerPage) {
				$json['not_items'] = false;
			}
			$json['success'] = true;
			$json['items'] = $battlesData;
		} else {
			$json['error_code'] = 'Not items';
		}
	} else {
		$json['error_code'] = 'Invalid parameters';
		$json['not_items'] = false;
	}
	echo_json($json);
}
