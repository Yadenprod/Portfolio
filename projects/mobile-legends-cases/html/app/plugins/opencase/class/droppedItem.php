<?php
error_reporting(E_ERROR|E_WARNING);
	class droppedItem {
		var $id = '';
		var $user_id = '';
		var $item_id = '';
		var $quality = '';
		var $price = '';
		var $time_drop = '';
		var $status = '';
		var $from = '';
		var $fast = '';
		var $offer_id = '';
		var $bot_id = '';
		var $error = '';
		var $withdrawable = 1;
		var $usable = 1;
		var $analog_id = null;		
		
		var $user_class = false;
		var $item_class = false;
		var $bot_class = false;
		var $case_class = false;
		
		private static $itemDataSources = [];
		private static $status_array = array('Ожидает', 'Запрошен на вывод', 'Получен', 'Продан', 'Контракт', 'Ошибка', 'Повторная отправка');
		private static $status_label_array = array('warning', 'info', 'success', 'primary', 'default', 'danger', 'warning');
		var $quality_array = array('Прямо с завода', 'Немного поношенное', 'После полевых испытаний', 'Поношенное', 'Закаленное в боях');
		var $quality_array_en = array('Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred');

		function __construct($id = '') {
			if ($id != '') {
				$this->load_droppedItem(db()->nomysqlinj($id));
			}
		}
		
		public static function addItemStatus($id, $name, $label) {
			self::$status_array[$id] = $name;
			self::$status_label_array[$id] = $label;
		} 
		
		public static function addSourceInfoClass($id, $class) {
			self::$itemDataSources[$id] = $class;
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

		function get_item_id() {
			return $this->item_id;
		}
		
		function get_item_class() {
			if ($this->item_class) {
				return $this->item_class;
			} else {
				$item = new item($this->get_item_id());
				$this->item_class = $item;
				return $item;
			}
		}
		
		function get_item_name() {
			return str_replace('StatTrak™', '<span class = "stattrak-color">StatTrak™</span>', $this->get_item_class()->get_name().($this->quality < 5? ' ('.$this->get_text_quality_en().')' : ''));
		}
		
		function get_item_name_alt() {
			return $this->get_item_class()->get_name().($this->quality < 5? ' ('.$this->get_text_quality_en().')' : '');
		}

		function set_item_id($item_id) {
			$this->item_id = $item_id;
			$this->item_class = false;
		}

		function get_quality() {
			return $this->quality;
		}
		
		function get_text_quality() {
			return isset($this->quality_array[$this->get_quality()]) ? $this->quality_array[$this->get_quality()] : '';
		}
		
		function get_quality_array() {
			return $this->quality_array;
		}
		
		function get_text_quality_en() {
			return isset($this->quality_array_en[$this->get_quality()]) ? $this->quality_array_en[$this->get_quality()] : '';
		}
		
		function get_quality_array_en() {
			return $this->quality_array_en;
		}

		function set_quality($quality) {
			$this->quality = $quality;
		}

		function get_price() {
			return $this->price;
		}

		function set_price($price) {
			$this->price = $price;
		}

		function get_time_drop() {
			return $this->time_drop;
		}
		
		function get_format_time_drop($format = 'd.m.Y H:i:s') {
			return getdatetime($this->get_time_drop(), $format);
		}

		function set_time_drop($time_drop) {
			$this->time_drop = $time_drop;
		}
		
		function time_left() {
			return datef($this->get_time_drop()) - time() + get_setval('opencase_auto_sell_time') * 60;
		}

		function get_status() {
			return $this->status;
		}
		
		function get_text_status() {
			return self::$status_array[$this->get_status()];
		}
		
		function get_label_status() {
			return '<span class = "label label-'.self::$status_label_array[$this->get_status()].'">'.self::$status_array[$this->get_status()].'</span>';
		}
		
		function get_status_array() {
			return self::$status_array;
		}

		function set_status($status) {
			$this->status = $status;
			$this->error = '';
		}
		
		function get_withdrawable() {
			return $this->withdrawable;
		}
		
		function set_withdrawable($withdrawable) {
			$this->withdrawable = $withdrawable;
		}
		
		function get_usable() {
			return $this->usable;
		}
		
		function set_usable($usable) {
			$this->usable = $usable;
		}
		
		function get_analog_id() {
			return $this->analog_id;
		}
		
		function set_analog_id($analog_id) {
			$this->analog_id = $analog_id;
		}
		
		function get_from() {
			return $this->from;
		}
		
		function set_from($from) {
			$this->from = $from;
		}
		
		function get_fast() {
			return $this->fast;
		}
		
		function set_fast($fast) {
			$this->fast = $fast;
		}
		
		function get_case_class() {
			if ($this->case_class) {
				return $this->case_class;
			} else {
				if ($this->get_from()) {
					$case = new ocase($this->get_from());
					$this->case_class = $case;
					return $case;
				} else {
					return false;
				}
			}
		}
		
		function get_contract_class() {
			$contractID = db()->query_once('select id from opencase_contracts where item_id = '.$this->get_id());
			if ($this->get_from() == 0 && isset($contractID['id']) && $contractID['id'] != '') {
				return new contract($contractID['id']);
			} else {
				return new contract();
			}
		}
		
		function get_offer_id() {
			return $this->offer_id;
		}
		
		function set_offer_id($offer_id) {
			$this->offer_id = $offer_id;
		}
		
		function get_bot_id() {
			return $this->bot_id;
		}
		
		function get_bot_class() {
			if ($this->bot_class) {
				return $this->bot_class;
			} else {
				$bot = new bot($this->get_bot_id());
				$this->bot_class = $bot;
				return $bot;
			}
		}
		
		function set_bot_id($bot_id) {
			$this->bot_id = $bot_id;
			$this->bot_class = false;
		}
		
		function get_error() {
			return $this->error;
		}
		
		function set_error($error) {
			$this->error = $error;
		}

		function set_parametrs( $id, $user_id, $item_id, $quality, $price, $time_drop, $status, $from, $fast, $offer_id, $bot_id, $error = '', $withdrawable = 1, $usable = 1, $analog_id = null) { 
 			$this->set_id($id);
			$this->set_user_id($user_id);
			$this->set_item_id($item_id);
			$this->set_quality($quality);
			$this->set_price($price);
			$this->set_time_drop($time_drop);
			$this->set_status($status);
			$this->set_from($from);
			$this->set_fast($fast);
			$this->set_offer_id($offer_id);
			$this->set_bot_id($bot_id);
			$this->set_error($error);
			$this->set_withdrawable($withdrawable);
			$this->set_usable($usable);
			$this->set_analog_id($analog_id);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['item_id'] != '')
				$this->set_item_id($_REQUEST['item_id']);
			if ($_REQUEST['quality'] != '')
				$this->set_quality($_REQUEST['quality']);
			if ($_REQUEST['price'] != '')
				$this->set_price($_REQUEST['price']);
			if ($_REQUEST['time_drop'] != '')
				$this->set_time_drop($_REQUEST['time_drop']);
			if ($_REQUEST['status'] != '')
				$this->set_status($_REQUEST['status']);
			if ($_REQUEST['from'] != '')
				$this->set_from($_REQUEST['from']);
			if ($_REQUEST['fast'] != '')
				$this->set_fast($_REQUEST['fast']);
			if ($_REQUEST['offer_id'] != '')
				$this->set_offer_id($_REQUEST['offer_id']);
			if ($_REQUEST['bot_id'] != '')
				$this->set_bot_id($_REQUEST['bot_id']);
			if ($_REQUEST['error'] != '')
				$this->set_error($_REQUEST['error']);
			if (isset($_REQUEST['withdrawable']))
				$this->set_withdrawable($_REQUEST['withdrawable']);
			if (isset($_REQUEST['usable']))
				$this->set_usable($_REQUEST['usable']);
			if (isset($_REQUEST['analog_id']))
				$this->set_analog_id($_REQUEST['analog_id']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_user_id('');
			$this->set_item_id('');
			$this->set_quality('');
			$this->set_price('');
			$this->set_time_drop('');
			$this->set_status('');
			$this->set_from('');
			$this->set_fast('');
			$this->set_offer_id('');
			$this->set_bot_id('');
			$this->set_error('');
			$this->set_withdrawable(1);
			$this->set_usable(1);
			$this->set_analog_id(null);
		}

		function  load_droppedItem($id) {
			$cache = ch()->get('droppedItem'.$id);
			if (!$cache) {
				$droppedItem = db()->query_once('select * from opencase_droppeditems where id = "'.$id.'"');
				$this->set_parametrs( $droppedItem['id'], $droppedItem['user_id'], $droppedItem['item_id'], $droppedItem['quality'], $droppedItem['price'], $droppedItem['time_drop'], $droppedItem['status'], $droppedItem['from'], $droppedItem['fast'], $droppedItem['offer_id'], $droppedItem['bot_id'], $droppedItem['error'], $droppedItem['withdrawable'], $droppedItem['usable'],  $droppedItem['analog_id']);
				if ($this->get_id() != '')
					ch()->set('droppedItem'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_user_id(), $cache->get_item_id(), $cache->get_quality(), $cache->get_price(), $cache->get_time_drop(), $cache->get_status(), $cache->get_from(), $cache->get_fast(), $cache->get_offer_id(), $cache->get_bot_id(), $cache->get_error(), $cache->get_withdrawable(), $cache->get_usable(), $cache->get_analog_id());
			}
		}

		function add_droppedItem($time = 0) {
			$now = 'NOW()';
			if ($this->get_fast() == 0) {
				if ($this->get_from() == 0) {
					$time = 5;
				} elseif ($this->get_from() > 0) {
					$time = 16;
				}
			}
			if ($time != 0) {
				$now = 'DATE_ADD(NOW(), INTERVAL '.$time.' SECOND)';  
			}
			db()->query_once('insert into opencase_droppeditems( `user_id`, `item_id`, `quality`, `price`, `time_drop`, `status`, `from`, `fast`, `offer_id`, `bot_id`, `error`, `withdrawable`, `usable`, `analog_id`) values ( "'.$this->get_user_id().'", "'.$this->get_item_id().'", "'.$this->get_quality().'", "'.$this->get_price().'", '.$now.', "'.$this->get_status().'", "'.$this->get_from().'", "'.$this->get_fast().'", "'.$this->get_offer_id().'", "'.$this->get_bot_id().'", "'.$this->get_error().'", "'.$this->get_withdrawable().'", "'.$this->get_usable().'", '.(empty($this->get_analog_id()) ? 'NULL' : '"'.$this->get_analog_id().'"').')');
			$this->load_droppedItem(db()->get_last_id());
			return $time;
		}

		function update_droppedItem() {
			db()->query_once('update opencase_droppeditems set `user_id` = "'.$this->get_user_id().'", `item_id` = "'.$this->get_item_id().'", `quality` = "'.$this->get_quality().'", `price` = "'.$this->get_price().'", `time_drop` = "'.$this->get_time_drop().'", `status` = "'.$this->get_status().'", `from` = "'.$this->get_from().'", `fast` = "'.$this->get_fast().'", `offer_id` = "'.$this->get_offer_id().'", `bot_id` = "'.$this->get_bot_id().'", `error` = "'.$this->get_error().'", `withdrawable` = "'.$this->get_withdrawable().'", `usable` = "'.$this->get_usable().'", `analog_id` = '.(empty($this->get_analog_id()) ? 'NULL' : '"'.$this->get_analog_id().'"').' where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('droppedItem'.$this->id, $this);
		}

		function delete_droppedItem() {
			db()->query_once('delete from opencase_droppeditems where id = "'.$this->get_id().'"');
			ch()->delete('droppedItem'.$this->id);
		}

		function get_droppedItems($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_droppeditems';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$droppedItemsArray = db()->query($sql);
			$droppedItems = array();
			if (is_array($droppedItemsArray)) {
				foreach ($droppedItemsArray as $droppedItemElement) {
					$droppedItem = new droppedItem($droppedItemElement['id']);
					array_push($droppedItems, $droppedItem);
				}
			}
			return $droppedItems;
		}
		
		function get_newDroppedItems($lastUpdate, $order = 'ASC', $limit = '') {
			return $this->get_droppedItems(($lastUpdate? 'time_drop > '.value($lastUpdate).' and ' : '').'time_drop <= NOW()', 'time_drop '.$order, $limit);
		}
		
		function get_source_link() {
			if ($this->get_from() > 0) {
				return '/case/' . $this->get_case_class()->get_key() . '/';
			} elseif($this->get_from() == 0) {
				return '/contracts/';
			}  elseif (isset(self::$itemDataSources[$this->get_from()])) {
				$class = self::$itemDataSources[$this->get_from()];
				return $class::getLink($this);
			}
			return '';
		}
		
		function get_source_image() {
			if ($this->get_from() > 0) {
				return $this->get_case_class()->get_src_image();
			} elseif($this->get_from() == 0) {
				return $this->get_contract_class()->get_image();
			} elseif (isset(self::$itemDataSources[$this->get_from()])) {
				$class = self::$itemDataSources[$this->get_from()];
				return $class::getImage($this);
			}
			return '';
		}
		
		function get_source_image_alt() {
			if ($this->get_from() > 0) {
				return $this->get_case_class()->get_name();
			} elseif($this->get_from() == 0) {
				return 'Контракт';
			}elseif (isset(self::$itemDataSources[$this->get_from()])) {
				$class = self::$itemDataSources[$this->get_from()];
				return $class::getImageAlt($this);
			}
			return '';
		}
		
		function get_source_css_class() {
			if($this->get_from() == 0) {
				return 'contract';
			} elseif (isset(self::$itemDataSources[$this->get_from()])) {
				$class = self::$itemDataSources[$this->get_from()];
				return $class::getCssClass($this);
			}
			return '';
		}
		
	}
?>