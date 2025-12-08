<?php

class FAQElement {

	private $id = '';
	private $question = '';
	private $answer = '';
	private $enabled = 0;
	private $position = 0;

	public function __construct($id = '') {
		if ($id != '') {
			$this->load(db()->nomysqlinj($id));
		}
	}

	private function load($id) {
		$cache = ch()->get('faq' . $id);
		if (!$cache) {
			$data = db()->query_once('SELECT * FROM faq WHERE id = "' . $id . '"');
			if (!empty($data)) {
				$this->id = $data['id'];
				$this->setQuestion($data['question']);
				$this->setAnswer($data['answer']);
				$this->setEnabled($data['enabled']);
				$this->setPosition($data['position']);
				ch()->set('faq' . $data['id'], $this);
			}
		} else {
			$this->id = $cache->getId();
			$this->setQuestion($cache->getQuestion());
			$this->setAnswer($cache->getAnswer());
			$this->setEnabled($cache->getEnabled());
			$this->setPosition($cache->getPosition());
		}
	}

	public function getId() {
		return $this->id;
	}

	public function getQuestion() {
		return $this->question;
	}

	public function setQuestion($question) {
		$this->question = $question;
	}

	public function getAnswer() {
		return $this->answer;
	}

	public function setAnswer($answer) {
		$this->answer = $answer;
	}

	public function getEnabled() {
		return $this->enabled;
	}

	public function setEnabled($enabled) {
		$this->enabled = $enabled;
	}

	public function getPosition() {
		return $this->position;
	}

	public function setPosition($position) {
		$this->position = $position;
	}

	public function fromRequest() {
		if (isset($_REQUEST['question'])) {
			$this->setQuestion(db()->nomysqlinj($_REQUEST['question']));
		}
		if (isset($_REQUEST['answer'])) {
			$this->setAnswer(db()->nomysqlinj($_REQUEST['answer']));
		}
		if (isset($_REQUEST['enabled'])) {
			$this->setEnabled($_REQUEST['enabled']);
		}
	}

	public function save() {
		if (!empty($this->getId())) {
			db()->query_once('UPDATE faq set `question` = "' . db()->nomysqlinj($this->getQuestion()) . '", `answer` = "' . db()->nomysqlinj($this->getAnswer()) . '", `enabled` = "' . $this->getEnabled() . '", `position` = "' . $this->getPosition() . '" WHERE id = "' . $this->getId() . '"');
			ch()->set('faq' . $this->getId(), $this);
		} else {
			$this->setPosition(self::getMaxPosition() + 1);
			db()->query_once('INSERT INTO faq( `question`, `answer`, `enabled`, `position`) VALUES ( "' . db()->nomysqlinj($this->getQuestion()) . '", "' . db()->nomysqlinj($this->getAnswer()) . '", "' . $this->getEnabled() . '", "' . $this->getPosition() . '")');
		}
	}

	public function delete() {
		db()->query_once('DELETE FROM faq WHERE id = "' . $this->getId() . '"');
		ch()->delete('faq' . $this->getId());
	}

	private static function getMaxPosition() {
		$pos = db()->query_once('SELECT MAX(position) FROM `faq`');
		return (int) $pos['MAX(position)'];
	}

	public static function getTotalCount() {
		$faqcount = db()->query_once('SELECT count(id) FROM faq');
		return $faqcount['count(id)'];
	}

	public static function getQuestions($page, $limit) {
		return db()->query('SELECT * FROM faq ORDER BY position LIMIT ' . (($page - 1) * $limit) . ',' . $limit);
	}

	public static function getAllEnabledQuestions() {
		return db()->query('SELECT * FROM faq WHERE enabled = 1 ORDER BY position');
	}

}
