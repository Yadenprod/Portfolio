<?php

class battle {

	const STATUS_WAITING = 0;
	const STATUS_PROGRESS = 1;
	const STATUS_FINISHED = 2;
	const STATUS_CANCEL = 3;
	const ROUND_TIME = 15;

	private static $statusArray = [self::STATUS_WAITING => 'В очереди', self::STATUS_PROGRESS => 'В процессе', self::STATUS_FINISHED => 'Завершен', self::STATUS_CANCEL => 'Отменен'];
	private static $statusLabelArray = [self::STATUS_WAITING => 'default', self::STATUS_PROGRESS => 'warning', self::STATUS_FINISHED => 'success', self::STATUS_CANCEL => 'danger'];
	private $id = '';
	private $creatorId = '';
	private $participantId = null;
	private $winnerId = null;
	private $caseId = null;
	private $additional = '';
	private $parsedAdditional = '';
	private $price = 0;
	private $status = self::STATUS_WAITING;
	private $finishedAt = '';
	private $creator = null;
	private $participant = null;
	private $itemsInCase = [];

	public function __construct($id = '') {
		if ($id != '') {
			$this->load(db()->nomysqlinj($id));
		}
	}

	private function load($id) {
		$cache = ch()->get('battle' . $id);
		if (!$cache) {
			$data = db()->query_once('SELECT * FROM opencase_battle WHERE id = "' . $id . '"');
			if (!empty($data)) {
				$this->id = $data['id'];
				$this->creatorId = $data['creator_id'];
				$this->participantId = $data['participant_id'];
				$this->winnerId = $data['winner_id'];
				$this->caseId = $data['case_id'];
				$this->setAdditional($data['additional']);
				$this->status = $data['status'];
				$this->price = $data['price'];
				$this->finishedAt = strtotime($data['finished_at']);
				ch()->set('battle' . $data['id'], $this);
			}
		} else {
			$this->id = $cache->id;
			$this->creatorId = $cache->creatorId;
			$this->participantId = $cache->participantId;
			$this->winnerId = $cache->winnerId;
			$this->caseId = $cache->caseId;
			$this->setAdditional($cache->additional);
			$this->status = $cache->status;
			$this->price = $cache->price;
			$this->finishedAt = $cache->finishedAt;
			$this->itemsInCase = $cache->itemsInCase;
		}
	}

	public function getId() {
		return $this->id;
	}

	public function getStatus() {
		if ($this->status == self::STATUS_FINISHED) {
			if (time() - $this->finishedAt < 0) {
				return self::STATUS_PROGRESS;
			}
		}
		return $this->status;
	}

	public function getPrice() {
		return $this->price;
	}

	public function getCreatorId() {
		return $this->creatorId;
	}

	public function getCreator() {
		if (empty($this->creator)) {
			$this->creator = new user($this->getCreatorId());
		}
		return $this->creator;
	}

	public function getParticipantId() {
		return $this->participantId;
	}

	public function getParticipant() {
		if (empty($this->participant) && !is_null($this->getParticipantId())) {
			$this->participant = new user($this->getParticipantId());
		}
		return $this->participant;
	}

	public function getAdditional() {
		if ($this->parsedAdditional == '') {
			$this->parsedAdditional = json_decode($this->additional, true);
		}
		return $this->parsedAdditional;
	}

	public function setAdditional($str) {
		$this->additional = $str;
		$this->parsedAdditional = '';
	}

	public function setCreatorId($creatorId) {
		$this->creatorId = $creatorId;
	}

	public function setWinnerId($winnerId) {
		$this->winnerId = $winnerId;
	}

	public function getWinnerId() {
		return $this->winnerId;
	}

	public function addParticipant($user) {
		$this->participantId = $user->get_id();
		$this->payForBattle($user);
		$this->save();
		ch()->set('battle' . $this->id, $this);
		$this->tryStartBattle();
	}

	public function setCaseId($caseId) {
		$this->caseId = $caseId;
		$case = new ocase($this->caseId);
		if ($case->get_sale_price() > 0) {
			$this->price = $case->get_sale_price();
		}
	}

