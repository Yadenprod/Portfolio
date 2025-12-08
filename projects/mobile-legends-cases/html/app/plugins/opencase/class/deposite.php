<?php
	class deposite {
		var $id = '';
		var $user_id = '';
		var $sum = '';
		var $num = '';
		var $from = '';
		var $status = '';
		var $time_add = '';
		
		var $user_class = false;
		
		var $from_array = array('Интеркасса', 'Unitpay', 'FreeKassa', 'QIWI');
		var $status_array = array('Новый', 'Ожидает оплаты', 'Обрабатывается', 'Успешно проведен', 'Отменен', 'Не проведен', 'Неизвестно');
		var $status_key_array = array('new', 'waitAccept', 'process', 'success', 'canceled', 'fail', 'unknow');
		var $status_label_array = array('warning', 'warning', 'warning', 'success', 'danger', 'danger', 'warning');

		function __construct($id = '') {
			if ($id != '') {
				$this->load_deposite(db()->nomysqlinj($id));
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
		}

		function get_sum() {
			return $this->sum;
		}

		function set_sum($sum) {
			$this->sum = $sum;
		}
		
		function get_num() {
			return $this->num;
		}

		function set_num($num) {
			$this->num = $num;
		}

		function get_from() {
			return $this->from;
		}
		
		function get_from_array() {
			return $this->from_array;
		}
		
		function get_from_text() {
			return $this->from_array[$this->get_from()];
		}

		function set_from($from) {
			$this->from = $from;
		}

		function get_status() {
			return $this->status;
		}
		
		function get_status_array() {
			return $this->status_array;
		}
		
		function get_status_text() {
			return $this->status_array[$this->get_status()];
		}
		
		function get_status_key_array() {
			return $this->status_key_array;
		}
		
		function get_status_key_text() {
			return $this->status_key_array[$this->get_status()];
		}
		
		function get_status_label_array() {
			return $this->status_label_array;
		}
		
		function get_status_label() {
			return '<span class = "label label-'.$this->status_label_array[$this->get_status()].'">'.$this->get_status_text().'</span>';
		}

		function set_status($status) {
			$this->status = $status;
		}

		function get_time_add() {
			return $this->time_add;
		}
		
		function get_format_time_add($format = 'd.m.Y H:i:s') {
			return getdatetime($this->get_time_add(), $format);
		}

		function set_time_add($time_add) {
			$this->time_add = $time_add;
		}

		function set_parametrs( $id, $user_id, $sum, $num, $from, $status, $time_add = '') { 
 			$this->set_id($id);
			$this->set_user_id($user_id);
			$this->set_sum($sum);
			$this->set_num($num);
			$this->set_from($from);
			$this->set_status($status);
			$this->set_time_add($time_add);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['sum'] != '')
				$this->set_sum($_REQUEST['sum']);
			if ($_REQUEST['num'] != '')
				$this->set_sum($_REQUEST['num']);
			if ($_REQUEST['from'] != '')
				$this->set_from($_REQUEST['from']);
			if ($_REQUEST['status'] != '')
				$this->set_status($_REQUEST['status']);
			if ($_REQUEST['time_add'] != '')
				$this->set_time_add($_REQUEST['time_add']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_user_id('');
			$this->set_sum('');
			$this->set_num('');
			$this->set_from('');
			$this->set_status('');
			$this->set_time_add('');
		}

		function  load_deposite($id) {
			$cache = ch()->get('deposite'.$id);
			if (!$cache) {
				$deposite = db()->query_once('select * from opencase_deposite where id = "'.$id.'"');
				$this->set_parametrs( $deposite['id'], $deposite['user_id'], $deposite['sum'], $deposite['num'], $deposite['from'], $deposite['status'], $deposite['time_add']);
				if ($this->get_id() != '')
					ch()->set('deposite'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_user_id(), $cache->get_sum(), $cache->get_num(), $cache->get_from(), $cache->get_status(), $cache->get_time_add());
			}
		}

		function add_deposite() {
			db()->query_once('insert into opencase_deposite( `user_id`, `sum`, `num`, `from`, `status`, `time_add`) values ( "'.$this->get_user_id().'", "'.$this->get_sum().'", "'.$this->get_num().'", "'.$this->get_from().'", "'.$this->get_status().'", NOW())');
		}

		function update_deposite() {
			db()->query_once('update opencase_deposite set `user_id` = "'.$this->get_user_id().'", `sum` = "'.$this->get_sum().'", `num` = "'.$this->get_num().'", `from` = "'.$this->get_from().'", `status` = "'.$this->get_status().'", `time_add` = "'.$this->get_time_add().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('deposite'.$this->id, $this);
		}

		function delete_deposite() {
			db()->query_once('delete from opencase_deposite where id = "'.$this->get_id().'"');
			ch()->delete('deposite'.$this->id);
		}

		function get_deposites($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_deposite';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$depositesArray = db()->query($sql);
			$deposites = array();
			if (is_array($depositesArray)) {
				foreach ($depositesArray as $depositeElement) {
					$deposite = new deposite($depositeElement['id']);
					array_push($deposites, $deposite);
				}
			}
			return $deposites;
		}
	}