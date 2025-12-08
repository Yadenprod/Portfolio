<?php

class bot {
	
	const DEFAULT_ENCRYPTED_TEXT = 'encrypted';

	var $id = '';
	var $steam_id = '';
	var $name = '';
	var $password = '';
	var $shared_secret = '';
	var $identity_secret = '';
	var $api_key = '';
	var $status = 0;
	var $enabled = '';
	var $offer_url = '';
	var $market_enable = 0;
	var $market_key = '';
	var $decrypted_market_key = '';
	var $status_array = array('Работает', 'Не работает', 'Подключается', 'Переподключается');
	var $status_label = array('label-success', 'label-danger', 'label-primary', 'label-warning');
	private $init_in_progress = false;

	function __construct($id = '') {
		if ($id != '') {
			$this->load_bot(db()->nomysqlinj($id));
		}
	}

	function get_id() {
		return $this->id;
	}

	function set_id($id) {
		$this->id = $id;
	}

	function get_steam_id() {
		return $this->steam_id;
	}

	function set_steam_id($steam_id) {
		$this->steam_id = $steam_id;
	}

	function get_name() {
		return $this->name;
	}

	function set_name($name) {
		$this->name = $name;
	}

	function get_password() {
		return $this->password;
	}

	function set_password($password) {
		if ($this->init_in_progress) {
			$this->password = $password;
		} elseif ($password != self::DEFAULT_ENCRYPTED_TEXT) {
			$this->password = encrypter::encrypt($password, encrypter::BOT_KEY_NAME);
		}
	}

	function get_shared_secret() {
		return $this->shared_secret;
	}

	function set_shared_secret($shared_secret) {
		if ($this->init_in_progress) {
			$this->shared_secret = $shared_secret;
		} elseif ($shared_secret != self::DEFAULT_ENCRYPTED_TEXT) {
			$this->shared_secret = encrypter::encrypt($shared_secret, encrypter::BOT_KEY_NAME);
		}
	}

	function get_identity_secret() {
		return $this->identity_secret;
	}

	function set_identity_secret($identity_secret) {
		if ($this->init_in_progress) {
			$this->identity_secret = $identity_secret;
		} elseif ($identity_secret != self::DEFAULT_ENCRYPTED_TEXT) {
			$this->identity_secret = encrypter::encrypt($identity_secret, encrypter::BOT_KEY_NAME);
		}
	}

	function get_api_key() {
		return $this->api_key;
	}

	function set_api_key($api_key) {
		if ($this->init_in_progress) {
			$this->api_key = $api_key;
		} elseif ($api_key != self::DEFAULT_ENCRYPTED_TEXT) {
			$this->api_key = encrypter::encrypt($api_key, encrypter::BOT_KEY_NAME);
		}
	}

	function get_market_key() {
		return $this->market_key;
	}
	
	function get_decrypted_market_key() {
		if (empty($this->market_key)) {
			return '';
		}
		if (empty($this->decrypted_market_key)) {
			$this->decrypted_market_key = encrypter::decrypt($this->market_key, encrypter::SITE_KEY_NAME);
		}
		return $this->decrypted_market_key;
	}

	function set_market_key($market_key) {
		if ($this->init_in_progress) {
			$this->market_key = $market_key;
			$this->decrypted_market_key = '';
		} elseif ($market_key != self::DEFAULT_ENCRYPTED_TEXT) {
			$this->market_key = encrypter::encrypt($market_key, encrypter::SITE_KEY_NAME);
			$this->decrypted_market_key = $market_key;
		}
	}

	function get_market_enable() {
		return $this->market_enable;
	}

	function set_market_enable($market_enable) {
		$this->market_enable = $market_enable;
	}
	
	function get_label_market_enable() {
		return $this->get_market_enable() ? '<span class = "label label-success">Включен</span>' : '<span class = "label label-danger">Отключен</span>';
	}

	function get_status() {
		return $this->status;
	}

	function get_text_status() {
		return $this->status_array[$this->status];
	}

	function get_label_status() {
		return '<span class = "label ' . $this->status_label[$this->status] . '">' . $this->status_array[$this->status] . '</span>';
	}

	function get_status_array() {
		return $this->status_array;
	}

	function set_status($status) {
		$this->status = $status;
	}

	function get_enabled() {
		return $this->enabled;
	}

	function get_text_enabled() {
		return $this->get_enabled() ? 'Включен' : 'Отключен';
	}