	public function getCase() {
		return new ocase($this->caseId);
	}

	public function save() {
		if (!empty($this->id)) {
			db()->query_once('UPDATE opencase_battle SET `creator_id` = "' . $this->creatorId . '", `participant_id` = ' . (empty($this->participantId) ? 'NULL' : '"' . $this->participantId . '"') . ', `winner_id` = ' . (empty($this->winnerId) ? 'NULL' : '"' . $this->winnerId . '"') . ', `case_id` = "' . $this->caseId . '", `additional` = "' . str_replace('"', '\\"', $this->additional) . '", `status` = "' . $this->status . '", `price` = "' . $this->price . '", `finished_at` = ' . (empty($this->finishedAt) ? 'NULL' : ('"' . date('Y-m-d H:i:s', $this->finishedAt) . '"')) . ' WHERE id = "' . $this->getId() . '"');
			ch()->set('battle' . $this->id, $this);
		} else {
			db()->query_once('INSERT INTO opencase_battle (`creator_id`, `participant_id`, `winner_id`, `case_id`, `additional`, `status`, `price`, `finished_at`) VALUES ( "' . $this->creatorId . '", ' . (empty($this->participantId) ? 'NULL' : '"' . $this->participantId . '"') . ', ' . (empty($this->winnerId) ? 'NULL' : '"' . $this->winnerId . '"') . ',"' . $this->caseId . '", "' . str_replace('"', '\\"', $this->additional) . '", "' . $this->status . '", "' . $this->price . '", ' . (empty($this->finishedAt) ? 'NULL' : ('"' . date('Y-m-d H:i:s', $this->finishedAt) . '"')) . ')');
			$this->id = db()->get_last_id();
			$this->payForBattle(new user($this->creatorId));
		}
	}

	public function getUserData($user) {
		if (is_null($user)) {
			return null;
		}
		$userRes = $this->getUserResult($user->get_id());
		return [
			'id' => $user->get_id(),
			'name' => $user->get_name(),
			'image' => $user->get_data('image'),
			'steam_id' => $user->get_data('steam_id'),
			'drop' => $userRes['drop'] ?? [],
		];
	}

	public function cancelGame() {
		if ($this->getStatus() == self::STATUS_WAITING) {
			$this->status = self::STATUS_CANCEL;
			$this->save();
			$users = [$this->getCreator(), $this->getParticipant()];
			foreach ($users as $user) {
				if (empty($user)) {
					continue;
				}
				inc_user_balance($user, $this->price);
				add_balance_log($user->get_id(), $this->price, 'Отмена участия в баттле  №' . $this->getId(), 1);
			}
		}
	}

	public function getItemsInCase() {
		if (empty($this->itemsInCase)) {
			$itemInst = new itemincase();
			$items = $itemInst->get_itemincases('case_id = ' . $this->caseId);
			$caseItems = [];
			foreach ($items as $item) {
				$caseItems[$item->get_item_class()->get_clear_name_key()] = $item;
			}
			foreach ($caseItems as $itemInCase) {
				$item = $itemInCase->get_item_class();
				$this->itemsInCase[] = [
					'id' => $item->get_id(),
					'name' => $item->get_name(),
					'image' => $item->get_steam_image('150fx132f'),
					'rarity' => $item->get_css_quality_class(),
				];
			}
		}
		return $this->itemsInCase;
	}

	private function getUserResult($userId) {
		if ($this->getStatus() != self::STATUS_PROGRESS && $this->getStatus() != self::STATUS_FINISHED) {
			return [];
		}
		$additional = $this->getAdditional();
		foreach ($additional as $res) {
			if ($res['userId'] == $userId) {
				if (isset($res['drop']['droppedItemId'])) {
					$droppedItem = new droppedItem($res['drop']['droppedItemId']);
					if ($droppedItem->get_id() != '') {
						$res['drop']['droppedItem'] = [
							'id' => $droppedItem->get_id(),
							'status' => $droppedItem->get_status(),
						];
					}
				}
				return $res;
			}
		}
		return [];
	}

