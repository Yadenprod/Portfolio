<?php
	class contract {
		var $id = '';
		var $user_id = '';
		var $items_id = '';
		var $item_id = '';
		var $items_price = '';
		var $time_open = '';
		var $image = '';
		
		var $user_class = false;
		var $item_class = false;

		function __construct($id = '') {
			if ($id != '') {
				$this->load_contract(db()->nomysqlinj($id));
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

		function get_items_id() {
			return $this->items_id;
		}
		
		function get_items_id_array() {
			return explode(';', $this->items_id);
		}
		
		function get_items_class() {
			$items = array();
			foreach ($this->get_items_id_array() as $id) {
				$items[] = new droppedItem($id);
			}
			return $items;
		}

		function set_items_id($items_id) {
			$this->items_id = $items_id;
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

		function get_items_price() {
			return $this->items_price;
		}

		function set_items_price($items_price) {
			$this->items_price = $items_price;
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
		
		function get_image() {
			return $this->image;
		}
		
		function set_image($image) {
			$this->image = $image;
		}
		
		function get_profit() {
			return $this->get_items_price() - $this->get_item_class()->get_price();
		}
		
		function set_parametrs( $id, $user_id, $items_id, $item_id, $items_price, $time_open, $image) { 
 			$this->set_id($id);
			$this->set_user_id($user_id);
			$this->set_items_id($items_id);
			$this->set_item_id($item_id);
			$this->set_items_price($items_price);
			$this->set_time_open($time_open);
			$this->set_image($image);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['items_id'] != '')
				$this->set_items_id($_REQUEST['items_id']);
			if ($_REQUEST['item_id'] != '')
				$this->set_item_id($_REQUEST['item_id']);
			if ($_REQUEST['items_price'] != '')
				$this->set_items_price($_REQUEST['items_price']);
			if ($_REQUEST['time_open'] != '')
				$this->set_time_open($_REQUEST['time_open']);
			if ($_REQUEST['image'] != '')
				$this->set_image($_REQUEST['image']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_user_id('');
			$this->set_items_id('');
			$this->set_item_id('');
			$this->set_items_price('');
			$this->set_time_open('');
			$this->set_image('');
		}

		function  load_contract($id) {
			$cache = ch()->get('contract'.$id);
			if (!$cache) {
				$contract = db()->query_once('select * from opencase_contracts where id = "'.$id.'"');
				$this->set_parametrs( $contract['id'], $contract['user_id'], $contract['items_id'], $contract['item_id'], $contract['items_price'], $contract['time_open'], $contract['image']);
				if ($this->get_id() != '')
					ch()->set('contract'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_user_id(), $cache->get_items_id(), $cache->get_item_id(), $cache->get_items_price(), $cache->get_time_open(), $cache->get_image());
			}
		}

		function add_contract() {
			db()->query_once('insert into opencase_contracts( `user_id`, `items_id`, `item_id`,`items_price`, `time_open`, `image`) values ( "'.$this->get_user_id().'", "'.$this->get_items_id().'", "'.$this->get_item_id().'", "'.$this->get_items_price().'", NOW(), "'.$this->get_image().'");');
		}

		function update_contract() {
			db()->query_once('update opencase_contracts set `user_id` = "'.$this->get_user_id().'", `items_id` = "'.$this->get_items_id().'", `item_id` = "'.$this->get_item_id().'", `items_price` = "'.$this->get_items_price().'", `time_open` = "'.$this->get_time_open().'", `image` = "'.$this->get_image().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('contract'.$this->id, $this);
		}

		function delete_contract() {
			db()->query_once('delete from opencase_contracts where id = "'.$this->get_id().'"');
			ch()->delete('contract'.$this->id);
		}

		function get_contracts($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_contracts';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$contractsArray = db()->query($sql);
			$contracts = array();
			if (is_array($contractsArray)) {
				foreach ($contractsArray as $contractElement) {
					$contract = new contract($contractElement['id']);
					array_push($contracts, $contract);
				}
			}
			return $contracts;
		}
	}
?>