<?php
	class botEvent {
		var $id = '';
		var $bot_id = 0;
		var $event = 0;
		var $additional = '';
		var $items_id = '';
		var $status = 0;
		var $time_add = '';
		var $time_start = '';
		var $iteration = 0;
		
		var $event_array = array(1 => 'Отправить предметы', 50 => 'Купить на сайте market.csgo.com', 100 => 'Для администратора');
		var $status_array = array('В очереди', 'В обработке', 'Завершено', 'Ошибка');
		var $status_label = array('default', 'warning', 'success', 'danger');

		function __construct($id = '') {
			if ($id != '') {
				$this->load_botEvent(db()->nomysqlinj($id));
			}
		}

		function get_id() {
			return $this->id;
		}

		function set_id($id) {
			$this->id = $id;
		}
		
		function get_bot_id() {
			return $this->bot_id;
		}
		
		function get_bot_class() {
			return new bot ($this->bot_id);
		}
		
		function set_bot_id($bot_id) {
			$this->bot_id = $bot_id;
		}

		function get_event() {
			return $this->event;
		}
		
		function get_text_event() {
			return !empty($this->event_array[$this->event])? $this->event_array[$this->event] : 'Неизвестно';
		}
		
		function get_array_event() {
			return $this->event_array;
		}

		function set_event($event) {
			$this->event = $event;
		}

		function get_additional() {
			return $this->additional;
		}
		
		function get_parsed_additional() {
			return json_decode($this->additional);
		}

		function set_additional($additional) {
			$this->additional = $additional;
		}
		
		function get_items_id() {
			return $this->items_id;
		}
		
		function get_items_array() {
			return explode(';', $this->items_id);
		}

		function set_items_id($items_id) {
			$this->items_id = $items_id;
		}
		
		function get_status() {
			return $this->status;
		}
		
		function get_text_status() {
			return $this->status_array[$this->status];
		}
		
		function get_array_status() {
			return $this->status_array;
		}
		
		function get_label_status() {
			return '<span class = "label label-'.$this->status_label[$this->status].'">'.$this->status_array[$this->status].'</span>';
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

		function get_time_start() {
			return $this->time_start;
		}
		
		function get_format_time_start($format = 'd.m.Y H:i:s') {
			return getdatetime($this->get_time_start(), $format);
		}

		function set_time_start($time_start) {
			$this->time_start = $time_start;
		}
		
		function get_iteration() {
			return $this->iteration;
		}
		
		function set_iteration($iteration) {
			$this->iteration = $iteration;
		}

		function set_parametrs($id, $bot_id, $event, $additional, $items_id, $status, $time_add, $time_start, $iteration = 0) { 
 			$this->set_id($id);
			$this->set_bot_id($bot_id);
			$this->set_event($event);
			$this->set_additional($additional);
			$this->set_items_id($items_id);
			$this->set_status($status);
			$this->set_time_add($time_add);
			$this->set_time_start($time_start);
			$this->set_iteration($iteration);
		}

		function set_parametrs_from_request() {
			if (isset($_REQUEST['bot_id']))
				$this->set_bot_id($_REQUEST['bot_id']);
			if (isset($_REQUEST['event']))
				$this->set_event($_REQUEST['event']);
			if (isset($_REQUEST['additional']))
				$this->set_additional($_REQUEST['additional']);
			if (isset($_REQUEST['items_id']))
				$this->set_items_id($_REQUEST['items_id']);
			if (isset($_REQUEST['status']))
				$this->set_status($_REQUEST['status']);
			if (isset($_REQUEST['time_add']))
				$this->set_time_add($_REQUEST['time_add']);
			if (isset($_REQUEST['time_start']))
				$this->set_time_start($_REQUEST['time_start']);
			if (isset($_REQUEST['iteration']))
				$this->set_iteration($_REQUEST['iteration']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_bot_id(0);
			$this->set_event(0);
			$this->set_additional('');
			$this->set_items_id('');
			$this->set_status(0);
			$this->set_time_add('');
			$this->set_time_start('');
			$this->set_iteration(0);
		}

		function  load_botEvent($id) {
			$cache = ch()->get('botEvent'.$id);
			if (!$cache) {
				$botEvent = db()->query_once('select * from opencase_botevents where id = "'.$id.'"');
				$this->set_parametrs( $botEvent['id'], $botEvent['bot_id'], $botEvent['event'], $botEvent['additional'], $botEvent['items_id'], $botEvent['status'], $botEvent['time_add'], $botEvent['time_start'], $botEvent['iteration']);
				if ($this->get_id() != '')
					ch()->set('botEvent'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_bot_id(), $cache->get_event(), $cache->get_additional(), $cache->get_items_id(), $cache->get_status(), $cache->get_time_add(), $cache->get_time_start(), $cache->get_iteration());
			}
		}

		function add_botEvent() {
			db()->query_once('insert into opencase_botevents(`bot_id`, `event`, `additional`, `items_id`, `status`, `time_add`, `time_start`, `iteration`) values ("'.$this->get_bot_id().'", "'.$this->get_event().'", "'.str_replace('"', '\\"', $this->get_additional()).'", "'.$this->get_items_id().'", "'.$this->get_status().'", NOW(), NOW(), "' .$this->get_iteration().'")');
		}

		function update_botEvent() {
			db()->query_once('update opencase_botevents set `bot_id` = "'.$this->get_bot_id().'", `event` = "'.$this->get_event().'", `additional` = "'.str_replace('"', '\\"', $this->get_additional()).'", `items_id` = "'.$this->get_items_id().'", `status` = "'.$this->get_status().'", `time_add` = "'.$this->get_time_add().'", `time_start` = "'.$this->get_time_start().'", `iteration` = "' . $this->get_iteration(). '" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('botEvent'.$this->id, $this);
		}

		function delete_botEvent() {
			db()->query_once('delete from opencase_botevents where id = "'.$this->get_id().'"');
			ch()->delete('botEvent'.$this->id);
		}

		function get_botEvents($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_botevents';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$botEventsArray = db()->query($sql);
			$botEvents = array();
			if (is_array($botEventsArray)) {
				foreach ($botEventsArray as $botEventElement) {
					$botEvent = new botEvent($botEventElement['id']);
					array_push($botEvents, $botEvent);
				}
			}
			return $botEvents;
		}
	}
?>