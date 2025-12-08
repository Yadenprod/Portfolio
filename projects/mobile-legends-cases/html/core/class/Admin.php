<?php
	class admin {
		var $id = 0;
		var $name = '';
		var $password = '';
		var $email = '';
		var $phone = '';
		var $ips = '';
		var $login = false;
		
		function __construct($id = '') {
			if ($id != '') {
				$this->load($id);
			}
		}
		
		function get_id() {
			return (int)$this->id;
		}
		
		function set_id($id) {
			$this->id = (int)$id;
		}
		
		function get_name() {
			return strip_tags(trim($this->name));
		}
		
		function set_name($name) {
			$this->name = strip_tags(trim($name));
		}
		
		function get_password() {
			return strip_tags(trim($this->password));
		}

		static function hash_password($password) {
			return md5(sha1(md5(sha1(md5(md5(sha1('ADMIN'.':'.CMSSECRET.':'.$password)))))));
		}
		
		function set_password($password) {
			$this->password = strip_tags(trim($password));
		}
		
		function set_nohash_password($password) {
			$this->password = $this->hash_password($password);
		}
		
		function get_email() {
			return strip_tags(trim($this->email));
		}
		
		function set_email($email) {
			$this->email = strip_tags(trim($email));
		}
		
		function get_phone() {
			return strip_tags(trim($this->phone));
		}
		
		function set_phone($phone) {
			$this->phone = strip_tags(trim($phone));
		}
		
		function get_ips() {
			return $this->ips;
		}
		
		function get_ips_array() {
			$ips = explode(';', $this->ips);
			$countIps = 0;
			if (is_array($ips) && count($ips) > 0) {
				foreach ($ips as $key => $ip) {
					$ips[$key] = trim($ip);
					
					if (strlen($ips[$key]) > 0) {
						$countIps++;
					}
				}
				if ($countIps > 0)
					return $ips;
				else
					return false;
			} else {
				return false;
			}
		}
		
		function set_ips($ips) {
			$this->ips = strip_tags(trim($ips));
		}
		
		function set_ips_from_array($ips) {
			if (is_array($ips) && count($ips) > 0) {
				foreach ($ips as $key => $ip) {
					$ips[$key] = strip_tags(trim($ip));
				}
				$this->ips = implode(';', $ips);
			} else {
				return '';
			}
		}
		
		function get_login() {
			return $this->login;
		}
		
		function set_login($login) {
			$this->login = $login;
		}
		
		function login($name, $password) {
			$admin = admin::get_admin(array('name' => $name, 'password' => $this->hash_password($password)));
			if (!$admin) return false;
			$this->load($admin->get_id());
			$ips = $this->get_ips_array();
			if (!$ips || (is_array($ips) && in_array(getip(), $ips))) {
				$this->set_login(true);
				return true;
			} else {
				$this->set_login(false);
				return false;
			}
		}

		function auth() {
			if (!get_cookie('admin_token')) return false;
			$admin = admin::get_admin('MD5(CONCAT("ADMIN", `id`, ":", `name`, ":", `password`, ":", '.value(iptoken('ADMIN')).')) = '.value(get_cookie('admin_token')));
			if (!$admin) return false;
			$this->load($admin->get_id());
			$this->set_login(true);
			return true;
		}
		
		function is_login() {
			return $this->get_login();
		}
		
		function set_from_array($admin) {
			if (isset($admin['id']))
				$this->set_id($admin['id']);
			if (isset($admin['name']))
				$this->set_name($admin['name']);
			if (isset($admin['password']))
			$this->set_password($admin['password']);
			if (isset($admin['email']))
				$this->set_email($admin['email']);
			if (isset($admin['phone']))
				$this->set_phone($admin['phone']);
			if (isset($admin['ips']))
				$this->set_ips($admin['ips']);
		}
		
		function load($id) {
			$admin = selo('admin', array('id' => $id));
			$this->set_from_array($admin);
		}
		
		function add() {
			ins('admin', array(
				'name' => $this->get_name(),
				'password' => $this->get_password(),
				'email' => $this->get_email(),
				'phone' => $this->get_phone(),
				'ips' => $this->get_ips()
			));
			$this->load(lastID());
		}
		
		function update() {
			upd('admin', array(
				'id' => $this->get_id(),
				'name' => $this->get_name(),
				'password' => $this->get_password(),
				'email' => $this->get_email(),
				'phone' => $this->get_phone(),
				'ips' => $this->get_ips()
			), array('id' => $this->get_id()));
			$this->load($this->get_id());
		}
		
		function delete() {
			del('admin', array('id' => $this->get_id()));
		}

		static function get_admin($where = false, $order = false) {
			$adminElement = selo('admin', $where, $order);
			if (!$adminElement['id']) 
				return false;
			$admin = new admin();
			$admin->set_from_array($adminElement);
			return $admin;
		}

		static function get_admins($where = false, $order = false, $limit = false) {
			$adminsArray = sel('admin', $where, $order, $limit);
			$admins = array();
			if (is_array($adminsArray)) {
				foreach ($adminsArray as $adminElement) {
					$admin = new admin();
					$admin->set_from_array($adminElement);
					array_push($admins, $admin);
				}
			}
			return $admins;
		}
	}
?>
