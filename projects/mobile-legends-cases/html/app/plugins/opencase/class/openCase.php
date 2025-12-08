<?php
	class openCase {
		var $id = '';
		var $user_id = '';
		var $case_id = '';
		var $item_id = '';
		var $case_price = '';
		var $time_open = '';
		
		var $user_class = false;
		var $case_class = false;
		var $item_class = false;

		function __construct($id = '') {
			if ($id != '') {
				$this->load_openCase(db()->nomysqlinj($id));
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

		function get_case_id() {
			return $this->case_id;
		}
		
		function get_case_class() {
			if ($this->case_class) {
				return $this->case_class;
			} else {
				$case = new ocase($this->get_case_id());
				$this->case_class = $case;
				return $case;
			}
		}

		function set_case_id($case_id) {
			$this->case_id = $case_id;
			$this->case_class = false;
		}

		function get_item_id() {
			return $this->item_id;
		}
		
		function get_item_class() {
			if ($this->item_class) {
				return $this->item_class;
			} else {
				$item = new droppedItem($this->get_item_id());
				$this->item_class = $item;
				return $item;
			}
		}

		function set_item_id($item_id) {
			$this->item_id = $item_id;
			$this->item_class = false;
		}

		function get_case_price() {
			return $this->case_price;
		}

		function set_case_price($case_price) {
			$this->case_price = $case_price;
		}

		function get_time_open() {
			return $this->time_open;
		}
		
		function get_format_time_open($format = 'd.m.Y H:i:s') {
			return getdatetime($this->time_open, $format);
		}

		function set_time_open($time_open) {
			$this->time_open = $time_open;
		}
		
		function get_profit() {
			return number_format($this->get_case_price() - $this->get_item_class()->get_price(), 2);
		}

		function set_parametrs( $id, $user_id, $case_id, $item_id, $case_price, $time_open) { 
 			$this->set_id($id);
			$this->set_user_id($user_id);
			$this->set_case_id($case_id);
			$this->set_item_id($item_id);
			$this->set_case_price($case_price);
			$this->set_time_open($time_open);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['case_id'] != '')
				$this->set_case_id($_REQUEST['case_id']);
			if ($_REQUEST['item_id'] != '')
				$this->set_item_id($_REQUEST['item_id']);
			if ($_REQUEST['case_price'] != '')
				$this->set_case_price($_REQUEST['case_price']);
			if ($_REQUEST['time_open'] != '')
				$this->set_time_open($_REQUEST['time_open']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_user_id('');
			$this->set_case_id('');
			$this->set_item_id('');
			$this->set_case_price('');
			$this->set_time_open('');
		}

		function  load_openCase($id) {
			$cache = ch()->get('openCase'.$id);
			if (!$cache) {
				$openCase = db()->query_once('select * from opencase_opencases where id = "'.$id.'"');
				$this->set_parametrs( $openCase['id'], $openCase['user_id'], $openCase['case_id'], $openCase['item_id'], $openCase['case_price'], $openCase['time_open']);
				if ($this->get_id() != '')
					ch()->set('openCase'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_user_id(), $cache->get_case_id(), $cache->get_item_id(), $cache->get_case_price(), $cache->get_time_open());
			}
		}

		function add_openCase($bot = false, $randTime = 0) {
            $now = 'NOW()';
            if ($bot) {
                $now = 'DATE_ADD(NOW(), INTERVAL '.$randTime.' SECOND)'; 
            }
			db()->query_once('insert into opencase_opencases( `user_id`, `case_id`, `item_id`, `case_price`, `time_open`) values ( "'.$this->get_user_id().'", "'.$this->get_case_id().'", "'.$this->get_item_id().'", "'.$this->get_case_price().'", '.$now.')');
		}

		function update_openCase() {
			db()->query_once('update opencase_opencases set `user_id` = "'.$this->get_user_id().'", `case_id` = "'.$this->get_case_id().'", `item_id` = "'.$this->get_item_id().'", `case_price` = "'.$this->get_case_price().'", `time_open` = "'.$this->get_time_open().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('openCase'.$this->id, $this);
		}

		function delete_openCase() {
			db()->query_once('delete from opencase_opencases where id = "'.$this->get_id().'"');
			ch()->delete('openCase'.$this->id);
		}

		function get_openCases($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_opencases';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$openCasesArray = db()->query($sql);
			$openCases = array();
			if (is_array($openCasesArray)) {
				foreach ($openCasesArray as $openCaseElement) {
					$openCase = new openCase($openCaseElement['id']);
					array_push($openCases, $openCase);
				}
			}
			return $openCases;
		}
	}
?>