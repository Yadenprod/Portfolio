<?php
	class Cache {
		var $memcached = false;
		var $servers = array();
		var $local = array();
		
		function __construct($settings = false) {
			if (!$settings) {
				require_once SETTINGSFOLDER . '/CacheSet.php';
				$settings = $cache_settings;
			}
			if (class_exists('Memcache') && $settings['enable']) {
				$this->memcached = new Memcache();
				$this->servers = $settings['servers'];
				if (count($this->servers) > 0) {
					foreach($this->servers as $key => $value) {
						$res = $this->memcached->connect($value['servername'], isset($value['port'])? $value['port'] : 11211);
					}
				}
			} else {
				return false;
			}
		}
		
		function get_memcahed() {
			return $this->memcached;
		}
		
		function set($key, $value, $expiration = 1440) {
			if ($this->memcached) {
				return $this->memcached->set($key, $value, false, $expiration);
			} else {
				return $this->local[$key] = $value; 
			}
		}
		
		function get($key) {
			if ($this->memcached) {
				return $this->memcached->get($key);
			} else {
				return isset($this->local[$key])? $this->local[$key] : false;
			}
		}
		
		function delete($key) {
			if ($this->memcached) {
				return $this->memcached->delete($key);
			} else {
				if (isset($this->local[$key]))
					unset($this->local[$key]);
				return false;
			}
		}
		
		function flush() {
			if ($this->memcached) {
				return $this->memcached->flush();
			} else {
				$this->local = [];
				return false;
			}
		}
		
		function add_server($servername, $port = 11211) {
			$server = array('servername' => $domain, 'port' => $port);
			$this->servers[] = $server;
			if ($this->memcached) {
				$this->memcached->addServer($servername, $port);
			}
		}
		
		function connect($servername, $port = 11211) {
			$this->memcached->connect($servername, $port);
		}
		
		function connect_all() {
			foreach($this->servers as $key => $value) {
				$this->memcached->connect($value['servername'], $value['port']);
			}
		}
		
		function close() {
			if ($this->memcached) {
				$this->memcached->close();
			} else {
				return false;
			}
		}
	}
?>