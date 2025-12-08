<?php
	class balanceLog {
		var $id = '';
		var $user_id = '';
		var $change = '';
		var $comment = '';
		var $time = '';
		var $type = '';
		
		var $user_class = false;
		
		var $type_array = array('Депозит', 'Открытие кейса', 'Продажа', 'Реферал', 'Реферер', 'Промокод', 'Администратор', 'Регистрация');

		function __construct($id = '') {
			if ($id != '') {
				$this->load_balanceLog(db()->nomysqlinj($id));
			}
		}

		function get_id() {
			return $this->id;
		}

		function set_id($id) {
			$this->id = $id;
		}

		function get_user_id() {
			return $this->user_id;
		}
		
		function get_user_class() {
			if ($this->user_class) {
				return $this->user_class;
			} else {
				$user = new user($this->get_user_id());
				$this->user_class = $user;
				return $user;
			}
		}

		function set_user_id($user_id) {
			$this->user_id = $user_id;
			$this->user_class = false;
		}

		function get_change() {
			return $this->change;
		}

		function set_change($change) {
			$this->change = $change;
		}

		function get_comment() {
			return $this->comment;
		}

		function set_comment($comment) {
			$this->comment = $comment;
		}

		function get_time() {
			return $this->time;
		}
		
		function get_format_time($format = 'd.m.Y H:i:s') {
			return getdatetime($this->time, $format);
		}

		function set_time($time) {
			$this->time = $time;
		}

		function get_type() {
			return $this->type;
		}
		
		function get_text_type() {
			return $this->type_array[$this->type];
		}
		
		function get_type_array() {
			return $this->type_array;
		}

		function set_type($type) {
			$this->type = $type;
		}

		function set_parametrs( $id, $user_id, $change, $comment, $time, $type) { 
 			$this->set_id($id);
			$this->set_user_id($user_id);
			$this->set_change($change);
			$this->set_comment($comment);
			$this->set_time($time);
			$this->set_type($type);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['change'] != '')
				$this->set_change($_REQUEST['change']);
			if ($_REQUEST['comment'] != '')
				$this->set_comment($_REQUEST['comment']);
			if ($_REQUEST['time'] != '')
				$this->set_time($_REQUEST['time']);
			if ($_REQUEST['type'] != '')
				$this->set_type($_REQUEST['type']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_user_id('');
			$this->set_change('');
			$this->set_comment('');
			$this->set_time('');
			$this->set_type('');
		}

		function  load_balanceLog($id) {
			$cache = ch()->get('balanceLog'.$id);
			if (!$cache) {
				$balanceLog = db()->query_once('select * from opencase_balancelog where id = "'.$id.'"');
				$this->set_parametrs( $balanceLog['id'], $balanceLog['user_id'], $balanceLog['change'], $balanceLog['comment'], $balanceLog['time'], $balanceLog['type']);
				if ($this->get_id() != '')
					ch()->set('balanceLog'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_user_id(), $cache->get_change(), $cache->get_comment(), $cache->get_time(), $cache->get_type());
			}
		}

		function add_balanceLog() {
			db()->query_once('insert into opencase_balancelog( `user_id`, `change`, `comment`, `time`, `type`) values ( "'.$this->get_user_id().'", "'.$this->get_change().'", "'.$this->get_comment().'", NOW(), "'.$this->get_type().'")');
		}

		function update_balanceLog() {
			db()->query_once('update opencase_balancelog set `user_id` = "'.$this->get_user_id().'", `change` = "'.$this->get_change().'", `comment` = "'.$this->get_comment().'", `time` = "'.$this->get_time().'", `type` = "'.$this->get_type().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('balanceLog'.$this->id, $this);
		}

		function delete_balanceLog() {
			db()->query_once('delete from opencase_balancelog where id = "'.$this->get_id().'"');
			ch()->delete('balanceLog'.$this->id);
		}

		function get_balanceLogs($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_balancelog';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$balanceLogsArray = db()->query($sql);
			$balanceLogs = array();
			if (is_array($balanceLogsArray)) {
				foreach ($balanceLogsArray as $balanceLogElement) {
					$balanceLog = new balanceLog($balanceLogElement['id']);
					array_push($balanceLogs, $balanceLog);
				}
			}
			return $balanceLogs;
		}
	}
	
	function add_balance_log($user_id, $change, $comment, $type) {
		$balanceLog = new balanceLog();
		$balanceLog->set_parametrs('', $user_id, $change, $comment, '', $type);
		$balanceLog->add_balanceLog();
	}
?>