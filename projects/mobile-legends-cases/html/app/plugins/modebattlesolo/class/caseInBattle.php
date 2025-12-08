<?php

class caseInBattle {

	private $caseId;
	private $position = 0;
	private $case = null;

	public function __construct($caseId = '') {
		if ($caseId != '') {
			$this->load(db()->nomysqlinj($caseId));
		}
	}

	private function load($caseId) {
		$cache = ch()->get('caseinbattle' . $caseId);
		if (!$cache) {
			$data = db()->query_once('SELECT * FROM opencase_battle_cases WHERE case_id = "' . $caseId . '"');
			if (!empty($data)) {
				$this->caseId = $data['case_id'];
				$this->position = $data['position'];
				ch()->set('caseinbattle' . $data['case_id'], $this);
			}
		} else {
			$this->caseId = $cache->caseId;
			$this->position = $cache->position;
		}
	}

	public function save() {
		db()->query_once('INSERT INTO opencase_battle_cases (`case_id`, `position`) VALUES ( "' . $this->caseId . '", "' . $this->position . '") ON DUPLICATE KEY UPDATE `position` = VALUES(`position`);');
		ch()->set('caseinbattle' . $this->caseId, $this);
	}

	public function delete() {
		db()->query_once('DELETE FROM opencase_battle_cases WHERE case_id = "' . $this->caseId . '"');
		ch()->delete('caseinbattle' . $this->caseId);
	}

	public function getCaseId() {
		return $this->caseId;
	}

	public function setCaseId($caseId) {
		$this->caseId = $caseId;
	}

	public function setPosition($pos) {
		$this->position = $pos;
	}

	public function getCaseClass() {
		if (is_null($this->case)) {
			$this->case = new ocase($this->caseId);
		}
		return $this->case;
	}

	public static function getAvailForAddCases() {
		$caseInst = new ocase();
		$cases = $caseInst->get_ocases('enable = 1 AND type = 0');
		$casesIds = db()->query('SELECT case_id FROM opencase_battle_cases');
		foreach ($cases as $caseKey => $case) {
			foreach ($casesIds as $caseIdData) {
				if ($case->get_id() == $caseIdData['case_id']) {
					unset($cases[$caseKey]);
				}
			}
		}
		return $cases;
	}

	public static function getAllBattleCases() {
		$casesIds = db()->query('SELECT case_id FROM opencase_battle_cases ORDER BY position ASC');
		$cases = [];
		foreach ($casesIds as $caseIdData) {
			$cases[] = new caseInBattle($caseIdData['case_id']);
		}
		return $cases;
	}

	public static function getMaxPosition() {
		$pos = db()->query_once('SELECT MAX(position) FROM opencase_battle_cases');
		return ((int) ($pos['MAX(position)'] ?? -1)) + 1;
	}

}
