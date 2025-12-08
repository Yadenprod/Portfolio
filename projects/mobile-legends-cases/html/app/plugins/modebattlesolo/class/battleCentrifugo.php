<?php

require_once PLUGINFOLDER . '/opencase/class/centrifugo.php';

class battleCentrifugo extends centrifugo {

	public static function updateBattleStatus($battle) {
		if (!self::ENABLED) {
			return;
		}
		try {
			$json = ['success' => false];
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
			self::getInstance()->publish("uptadeBattle" . $battle->getId(), $json);
		} catch (\Exception $ex) {
			
		}
	}

	public static function updateBattlesList() {
		if (!self::ENABLED) {
			return;
		}
		try {
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
			$json['stats'] = get_count_battles();
			$json['lastBattle'] = get_last_battle();
			self::getInstance()->publish("uptadeBattleList", $json);
		} catch (\Exception $ex) {
			
		}
	}

}