	function get_label_enabled() {
		return $this->get_enabled() ? '<span class = "label label-success">Включен</span>' : '<span class = "label label-danger">Отключен</span>';
	}

	function set_enabled($enabled) {
		$this->enabled = $enabled;
	}

	function get_offer_url() {
		return $this->offer_url;
	}

	function set_offer_url($offer_url) {
		$this->offer_url = $offer_url;
	}

	function get_bot_inventory() {
		$item = new invItems();
		$items = $item->get_invItemss('bot_id = "' . $this->get_id() . '"');
		return $items;
	}

	function get_steam_inventory($game_id = 730) {
		$data = file_get_contents_https('https://steamcommunity.com/profiles/' . $this->get_steam_id() . '/inventory/json/' . $game_id . '/2/');
		if ($data) {
			$data = json_decode($data);
			if (isset($data->success) && $data->success) {
				$items = (array) $data->rgInventory;
				$descriptions = (array) $data->rgDescriptions;
				$return_items = array();
				foreach ($items as $itm) {
					$description = $descriptions[$itm->classid . '_' . $itm->instanceid];
					$item = new invItems();
					$item->set_parametrs($itm->id, $itm->classid, $itm->instanceid, $itm->amount, $itm->pos, $description->appid, $description->icon_url, isset($description->icon_url_large) ? $description->icon_url_large : $description->icon_url, $description->icon_drag_url, $description->name, $description->market_hash_name, $description->market_name, $description->name_color, $description->background_color, $description->type, $description->tradable, $description->marketable, $description->commodity, $description->market_tradable_restriction, 2, 0, $this->get_id(), 0);
					$return_items[] = $item;
				}
				return $return_items;
			} else {
				return false;
			}
		} else {
			return false;
		}
	}

	function update_inventory_from_steam() {
		$botInventory = $this->get_steam_inventory(get_setval('opencase_gameid'));
		if ($botInventory && is_array($botInventory)) {
			$res = db()->query('SELECT id FROM opencase_invitems where bot_id = "' . $this->get_id() . '"');
			$ids = [];
			foreach ($res as $row) {
				$ids[$row['id']] = $row['id'];
			}
			$values = array();
			foreach ($botInventory as $invItem) {
				if (!isset($ids[$invItem->get_id()])) {
					array_push($values, $invItem->get_insert_value());
				} else {
					unset($ids[$invItem->get_id()]);
				}
			}
			if (!empty($values)) {
				$sql = 'INSERT INTO opencase_invitems(`id`, `classid`, `instanceid`, `amount`, `pos`, `appid`, `icon_url`, `icon_url_large`, `icon_drag_url`, `name`, `market_hash_name`, `market_name`, `name_color`, `background_color`, `type`, `tradable`, `marketable`, `commodity`, `market_tradable_restriction`, `contextid`, `price`, `bot_id`, `status`) VALUES';
				$sql .= implode(',', $values);
				db()->query_once($sql);
			}
			if (!empty($ids)) {
				$sql = 'DELETE FROM opencase_invitems WHERE id IN (' . implode(', ', $ids) . ')';
				db()->query_once($sql);
			}
			return true;
		} else {
			return false;
		}
	}

	function set_parametrs($id, $steam_id, $name, $password, $shared_secret, $identity_secret, $api_key, $status, $enabled, $offer_url, $market_enable, $market_key) {
		$this->set_id($id);
		$this->set_steam_id($steam_id);
		$this->set_name($name);
		$this->set_password($password);
		$this->set_shared_secret($shared_secret);
		$this->set_identity_secret($identity_secret);
		$this->set_api_key($api_key);
		$this->set_status($status);
		$this->set_enabled($enabled);
		$this->set_offer_url($offer_url);
		$this->set_market_enable($market_enable);
		$this->set_market_key($market_key);
	}

	function set_parametrs_from_request() {
		if (isset($_REQUEST['steam_id']))
			$this->set_steam_id($_REQUEST['steam_id']);
		if (isset($_REQUEST['name']))
			$this->set_name($_REQUEST['name']);
		if (isset($_REQUEST['password']))
			$this->set_password($_REQUEST['password']);
		if (isset($_REQUEST['shared_secret']))
			$this->set_shared_secret($_REQUEST['shared_secret']);
		if (isset($_REQUEST['identity_secret']))
			$this->set_identity_secret($_REQUEST['identity_secret']);
		if (isset($_REQUEST['api_key']))
			$this->set_api_key($_REQUEST['api_key']);
		if (isset($_REQUEST['status']))
			$this->set_status($_REQUEST['status']);
		if (isset($_REQUEST['enabled']))
			$this->set_enabled($_REQUEST['enabled']);
		if (isset($_REQUEST['offer_url']))
			$this->set_offer_url($_REQUEST['offer_url']);
		if (isset($_REQUEST['market_enable']))
			$this->set_market_enable($_REQUEST['market_enable']);
		if (isset($_REQUEST['market_key']))
			$this->set_market_key($_REQUEST['market_key']);
	}

