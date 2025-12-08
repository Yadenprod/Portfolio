<?php
	class invItems {
		var $id = '';
		var $classid = '';
		var $instanceid = '';
		var $amount = '';
		var $pos = '';
		var $appid = '';
		var $icon_url = '';
		var $icon_url_large = '';
		var $icon_drag_url = '';
		var $name = '';
		var $market_hash_name = '';
		var $market_name = '';
		var $name_color = '';
		var $background_color = '';
		var $type = '';
		var $tradable = '';
		var $marketable = '';
		var $commodity = '';
		var $market_tradable_restriction = '';
		var $contextid = '';
		var $price = '';
		var $bot_id = '';
		var $status = '';
		var $created_at = 0;
		
		var $status_array = array('Свободен', 'Занят');

		function __construct($id = '') {
			if ($id != '') {
				$this->load_invItems(db()->nomysqlinj($id));
			}
		}

		function get_id() {
			return $this->id;
		}

		function set_id($id) {
			$this->id = $id;
		}

		function get_classid() {
			return $this->classid;
		}

		function set_classid($classid) {
			$this->classid = $classid;
		}

		function get_instanceid() {
			return $this->instanceid;
		}

		function set_instanceid($instanceid) {
			$this->instanceid = $instanceid;
		}

		function get_amount() {
			return $this->amount;
		}

		function set_amount($amount) {
			$this->amount = $amount;
		}

		function get_pos() {
			return $this->pos;
		}

		function set_pos($pos) {
			$this->pos = $pos;
		}

		function get_appid() {
			return $this->appid;
		}

		function set_appid($appid) {
			$this->appid = $appid;
		}

		function get_icon_url() {
			return $this->icon_url;
		}
		
		function get_src_icon_url($width = false, $height = false) {
			return 'https://steamcommunity-a.akamaihd.net/economy/image/'.$this->get_icon_url().($width && $height? '/'.$width.'x'.$height : '');
		}

		function set_icon_url($icon_url) {
			$this->icon_url = $icon_url;
		}

		function get_icon_url_large() {
			return $this->icon_url_large;
		}
		
		function get_src_icon_url_large($width = false, $height = false) {
			return 'https://steamcommunity-a.akamaihd.net/economy/image/'.$this->get_icon_url_large().($width && $height? '/'.$width.'x'.$height : '');
		}

		function set_icon_url_large($icon_url_large) {
			$this->icon_url_large = $icon_url_large;
		}

		function get_icon_drag_url() {
			return $this->icon_drag_url;
		}
		
		function get_src_icon_drag_url($width = false, $height = false) {
			return 'https://steamcommunity-a.akamaihd.net/economy/image/'.$this->get_icon_drag_url().($width && $height? '/'.$width.'x'.$height : '');
		}

		function set_icon_drag_url($icon_drag_url) {
			$this->icon_drag_url = $icon_drag_url;
		}

		function get_name() {
			return $this->name;
		}

		function set_name($name) {
			$this->name = $name;
		}

		function get_market_hash_name() {
			return $this->market_hash_name;
		}

		function set_market_hash_name($market_hash_name) {
			$this->market_hash_name = $market_hash_name;
		}

		function get_market_name() {
			return $this->market_name;
		}

		function set_market_name($market_name) {
			$this->market_name = $market_name;
		}

		function get_name_color() {
			return $this->name_color;
		}

		function set_name_color($name_color) {
			$this->name_color = $name_color;
		}

		function get_background_color() {
			return $this->background_color;
		}

		function set_background_color($background_color) {
			$this->background_color = $background_color;
		}

		function get_type() {
			return $this->type;
		}

		function set_type($type) {
			$this->type = $type;
		}

		function get_tradable() {
			return $this->tradable;
		}

		function set_tradable($tradable) {
			$this->tradable = $tradable;
		}

		function get_marketable() {
			return $this->marketable;
		}

		function set_marketable($marketable) {
			$this->marketable = $marketable;
		}

		function get_commodity() {
			return $this->commodity;
		}

		function set_commodity($commodity) {
			$this->commodity = $commodity;
		}

		function get_market_tradable_restriction() {
			return $this->market_tradable_restriction;
		}

		function set_market_tradable_restriction($market_tradable_restriction) {
			$this->market_tradable_restriction = $market_tradable_restriction;
		}

		function get_contextid() {
			return $this->contextid;
		}

		function set_contextid($contextid) {
			$this->contextid = $contextid;
		}
		
		function get_price() {
			return $this->price;
		}
		
		function get_created_at() {
			return $this->created_at;
		}
		
		function set_created_at($created_at) {
			$this->created_at = $created_at;
		}
		
		function get_rate_price($rate = 55, $decimals = 2) {
			return number_format($this->price * $rate, $decimals);
		}

		function set_price($price) {
			$this->price = $price;
		}
		
		function get_bot_id() {
			return $this->bot_id;
		}
		
		function get_bot_class() {
			$bot = new bot($this->bot_id);
			return $bot;
		}

		function set_bot_id($bot_id) {
			$this->bot_id = $bot_id;
		}
		
		function get_status() {
			return $this->status;
		}
		
		function get_text_status() {
			return $this->status_array[$this->status];
		}
		
		function get_status_array() {
			return $this->status_array;
		}

		function set_status($status) {
			$this->status = $status;
		}
		
		function get_insert_value() {
			return '("'.$this->get_id().'", "'.$this->get_classid().'", "'.$this->get_instanceid().'", "'.$this->get_amount().'", "'.$this->get_pos().'", "'.$this->get_appid().'", "'.$this->get_icon_url().'", "'.$this->get_icon_url_large().'", "'.$this->get_icon_drag_url().'", "'.$this->get_name().'", "'.$this->get_market_hash_name().'", "'.$this->get_market_name().'", "'.$this->get_name_color().'", "'.$this->get_background_color().'", "'.$this->get_type().'", "'.$this->get_tradable().'", "'.$this->get_marketable().'", "'.$this->get_commodity().'", "'.$this->get_market_tradable_restriction().'", "'.$this->get_contextid().'", "'.$this->get_price().'", "'.$this->get_bot_id().'", "'.$this->get_status().'")';
		}
		
		function get_html_item() {
			$content = '
							<div class = "col-lg-1 col-md-2 col-xs-3 invItem status-'.$this->get_status().'">
								<i class = "fa fa-check-square-o"></i>
								<img src = "'.$this->get_src_icon_url('100f', '100f').'" alt = "'.$this->get_market_hash_name().'" title = "'.$this->get_market_hash_name().'" class = "img-responsive">
								<input type = "checkbox" name = "items[]" value = "'.$this->get_id().'" class = "invItemCkeck">
							</div>
			';
			return $content;
		}

		function set_parametrs( $id, $classid, $instanceid, $amount, $pos, $appid, $icon_url, $icon_url_large, $icon_drag_url, $name, $market_hash_name, $market_name, $name_color, $background_color, $type, $tradable, $marketable, $commodity, $market_tradable_restriction, $contextid, $price = 0, $bot_id = 0, $status = 0, $created_at = 0) { 
 			$this->set_id($id);
			$this->set_classid($classid);
			$this->set_instanceid($instanceid);
			$this->set_amount($amount);
			$this->set_pos($pos);
			$this->set_appid($appid);
			$this->set_icon_url($icon_url);
			$this->set_icon_url_large($icon_url_large);
			$this->set_icon_drag_url($icon_drag_url);
			$this->set_name($name);
			$this->set_market_hash_name($market_hash_name);
			$this->set_market_name($market_name);
			$this->set_name_color($name_color);
			$this->set_background_color($background_color);
			$this->set_type($type);
			$this->set_tradable($tradable);
			$this->set_marketable($marketable);
			$this->set_commodity($commodity);
			$this->set_market_tradable_restriction($market_tradable_restriction);
			$this->set_contextid($contextid);
			$this->set_price($price);
			$this->set_bot_id($bot_id);
			$this->set_status($status);
			$this->set_created_at($created_at);
		}
		
		function set_parametrs_from_json($json, $price = 0, $bot_id = 0, $status = 0) {
			$json = json_decode($json);
			$this->set_parametrs( $json->id, $json->classid, $json->instanceid, $json->amount, $json->pos, $json->appid, $json->icon_url, $json->icon_url_large, $json->icon_drag_url, $json->name, $json->market_hash_name, $json->market_name, $json->name_color, $json->background_color, $json->type, $json->tradable, $json->marketable, $json->commodity, $json->market_tradable_restriction, $json->contextid, $price, $bot_id, $status);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['classid'] != '')
				$this->set_classid($_REQUEST['classid']);
			if ($_REQUEST['instanceid'] != '')
				$this->set_instanceid($_REQUEST['instanceid']);
			if ($_REQUEST['amount'] != '')
				$this->set_amount($_REQUEST['amount']);
			if ($_REQUEST['pos'] != '')
				$this->set_pos($_REQUEST['pos']);
			if ($_REQUEST['appid'] != '')
				$this->set_appid($_REQUEST['appid']);
			if ($_REQUEST['icon_url'] != '')
				$this->set_icon_url($_REQUEST['icon_url']);
			if ($_REQUEST['icon_url_large'] != '')
				$this->set_icon_url_large($_REQUEST['icon_url_large']);
			if ($_REQUEST['icon_drag_url'] != '')
				$this->set_icon_drag_url($_REQUEST['icon_drag_url']);
			if ($_REQUEST['name'] != '')
				$this->set_name($_REQUEST['name']);
			if ($_REQUEST['market_hash_name'] != '')
				$this->set_market_hash_name($_REQUEST['market_hash_name']);
			if ($_REQUEST['market_name'] != '')
				$this->set_market_name($_REQUEST['market_name']);
			if ($_REQUEST['name_color'] != '')
				$this->set_name_color($_REQUEST['name_color']);
			if ($_REQUEST['background_color'] != '')
				$this->set_background_color($_REQUEST['background_color']);
			if ($_REQUEST['type'] != '')
				$this->set_type($_REQUEST['type']);
			if ($_REQUEST['tradable'] != '')
				$this->set_tradable($_REQUEST['tradable']);
			if ($_REQUEST['marketable'] != '')
				$this->set_marketable($_REQUEST['marketable']);
			if ($_REQUEST['commodity'] != '')
				$this->set_commodity($_REQUEST['commodity']);
			if ($_REQUEST['market_tradable_restriction'] != '')
				$this->set_market_tradable_restriction($_REQUEST['market_tradable_restriction']);
			if ($_REQUEST['contextid'] != '')
				$this->set_contextid($_REQUEST['contextid']);
			if ($_REQUEST['price'] != '')
				$this->set_price($_REQUEST['price']);
			if ($_REQUEST['bot_id'] != '')
				$this->set_bot_id($_REQUEST['bot_id']);
			if ($_REQUEST['status'] != '')
				$this->set_status($_REQUEST['status']);
			if ($_REQUEST['created_at'] != '')
				$this->set_created_at($_REQUEST['created_at']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_classid('');
			$this->set_instanceid('');
			$this->set_amount('');
			$this->set_pos('');
			$this->set_appid('');
			$this->set_icon_url('');
			$this->set_icon_url_large('');
			$this->set_icon_drag_url('');
			$this->set_name('');
			$this->set_market_hash_name('');
			$this->set_market_name('');
			$this->set_name_color('');
			$this->set_background_color('');
			$this->set_type('');
			$this->set_tradable('');
			$this->set_marketable('');
			$this->set_commodity('');
			$this->set_market_tradable_restriction('');
			$this->set_contextid('');
			$this->set_price('');
			$this->set_bot_id('');
			$this->set_status('');
			$this->set_created_at(0);
		}

		function  load_invItems($id) {
			$cache = ch()->get('invItems'.$id);
			if (!$cache) {
				$invItems = db()->query_once('select * from opencase_invitems where id = "'.$id.'"');
				$this->set_parametrs( $invItems['id'], $invItems['classid'], $invItems['instanceid'], $invItems['amount'], $invItems['pos'], $invItems['appid'], $invItems['icon_url'], $invItems['icon_url_large'], $invItems['icon_drag_url'], $invItems['name'], $invItems['market_hash_name'], $invItems['market_name'], $invItems['name_color'], $invItems['background_color'], $invItems['type'], $invItems['tradable'], $invItems['marketable'], $invItems['commodity'], $invItems['market_tradable_restriction'], $invItems['contextid'], $invItems['price'], $invItems['bot_id'], $invItems['status'], $invItems['created_at']);
				if ($this->get_id() != '')
					ch()->set('invItems'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_classid(), $cache->get_instanceid(), $cache->get_amount(), $cache->get_pos(), $cache->get_appid(), $cache->get_icon_url(), $cache->get_icon_url_large(), $cache->get_icon_drag_url(), $cache->get_name(), $cache->get_market_hash_name(), $cache->get_market_name(), $cache->get_name_color(), $cache->get_background_color(), $cache->get_type(), $cache->get_tradable(), $cache->get_marketable(), $cache->get_commodity(), $cache->get_market_tradable_restriction(), $cache->get_contextid(), $cache->get_price(), $cache->get_bot_id(), $cache->get_status(), $cache->get_created_at());
			}
		}

		function add_invItems() {
			db()->query_once('insert into opencase_invitems(`id`, `classid`, `instanceid`, `amount`, `pos`, `appid`, `icon_url`, `icon_url_large`, `icon_drag_url`, `name`, `market_hash_name`, `market_name`, `name_color`, `background_color`, `type`, `tradable`, `marketable`, `commodity`, `market_tradable_restriction`, `contextid`, `price`, `bot_id`, `status`) values ("'.$this->get_id().'", "'.$this->get_classid().'", "'.$this->get_instanceid().'", "'.$this->get_amount().'", "'.$this->get_pos().'", "'.$this->get_appid().'", "'.$this->get_icon_url().'", "'.$this->get_icon_url_large().'", "'.$this->get_icon_drag_url().'", "'.$this->get_name().'", "'.$this->get_market_hash_name().'", "'.$this->get_market_name().'", "'.$this->get_name_color().'", "'.$this->get_background_color().'", "'.$this->get_type().'", "'.$this->get_tradable().'", "'.$this->get_marketable().'", "'.$this->get_commodity().'", "'.$this->get_market_tradable_restriction().'", "'.$this->get_contextid().'", "'.$this->get_price().'", "'.$this->get_bot_id().'", "'.$this->get_status().'")');
		}

		function update_invItems() {
			db()->query_once('update opencase_invitems set `classid` = "'.$this->get_classid().'", `instanceid` = "'.$this->get_instanceid().'", `amount` = "'.$this->get_amount().'", `pos` = "'.$this->get_pos().'", `appid` = "'.$this->get_appid().'", `icon_url` = "'.$this->get_icon_url().'", `icon_url_large` = "'.$this->get_icon_url_large().'", `icon_drag_url` = "'.$this->get_icon_drag_url().'", `name` = "'.$this->get_name().'", `market_hash_name` = "'.$this->get_market_hash_name().'", `market_name` = "'.$this->get_market_name().'", `name_color` = "'.$this->get_name_color().'", `background_color` = "'.$this->get_background_color().'", `type` = "'.$this->get_type().'", `tradable` = "'.$this->get_tradable().'", `marketable` = "'.$this->get_marketable().'", `commodity` = "'.$this->get_commodity().'", `market_tradable_restriction` = "'.$this->get_market_tradable_restriction().'", `contextid` = "'.$this->get_contextid().'", `price` = "'.$this->get_price().'", `bot_id` = "'.$this->get_bot_id().'", `status` = "'.$this->get_status().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('invItems'.$this->id, $this);
		}

		function delete_invItems() {
			db()->query_once('delete from opencase_invitems where id = "'.$this->get_id().'"');
			ch()->delete('invItems'.$this->id);
		}

		function get_invItemss($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_invitems';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$invItemssArray = db()->query($sql);
			$invItemss = array();
			if (is_array($invItemssArray)) {
				foreach ($invItemssArray as $invItemsElement) {
					$invItems = new invItems($invItemsElement['id']);
					array_push($invItemss, $invItems);
				}
			}
			return $invItemss;
		}
	}
?>