	private function payForBattle($user) {
		dec_user_balance($user, $this->price);
		add_balance_log($user->get_id(), -$this->price, 'Участие в баттле  №' . $this->getId(), 1);
	}

	private function tryStartBattle() {
		$battleDrop = $this->findBattleDrop();
		if (empty($battleDrop)) {
			$this->cancelGame();
			return;
		}
		$resultData = [];
		$max = 0;
		$winnerId = -1;
		foreach ($battleDrop as $userId => $dropItemData) {
			if ($dropItemData['price'] > $max) {
				$max = $dropItemData['price'];
				$winnerId = $userId;
			} elseif ($dropItemData['price'] == $max) {
				$winnerId = -1;
			}
		}
		$this->setWinnerId($winnerId);
		foreach ($battleDrop as $userId => $dropItemData) {
			if ($winnerId == -1) {
				$itemId = $this->giveDroppedItemToUser($userId, $dropItemData);
			} else {
				$itemId = $this->giveDroppedItemToUser($winnerId, $dropItemData);
			}
			$resultData[] = [
				'userId' => $userId,
				'drop' => ['droppedItemId' => $itemId, 'id' => $dropItemData['item_id'], 'name' => $dropItemData['name'], 'rarity' => $dropItemData['quality'], 'image' => $dropItemData['image'], 'price' => $dropItemData['price']],
			];
		}
		$this->setAdditional(json_encode($resultData, JSON_UNESCAPED_UNICODE));
		$this->finishedAt = time() + self::ROUND_TIME;
		$this->status = self::STATUS_FINISHED;
		$this->save();
		update_setval('opencase_count_battles', get_setval('opencase_count_battles') + 1);
		centrifugo::sendStats();
	}

	private function findBattleDrop() {
		$case = new ocase($this->caseId);
		if ($case->get_id() == '' || !$case->is_available() || $case->get_type() != ocase::TYPE_DEFAULT || !$case->allow_open_case_num(2)) {
			return false;
		}
		$caseItems = [];
		$enabledCaseItems = db()->query('SELECT * FROM opencase_itemincase WHERE case_id = "' . $case->get_id() . '" AND (count_items = -1 OR count_items > 0) AND enabled = 1 AND chance > 0 ORDER BY chance DESC');
		foreach ($enabledCaseItems as $item) {
			$tmpItem = new item($item['item_id']);
			if ($tmpItem->get_id() != '') {
				$caseItems[$item['id']] = ['itemincase_id' => $item['id'], 'count_items' => $item['count_items'], 'name' => $tmpItem->get_name(), 'chance' => $item['chance'], 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'quality' => $tmpItem->get_css_quality_class(), 'price' => $tmpItem->get_price(), 'case_id' => $case->get_id(), 'case_price' => $case->get_sale_price()];
			}
		}
		if (empty($caseItems)) {
			return false;
		}
		$creator = $this->getCreator();
		$participant = $this->getParticipant();
		if (empty($creator) || empty($participant)) {
			return false;
		}
		$dropOnlyHave = get_setval('opencase_drop_only_have') == 1;
		$botItems = [];
		if ($dropOnlyHave) {
			$botItems = db()->query('SELECT * FROM opencase_invitems WHERE status = 0');
		}
		$users = [$creator, $participant];
		shuffle($users);
		$totalAvailUsersProfit = max(0, get_setval('opencase_userprofit'));
		$selfUsersProfit = [];
		$dropsData = [];
		foreach ($users as $user) {
			if ($user->get_data('use_self_profit') == 1) {
				$selfUsersProfit[$user->get_id()] = [
					'user' => $user,
					'currentProfit' => $user->get_data('self_profit')
				];
				$currentProfit = &$selfUsersProfit[$user->get_id()]['currentProfit'];
			} else {
				$currentProfit = &$totalAvailUsersProfit;
			}
			$dropItemData = $this->getUserCaseDropItemData($user, $case, $caseItems, $botItems, $currentProfit, $dropOnlyHave);
			if (empty($dropItemData)) {
				return false;
			}
			$dropsData[$user->get_id()] = $dropItemData;
		}
		$case->set_open_count($case->get_open_count() + 2);
		$case->update_ocase();
		update_setval('opencase_userprofit', $totalAvailUsersProfit);
		foreach ($selfUsersProfit as $profitData) {
			$profitData['user']->upd_data('self_profit', $profitData['currentProfit']);
		}
		update_setval('opencase_count_open_case', get_setval('opencase_count_open_case') + 2);
		return $dropsData;
	}