	function clear_parametrs() {
		$this->set_id('');
		$this->set_steam_id('');
		$this->set_name('');
		$this->set_password('');
		$this->set_shared_secret('');
		$this->set_identity_secret('');
		$this->set_api_key('');
		$this->set_status(0);
		$this->set_enabled('');
		$this->set_offer_url('');
		$this->set_market_enable(0);
		$this->set_market_key('');
	}

	function load_bot($id) {
		$this->init_in_progress = true;
		$cache = ch()->get('bot' . $id);
		if (!$cache) {
			$bot = db()->query_once('select * from opencase_bot where id = "' . $id . '"');
			$this->set_parametrs($bot['id'], $bot['steam_id'], $bot['name'], $bot['password'], $bot['shared_secret'], $bot['identity_secret'], $bot['api_key'], $bot['status'], $bot['enabled'], $bot['offer_url'], $bot['market_enable'], $bot['market_key']);
			if ($this->get_id() != '')
				ch()->set('bot' . $id, $this);
		} else {
			$this->set_parametrs($cache->get_id(), $cache->get_steam_id(), $cache->get_name(), $cache->get_password(), $cache->get_shared_secret(), $cache->get_identity_secret(), $cache->get_api_key(), $cache->get_status(), $cache->get_enabled(), $cache->get_offer_url(), $cache->get_market_enable(), $cache->get_market_key());
			$this->decrypted_market_key = $cache->decrypted_market_key;
		}
		$this->init_in_progress = false;
	}

	function add_bot() {
		db()->query_once('insert into opencase_bot( `steam_id`, `name`, `password`, `shared_secret`, `identity_secret`, `api_key`, `status`, `enabled`, `offer_url`, `market_enable`, `market_key`) values ( "' . $this->get_steam_id() . '", "' . $this->get_name() . '", "' . $this->get_password() . '", "' . $this->get_shared_secret() . '", "' . $this->get_identity_secret() . '", "' . $this->get_api_key() . '", "' . $this->get_status() . '", "' . $this->get_enabled() . '", "' . $this->get_offer_url() . '", "' . $this->get_market_enable() . '", "' . $this->get_market_key() . '")');
	}

	function update_bot() {
		db()->query_once('update opencase_bot set `steam_id` = "' . $this->get_steam_id() . '", `name` = "' . $this->get_name() . '", `password` = "' . $this->get_password() . '", `shared_secret` = "' . $this->get_shared_secret() . '", `identity_secret` = "' . $this->get_identity_secret() . '", `api_key` = "' . $this->get_api_key() . '", `status` = "' . $this->get_status() . '", `enabled` = "' . $this->get_enabled() . '", `offer_url` = "' . $this->get_offer_url() . '", `market_enable` = "' . $this->get_market_enable() . '", `market_key` = "' . $this->get_market_key() . '" where id = "' . $this->get_id() . '"');
		if ($this->get_id() != '')
			ch()->set('bot' . $this->id, $this);
	}

	function delete_bot() {
		db()->query_once('delete from opencase_bot where id = "' . $this->get_id() . '"');
		ch()->delete('bot' . $this->id);
	}

	function get_bots($where = '', $order = '', $limit = '') {
		$sql = 'select id from opencase_bot';
		if ($where != '')
			$sql .= ' where ' . $where;
		if ($order != '')
			$sql .= ' order by ' . $order;
		if ($limit != '')
			$sql .= ' limit ' . $limit;
		$botsArray = db()->query($sql);
		$bots = array();
		if (is_array($botsArray)) {
			foreach ($botsArray as $botElement) {
				$bot = new bot($botElement['id']);
				array_push($bots, $bot);
			}
		}
		return $bots;
	}
	
	function get_encrypted_data_input_text($data) {
		if (empty($data)) {
			return '';
		}
		return self::DEFAULT_ENCRYPTED_TEXT;
	}

}

?>