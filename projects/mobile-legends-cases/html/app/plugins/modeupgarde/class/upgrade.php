<?php

class upgrade {

	const STATUS_UNKNOWN = 0;
	const STATUS_SUCCESS = 1;
	const STATUS_FAIL = 2;

	private static $statusArray = [self::STATUS_UNKNOWN => 'Неизвестно', self::STATUS_SUCCESS => 'Успех', self::STATUS_FAIL => 'Неудача'];
	private static $statusLabelArray = [self::STATUS_UNKNOWN => 'warning', self::STATUS_SUCCESS => 'success', self::STATUS_FAIL => 'danger'];
	private $id = '';
	private $userId = '';
	private $itemId = 0;
	private $sourceId = '';
	private $targetId = '';
	private $additionalBalance = 0;
	private $status = self::STATUS_UNKNOWN;
	private $image = '';
	private $createdAt = '';
	private $user = null;
	private $source = null;
	private $target = null;
	private $item = null;

	public function __construct($id = '') {
		if ($id != '') {
			$this->load(db()->nomysqlinj($id));
		}
	}

	private function load($id) {
		$cache = ch()->get('upgrade' . $id);
		if (!$cache) {
			$data = db()->query_once('SELECT * FROM opencase_upgrades WHERE id = "' . $id . '"');
			if (!empty($data)) {
				$this->id = $data['id'];
				$this->setUserId($data['user_id']);
				$this->setItemId($data['item_id']);
				$this->setSourceId($data['source_id']);
				$this->setTargetId($data['target_id']);
				$this->setStatus($data['status']);
				$this->setImage($data['image']);
				$this->setCreatedAt($data['created_at']);
				$this->setAdditionalBalance($data['balance']);
				ch()->set('upgrade' . $data['id'], $this);
			}
		} else {
			$this->id = $cache->getId();
			$this->setUserId($cache->getUserId());
			$this->setItemId($cache->getItemId());
			$this->setSourceId($cache->getSourceId());
			$this->setTargetId($cache->getTargetId());
			$this->setStatus($cache->getStatus());
			$this->setImage($cache->getImage());
			$this->setCreatedAt($cache->getCreatedAt());
			$this->setAdditionalBalance($cache->getAdditionalBalance());
		}
	}

	public function getId() {
		return $this->id;
	}

	public function getUserId() {
		return $this->userId;
	}

	public function setUserId($userId) {
		$this->userId = $userId;
	}

	public function getItemId() {
		return $this->itemId;
	}

	public function setItemId($itemId) {
		$this->itemId = $itemId;
	}

	public function getSourceId() {
		return $this->sourceId;
	}

	public function setSourceId($sourceId) {
		$this->sourceId = $sourceId;
	}

	public function getTargetId() {
		return $this->targetId;
	}

	public function setTargetId($targetId) {
		$this->targetId = $targetId;
	}

	public function getStatus() {
		return $this->status;
	}

	public function setStatus($status) {
		$this->status = $status;
	}

	public function getImage() {
		return $this->image;
	}

	public function setImage($image) {
		$this->image = $image;
	}

	public function getAdditionalBalance() {
		return $this->additionalBalance;
	}

	public function setAdditionalBalance($additionalBalance) {
		$this->additionalBalance = $additionalBalance;
	}

	public function getCreatedAt() {
		return $this->createdAt;
	}

	public function setCreatedAt($createdAt) {
		$this->createdAt = $createdAt;
	}

	public function save() {
		if (!empty($this->getId())) {
			db()->query_once('UPDATE opencase_upgrades set `user_id` = "' . $this->getUserId() . '", `item_id` = "' . $this->getItemId() . '", `source_id` = "' . $this->getSourceId() . '", `target_id` = "' . $this->getTargetId() . '", `status` = "' . $this->getStatus() . '", `image` = "' . $this->getImage() . '", `balance` = "' . $this->getAdditionalBalance() . '" WHERE id = "' . $this->getId() . '"');
			ch()->set('upgrade' . $this->getId(), $this);
		} else {
			db()->query_once('INSERT INTO opencase_upgrades (`user_id`, `item_id`, `source_id`, `target_id`, `status`, `image`,	`balance`) VALUES ( "' . $this->getUserId() . '", "' . $this->getItemId() . '", "' . $this->getSourceId() . '", "' . $this->getTargetId() . '", "' . $this->getStatus() . '", "' . $this->getImage() . '", "' . $this->getAdditionalBalance() . '")');
		}
	}

	public function delete() {
		db()->query_once('DELETE FROM opencase_upgrades WHERE id = "' . $this->getId() . '"');
		ch()->delete('upgrade' . $this->getId());
	}

	public function getUser() {
		if (empty($this->user)) {
			$this->user = new user($this->getUserId());
		}
		return $this->user;
	}

	public function getSource() {
		if (empty($this->source)) {
			$this->source = new droppedItem($this->getSourceId());
		}
		return $this->source;
	}

	public function getTarget() {
		if (empty($this->target)) {
			$this->target = new item($this->getTargetId());
		}
		return $this->target;
	}

	public function getProfit() {
		if ($this->getStatus() == self::STATUS_SUCCESS) {
			return $this->getSource()->get_price() + $this->getAdditionalBalance() - $this->getTarget()->get_price();
		} elseif ($this->getStatus() == self::STATUS_FAIL) {
			return $this->getSource()->get_price() + $this->getAdditionalBalance();
		}
		return 0;
	}

	function getItem() {
		if (empty($this->item)) {
			$this->item = new droppedItem($this->getItemId());
		}
		return $this->item;
	}

	public function getLabelStatus() {
		return '<span class = "label label-' . self::$statusLabelArray[$this->getStatus()] . '">' . self::$statusArray[$this->getStatus()] . '</span>';
	}

	public function getFormatCreatedAt($format = 'd.m.Y H:i:s') {
		return getdatetime($this->getCreatedAt(), $format);
	}

	public static function getUpgrades($where = '', $order = '', $limit = '') {
		$sql = 'SELECT id FROM opencase_upgrades';
		if ($where != '') {
			$sql .= ' WHERE ' . $where;
		}
		if ($order != '') {
			$sql .= ' ORDER BY ' . $order;
		}
		if ($limit != '') {
			$sql .= ' LIMIT ' . $limit;
		}
		$upgradesArray = db()->query($sql);
		$upgrades = [];
		if (is_array($upgradesArray)) {
			foreach ($upgradesArray as $upgradesElement) {
				array_push($upgrades, new upgrade($upgradesElement['id']));
			}
		}
		return $upgrades;
	}

	public static function getUpgradesCount() {
		$count = db()->query_once('SELECT COUNT(id) as count FROM opencase_upgrades');
		return $count['count'];
	}

}