	private function getUserCaseDropItemData($user, $case, &$caseItems, $botItems, &$totalAvailUsersProfit, $dropOnlyHave) {
		if (empty($caseItems)) {
			return false;
		}
		$availableProfit = ($case->get_sale_price()) * (float) (get_setval('opencase_chance') / 100) + $totalAvailUsersProfit;
		$haveItems = [];
		$totalChance = (float) ($user->get_data('chance') / 100) * (float) ($case->get_chance() / 100);
		$checkItemsPrice = $case->get_price();
		foreach ($caseItems as $caseItem) {
			if ($caseItem['price'] <= $availableProfit) {
				if ($caseItem['price'] <= $checkItemsPrice) {
					if ($totalChance > 0) {
						$caseItem['chance'] /= $totalChance;
					}
				} else {
					if ($totalChance <= 0) {
						continue;
					}
					$caseItem['chance'] *= $totalChance;
				}
				$haveItems[] = $caseItem;
			}
		}
		if ($dropOnlyHave) {
			$haveItemTmp = $haveItems;
			foreach ($haveItems as $key => $hItem) {
				foreach ($botItems as $botItem) {
					if ($hItem['name'] == $botItem['market_hash_name']) {
						continue 2;
					}
				}
				unset($haveItems[$key]);
			}
			if (empty($haveItems)) {
				$haveItems = $haveItemTmp;
			}
		}
		$dropItemData = null;
		if (empty($haveItems)) {
			$haveItems = $caseItems;
			usort($haveItems, 'sortItemByPrice');
			$dropItemData = $haveItems[0];
		} else {
			$chanceSum = 0;
			foreach ($haveItems as $key => $hItem) {
				$chanceSum += $hItem['chance'];
			}

			$chance = rand(0, $chanceSum - 1);
			$i = 0;
			foreach ($haveItems as $hItem) {
				if ($chance >= $i && $chance < $i + (int) $hItem['chance']) {
					$dropItemData = $hItem;
					break;
				} else {
					$i += (int) $hItem['chance'];
				}
			}
		}
		if (empty($dropItemData)) {
			return false;
		}
		if ($caseItems[$dropItemData['itemincase_id']]['count_items'] > 0) {
			$caseItems[$dropItemData['itemincase_id']]['count_items'] --;
			if ($caseItems[$dropItemData['itemincase_id']]['count_items'] == 0) {
				unset($caseItems[$dropItemData['itemincase_id']]);
			}
		}
		$changeProfit = $case->get_sale_price() * ((float) (get_setval('opencase_chance') / 100)) - round($dropItemData['price']);
		$totalAvailUsersProfit = max(0, round($totalAvailUsersProfit + $changeProfit));
		return $dropItemData;
	}

	private function giveDroppedItemToUser($userId, $dropItemData) {
		$dItem = new droppedItem();
		$itemPrice = round($dropItemData['price']);
		$dItem->set_parametrs('', $userId, $dropItemData['item_id'], 5, $itemPrice, '', 0, DROPPED_ITEM_FROM_BATTLE, 0, 0, 0, '', $dropItemData['withdrawable'], $dropItemData['usable']);
		$time = $dItem->add_droppedItem(self::ROUND_TIME);
		$itemID = $dItem->get_id();
		$openCase = new openCase();
		$openCase->set_parametrs('', $userId, $dropItemData['case_id'], $itemID, $dropItemData['case_price'], '');
		$openCase->add_openCase();
		$itemincase = new itemincase($dropItemData['itemincase_id']);
		if ($itemincase->get_count_items() > 0) {
			$itemincase->set_count_items($itemincase->get_count_items() - 1);
			$itemincase->update_itemincase();
		}
		centrifugo::sendItem($dItem, $time);
		return $itemID;
	}

