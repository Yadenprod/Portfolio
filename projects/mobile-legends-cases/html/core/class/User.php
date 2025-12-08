<?php
	class user {
		private $id = 0;
		private $name = '';
		private $email = '';
		private $password = '';
		private $banned = false;
		private $time_reg = '';
		private $login = false;
		private $user_data = array();

		function __construct($id = false) {
			if ($id) {
				$this->load((int)$id);
			}
		}

		function get_id() {
			return (int)$this->id;
		}

		function set_id($id) {
			$this->id = (int)$id;
		}

		function get_name() {
			return $this->name;
		}

		function set_name($name) {
			$this->name = substr(strip_tags(trim($name)), 0, 64);
		}

		function get_email() {
			return $this->email;
		}

		function set_email($email) {
			$this->email = substr(strip_tags(trim($email)), 0, 128);
		}

		function get_password() {
			return $this->password;
		}

		static function hash_password($password) {
			return md5(sha1(sha1(md5(md5(sha1(md5('USER'.':'.CMSSECRET.':'.$password)))))));
		}

		function set_password($password) {
			$this->password = strip_tags(trim($password));
		}

		function set_nohash_password($password) {
			$this->password = $this->hash_password($password);
		}

		function get_banned() {
			return $this->banned? true : false;
		}

		function set_banned($banned) {
			$this->banned = $banned? true : false;
		}

		function ban() {
			$this->set_ban(true);
			upd('users', array('banned' => true), array('id' => $this->get_id()), false, 1);
		}

		function get_time_reg() {
			return $this->time_reg;
		}

		function get_formated_time_reg($format = 'd.m.Y H:i:s') {
			return date($format, date_sql_to_timestamp($this->get_time_reg()));
		}

		function set_time_reg($time_reg) {
			$this->time_reg = $time_reg;
		}

		function login($email, $password) {
            $user = user::get_user(array('email' => $email, 'password' => $this->hash_password($password), 'banned' => 0));
            if ($user) {
                $this->load($user->get_id());
                $this->login = true;
				$this->set_auth_cookie();
                return true;
            } else {
                return false;
            }
		}
		
		function set_auth_cookie() {
			set_cookie('token', md5('USER'.$this->get_id().':'.$this->get_email().':'.$this->get_password().':'.iptoken('USER')));
		}
		
		function clear_auth_cookie() {
			clear_cookie('token');
		}

		function auth() {
			if (!get_cookie('token')) return false;
			$user = user::get_user('MD5(CONCAT("USER", `id`, ":", `email`, ":", `password`, ":", '.value(iptoken('USER')).')) = '.value(get_cookie('token')));
			if (!$user) return false;
			if ($user->get_banned()) {
				$user->clear_auth_cookie();
				return false;
			}
			$this->load($user->get_id());
			$this->set_login(true);
			return true;
		}

		function is_login() {
			return $this->login;
		}

		function set_login($value) {
			$this->login = $value? true : false;
		}

		function load_user_data() {
			$fields = user_field::get_user_fields();  
			foreach ($fields as $field) {
				$this->user_data[$field->get_key()] = user_data::get_user_data(array('user_field_id' => $field->get_id(), 'user_id' => $this->get_id()));
				if ($this->user_data[$field->get_key()]) {
					$this->user_data[$field->get_key()]->set_user_field($field);
				} else {
					$this->user_data[$field->get_key()] = new user_data();
					$this->user_data[$field->get_key()]->set_user_id($this->get_id());
					$this->user_data[$field->get_key()]->set_user_field_id($field->get_id());
					$this->user_data[$field->get_key()]->set_value($field->get_default());
					$this->user_data[$field->get_key()]->add();
				}
			}
		}

		function update_user_data() {
			foreach ($this->user_data as $data) {
				$data->update();
			}
			if ($this->get_id() != '') {
				ch()->set('user'.$this->get_id(), $this);
			}
		}

		function delete_user_data() {
			del('users_data', array('user_id' => $this->get_id()));
			ch()->delete('user'.$this->get_id());
		}

		function get_data($key) {
			return isset($this->user_data[$key])? $this->user_data[$key]->get_value() : false;
		}

		function set_data($key, $value) {
			if (isset($this->user_data[$key]))
				$this->user_data[$key]->set_value($value);
		}

		function upd_data($key, $value) {
			if (isset($this->user_data[$key])) {
				$this->set_data($key, $value);
				$this->user_data[$key]->update();
			}
			if ($this->get_id() != '') {
				ch()->set('user'.$this->get_id(), $this);
			}
		}

		function log($event, $type = 0, $data = array()) {
			$log = new user_log();
			$log->set_user_id($this->get_id());
			$log->set_ip(getip());
			$log->set_event($event);
			$log->set_type($type);
			$log->set_data($data);
			$log->add();
		}

		function get_logs($where = false) {
			if (is_array($where)) 
				$where['user_id'] = $this->get_id();
			else if (is_string($where))
				$where = '('.$where.') and `user_id` = '.$this->get_id();
			else
				$where = array('user_id' => $this->get_id());
			return user_log::get_user_logs($where);
		}

		function set_from_array($user) {
			if (isset($user['id']))
				$this->set_id($user['id']);
			if (isset($user['name']))
				$this->set_name($user['name']);
			if (isset($user['email']))
				$this->set_email($user['email']);
			if (isset($user['password']))
				$this->set_password($user['password']);
			if (isset($user['banned']))
				$this->set_banned($user['banned']);
			if (isset($user['time_reg']))
				$this->set_time_reg($user['time_reg']);
		}

		function load($id) {
			$cache = ch()->get('user'.$id);			
			if (!$cache) {
				$user =  selo('users', array('id' => $id));
				if (!empty($user['id'])) {
					$this->set_from_array($user);
					$this->load_user_data();
				}
				if ($this->get_id() != '') {
					ch()->set('user'.$id, $this);
				}
			} else {
				$this->set_from_array([
					'id' => $cache->get_id(),
					'name' => $cache->get_name(),
					'email' => $cache->get_email(),
					'password' => $cache->get_password(),
					'banned' => $cache->get_banned(),
					'time_reg' => $cache->get_time_reg(),
				]);
				$this->user_data = $cache->user_data;
			}
		}

		function add() {
			ins('users', array(
				'name' => $this->get_name(),
				'email' => $this->get_email(),
				'password' => $this->get_password(),
				'banned' => $this->get_banned()
			));
			$this->load(lastID());
		}

		function update() {
			upd('users', array(
				'name' => $this->get_name(),
				'email' => $this->get_email(),
				'password' => $this->get_password(),
				'banned' => $this->get_banned()
			), array('id' => $this->get_id()));
			$this->update_user_data();
			if ($this->get_id() != '') {
				ch()->set('user'.$this->get_id(), $this);
			}
		}

		function delete() {
			del('users', array('id' => $this->get_id()));
			$this->delete_user_data();
			ch()->delete('user'.$this->get_id());
		}

		static function get_user($where ='', $order = '') {
			$userElement = selo('users', $where, $order);
			if (!$userElement['id']) 
				return false;
			$user = new user();
			$user->set_from_array($userElement);
			$user->load_user_data();
			return $user;
		}

		static function get_users($where ='', $order = '', $limit = '') {
			$usersArray = sel('users', $where, $order, $limit);
			$users = array();
			if (is_array($usersArray)) {
				foreach ($usersArray as $userElement) {
					$user = new user();
					$user->set_from_array($userElement);
					$user->load_user_data();
					array_push($users, $user);
				}
			}
			return $users;
		}
	}

	class user_field {
		private $id = 0;
		private $key = '';
		private $type = '';
		private $default = '';
		private $description = '';

		function __construct($id = false) {
			if ($id) 
				$this->load((int)$id);
		}

		function get_id() {
			return (int)$this->id;
		}

		function set_id($id) {
			$this->id = (int)$id;
		}

		function get_key() {
			return $this->key;
		}

		function set_key($key) {
			$this->key = strip_tags(trim($key));
		}

		function get_type() {
			return $this->type;
		}

		function set_type($type) {
			$this->type = strip_tags(trim($type));
		}

		function get_default() {
			$type = $this->get_type();
			switch ($type) {
				case 'int':
				case 'integer':
					$value = (int)$this->default;
					break;
				case 'float':
				case 'double':
					$value = (float)$this->default;
					break;
				case 'bool':
				case 'boolean':
					$value = $this->default? true : false;
					break;
				case 'array':
					$value = json_decode($this->default, true);
					break;
				case 'text':
					$value = trim($this->default);
					break;
				case 'string':
					$value = trim(strip_tags($this->default));
					break;
				default:
					$value = $this->default;
			}
			return $value;
		}

		function set_default($default) {
			$type = $this->get_type();
			switch ($type) {
				case 'int':
				case 'integer':
					$value = (int)$default;
					break;
				case 'float':
				case 'double':
					$value = (float)$default;
					break;
				case 'bool':
				case 'boolean':
					$value = $default? 1 : 0;
					break;
				case 'array':
					$value = json_encode($default);
					break;
				case 'text':
					$value = trim($default);
					break;
				case 'string':
					$value = trim(strip_tags($default));
					break;
				default:
					$value = $default;
			}
			$this->default = $value;
		}

		function get_description() {
			return $this->description;
		}

		function set_description($description) {
			$this->description = strip_tags(trim($description));
		}

		function set_from_array($user_field) {
			if (isset($user_field['id']))
				$this->set_id($user_field['id']);
			if (isset($user_field['key']))
				$this->set_key($user_field['key']);
			if (isset($user_field['type']))
				$this->set_type($user_field['type']);
			if (isset($user_field['default']))
				$this->set_default($user_field['default']);
			if (isset($user_field['description']))
				$this->set_description($user_field['description']);
		}

		function load($id) {
			$user_field =  selo('user_fields', array('id' => $id));
			$this->set_from_array($user_field);
		}

		function add_user_field() {
			ins('user_fields', array(
				'key' => $this->get_key(),
				'type' => $this->get_type(),
				'default' => $this->get_default(),
				'description' => $this->get_description()
			));
			$this->load(lastID());
		}

		function update_user_field() {
			upd('user_fields', array(
				'key' => $this->get_key(),
				'type' => $this->get_type(),
				'default' => $this->get_default(),
				'description' => $this->get_description()
			), array('id' => $this->get_id()));
			$this->load($this->get_id());
		}

		function delete_user_field() {
			del('user_fields', array('id' => $this->get_id()));
			del('users_data', array('user_field_id' => $this->get_id()));
		}

		static function get_user_field($where ='', $order = '') {
			$user_fieldElement = selo('user_fields', $where, $order, 1);
			if (!$user_fieldElement['id']) 
				return false;
			$user_field = new user_field();
			$user_field->set_from_array($user_fieldElement);
			return $user_field;
		}

		static function get_user_fields($where ='', $order = '', $limit = '') {
			$user_fieldsArray = sel('user_fields', $where, $order, $limit);
			$user_fields = array();
			if (is_array($user_fieldsArray)) {
				foreach ($user_fieldsArray as $user_fieldElement) {
					$user_field = new user_field();
					$user_field->set_from_array($user_fieldElement);
					array_push($user_fields, $user_field);
				}
			}
			return $user_fields;
		}
	}

	class user_data {
		private $id = 0;
		private $user_id = 0;
		private $user_field_id = 0;
		private $value = '';
		private $update = false;

		private $user_class = false;
		private $user_field_class = false;

		function __construct($id = false) {
			if ($id) 
				$this->load((int)$id);
		}

		function get_id() {
			return (int)$this->id;
		}

		function set_id($id) {
			$this->id = (int)$id;
		}

		function get_user_id() {
			return (int)$this->user_id;
		}

		function get_user() {
			if (!$this->user_class) 
				$this->user_class = new user($this->get_user_id());
			return $this->user_class;
		}

		function set_user_id($user_id) {
			$this->user_id = (int)$user_id;
			$this->user_class = false;
		}

		function get_user_field_id() {
			return (int)$this->user_field_id;
		}

		function get_user_field() {
			if (!$this->user_field_class) 
				$this->user_field_class = new user_field($this->get_user_field_id());
			return $this->user_field_class;
		}

		function set_user_field($user_field) {
			if (is_a($user_field, 'user_field')) {
				$this->user_field_id = $user_field->get_id();
				$this->user_field_class = $user_field;
			}
		}

		function set_user_field_id($user_field_id) {
			$this->user_field_id = (int)$user_field_id;
			$this->user_field_class = false;
		}

		function get_key() {
			return $this->get_user_field()->get_key();
		}

		function get_value() {
			$type = $this->get_user_field()->get_type();
			switch ($type) {
				case 'int':
				case 'integer':
					$value = (int)$this->value;
					break;
				case 'float':
				case 'double':
					$value = (float)$this->value;
					break;
				case 'bool':
				case 'boolean':
					$value = $this->value? true : false;
					break;
				case 'array':
					$value = json_decode($this->value, true);
					break;
				case 'text':
					$value = trim($this->value);
					break;
				case 'string':
					$value = trim(strip_tags($this->value));
					break;
				default:
					$value = $this->value;
			}
			return $value;
		}

		function set_value($value) {
			$this->update = true;
			$type = $this->get_user_field()->get_type();
			switch ($type) {
				case 'int':
				case 'integer':
					$value = (int)$value;
					break;
				case 'float':
				case 'double':
					$value = (float)$value;
					break;
				case 'bool':
				case 'boolean':
					$value = $value? 1 : 0;
					break;
				case 'array':
					$value = json_encode($value);
					break;
				case 'text':
					$value = trim($value);
					break;
				case 'string':
					$value = trim(strip_tags($value));
					break;
				default:
					$value = $value;
			}
			$this->value = $value;
		}

		function set_from_array($user_data) {
			if (isset($user_data['id']))
				$this->set_id($user_data['id']);
			if (isset($user_data['user_id']))
				$this->set_user_id($user_data['user_id']);
			if (isset($user_data['user_field_id']))
				$this->set_user_field_id($user_data['user_field_id']);
			if (isset($user_data['value']))
				$this->set_value($user_data['value']);
		}

		function  load($id) {
			$user_data =  selo('users_data', array('id' => $id));
			$this->set_from_array($user_data);
		}

		function add() {
			if (!$this->update)
				$this->set_value($this->get_user_field()->get_default());
			ins('users_data', array(
				'user_id' => $this->get_user_id(),
				'user_field_id' => $this->get_user_field_id(),
				'value' => $this->get_value()
			));
			$this->load(lastID());
		}

		function update() {
			if ($this->update) {
				upd('users_data', array(
					'user_id' => $this->get_user_id(),
					'user_field_id' => $this->get_user_field_id(),
					'value' => $this->get_value()
				), array('id' => $this->get_id()));
				$this->update = false;
				$this->load($this->get_id());
			}
		}

		function delete() {
			del('users_data', array('id' => $this->get_id()));
		}

		static function get_user_data($where ='', $order = '') {
			$user_dataElement = selo('users_data', $where, $order, 1);
			if (!$user_dataElement['id'])
				return false;
			$user_data = new user_data();
			$user_data->set_from_array($user_dataElement);
			return $user_data;
		}

		static function get_users_data($where ='', $order = '', $limit = '') {
			$users_dataArray = sel('users_data', $where, $order, $limit);
			$users_data = array();
			if (is_array($users_dataArray)) {
				foreach ($users_dataArray as $user_dataElement) {
					$user_data = new user_data();
					$user_data->set_from_array($user_dataElement);
					array_push($users_data, $user_data);
				}
			}
			return $users_data;
		}
	}

	class user_log {
		private $id = 0;
		private $user_id = 0;
		private $ip = '';
		private $event = '';
		private $type = 0;
		private $time = '';
		private $data = '';

		private $user_class = false;

		function __construct($id = false) {
			if ($id) 
				$this->load((int)$id);
		}

		function get_id() {
			return (int)$this->id;
		}

		function set_id($id) {
			$this->id = (int)$id;
		}

		function get_user_id() {
			return (int)$this->user_id;
		}

		function get_user() {
			if (!$this->user_class) 
				$this->user_class = new user($this->get_user_id());
			return $this->user_class;
		}

		function set_user_id($user_id) {
			$this->user_id = (int)$user_id;
			$this->user_class = false;
		}

		function get_ip() {
			return $this->ip;
		}

		function set_ip($ip) {
			$this->ip = substr(strip_tags(trim($ip)), 0, 15);
		}

		function get_event() {
			return $this->event;
		}

		function set_event($event) {
			$this->event = substr(strip_tags(trim($event)), 0, 128);
		}

		function get_type() {
			return (int)$this->type;
		}

		function set_type($type) {
			$this->type = (int)$type;
		}

		function get_time() {
			return $this->time;
		}
		
		function get_formated_time($format = 'd.m.Y H:i:s') {
			return date($format, date_sql_to_timestamp($this->get_time()));
		}

		function set_time($time) {
			$this->time = $time;
		}

		function get_data() {
			return $this->data;
		}

		function set_data($data) {
			$this->data = $data;
		}

		function set_from_array($user_log) {
			if (isset($user_log['id']))
				$this->set_id($user_log['id']);
			if (isset($user_log['user_id']))
				$this->set_user_id($user_log['user_id']);
			if (isset($user_log['ip']))
				$this->set_ip($user_log['ip']);
			if (isset($user_log['event']))
				$this->set_event($user_log['event']);
			if (isset($user_log['type']))
				$this->set_type($user_log['type']);
			if (isset($user_log['time']))
				$this->set_time($user_log['time']);
			if (isset($user_log['data']))
				$this->set_data(is_array($user_log['data'])? $user_log['data'] : json_decode($user_log['data'], true));
		}

		function load($id) {
			$user_log = selo('user_logs', array('id' => $id));
			$this->set_from_array($user_log);
		}

		function add() {
			ins('user_logs', array(
				'user_id' => $this->get_user_id(),
				'ip' => $this->get_ip(),
				'event' => $this->get_event(),
				'type' => $this->get_type(),
				'data' => $this->get_data()
			));
			$this->load(lastID());
		}

		function update() {
			upd('user_logs', array(
				'user_id' => $this->get_user_id(),
				'ip' => $this->get_ip(),
				'event' => $this->get_event(),
				'type' => $this->get_type(),
				'data' => $this->get_data()
			), array('id' => $this->get_id()));
			$this->load($this->get_id());
		}

		function delete() {
			del('user_logs', array('id' => $this->get_id()));
		}

		static function get_user_log($where ='', $order = '') {
			$user_logElement = selo('user_logs', $where, $order, 1);
			if (!$user_logElement['id'])
				return false;
			$user_log = new user_log();
			$user_log->set_from_array($user_logElement);
			return $user_log;
		}

		static function get_user_logs($where ='', $order = '', $limit = '') {
			$user_logsArray = sel('user_logs', $where, $order, $limit);
			$user_logs = array();
			if (is_array($user_logsArray)) {
				foreach ($user_logsArray as $user_logElement) {
					$user_log = new user_log();
					$user_log->set_from_array($user_logElement);
					array_push($user_logs, $user_log);
				}
			}
			return $user_logs;
		}
	}
?>