	public static function getBattles($where = '', $order = '', $limit = '') {
		$sql = 'SELECT id FROM opencase_battle';
		if ($where != '') {
			$sql .= ' WHERE ' . $where;
		}
		if ($order != '') {
			$sql .= ' ORDER BY ' . $order;
		}
		if ($limit != '') {
			$sql .= ' LIMIT ' . $limit;
		}
		$battlesArray = db()->query($sql);
		$battles = [];
		if (is_array($battlesArray)) {
			foreach ($battlesArray as $battlesElement) {
				array_push($battles, new battle($battlesElement['id']));
			}
		}
		return $battles;
	}

	public static function getBattlesCount() {
		$count = db()->query_once('SELECT COUNT(id) as count FROM opencase_battle');
		return $count['count'];
	}

	public static function getActiveBattlesByCaseCount() {
		$activeBattlesData = db()->query('SELECT COUNT(1) as count, case_id FROM opencase_battle WHERE status=' . self::STATUS_WAITING . ' GROUP BY case_id');
		$battlesByCaseCount = [];
		foreach ($activeBattlesData as $activeBattleData) {
			$battlesByCaseCount[$activeBattleData['case_id']] = $activeBattleData['count'];
		}
		return $battlesByCaseCount;
	}

	public static function getAvailForBattleCases() {
		$casesIds = db()->query('SELECT case_id FROM opencase_battle_cases ORDER BY position ASC');
		$cases = [];
		foreach ($casesIds as $caseIdData) {
			$case = new ocase($caseIdData['case_id']);
			if ($case->is_available() && $case->get_type() == ocase::TYPE_DEFAULT) {
				$cases[$case->get_id()] = $case;
			}
		}
		return $cases;
	}

	public static function isAvailForBattleCase($caseId) {
		$caseIdData = db()->query_once('SELECT case_id FROM opencase_battle_cases WHERE case_id = "' . $caseId . '"');
		if (isset($caseIdData['case_id']) && $caseIdData['case_id'] == $caseId) {
			$case = new ocase($caseId);
			return $case->is_available() && $case->get_type() == ocase::TYPE_DEFAULT;
		}
		return false;
	}

	public static function getActiveBattleByCaseId($caseId, $userId = 0) {
		$caseIdData = db()->query_once('SELECT id FROM opencase_battle WHERE participant_id IS NULL AND status=' . self::STATUS_WAITING . ' AND case_id = "' . $caseId . '" ORDER BY (creator_id = "' . $userId . '")');
		if (isset($caseIdData['id'])) {
			$battle = new battle($caseIdData['id']);
			if ($battle->getId() != '') {
				return $battle;
			}
		}
		return null;
	}

	public function getProfit() {
		if ($this->status == self::STATUS_FINISHED) {
			$additional = $this->getAdditional();
			$sum = 0;
			if (!empty($additional)) {
				foreach ($additional as $res) {
					$sum += $this->getPrice() - $res['drop']['price'];
				}
			}
			return $sum;
		}
		return 0;
	}

	public function getWonLabelByUserId($userId) {
		if ($userId == $this->winnerId) {
			$sum = 0;
			$additional = $this->getAdditional();
			if (!empty($additional)) {
				foreach ($additional as $res) {
					$sum += $res['drop']['price'];
				}
			}
			if ($sum > 0) {
				return ' <sup><i>' . $sum . ' руб</i></sup>';
			}
		} elseif ($this->winnerId == -1) {
			$additional = $this->getAdditional();
			if (!empty($additional)) {
				foreach ($additional as $res) {
					if ($res['userId'] == $userId) {
						return ' <sup><i>' . $res['drop']['price'] . ' руб</i></sup>';
					}
				}
			}
		}
		return '';
	}

	public function getFormatFinishedAt($format = 'd.m.Y H:i:s') {
		if (empty($this->finishedAt)) {
			return '-';
		}
		return date($format, $this->finishedAt);
	}

	public function getLabelStatus() {
		return '<span class = "label label-' . self::$statusLabelArray[$this->getStatus()] . '">' . self::$statusArray[$this->getStatus()] . '</span>';
	}

}
