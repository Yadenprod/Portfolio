<?php 
	class Settings
	{
		var $settings = array();
		
		function __construct() {
			$this->load_settings();
		}
		
		function get_setting($key) {
			return $this->settings[$key];
		}
		
		function get_settings() {
			return $this->settings;
		}
		
		function get_settings_class() {
			return $this;
		}
		
		function get_setting_value($key) {
			if (isset($this->settings[$key])) {
				switch($this->settings[$key]['type']) {
					case 'int':
					case 'integer':
						$value = (int)$this->settings[$key]['value'];
						break;
					case 'float':
					case 'real':				
					case 'double':
						$value = (float)$this->settings[$key]['value'];
						break;
					case 'bool':
					case 'boolean':
						$value = $this->settings[$key]['value'] == 1;
						break;
					case 'text':
					case 'string': 
						$value = (string)$this->settings[$key]['value'];
						break;
					case 'array':
						$value = json_decode($this->settings[$key]['value']);
						break;
					default:
						$value = (string)$this->settings[$key]['value'];
				}
				return $value;
			} else {
				return false;
			}
		}
		
		function set_settings($key, $value) {
			$this->settings[$key] = $value;
		}
		
		function clear_settings() {
			$this->settings = array();
		}
		
		function load_settings() {
			$setting = sel('settings'); 
			if ($setting) {
				foreach ($setting as $set) {
					$this->set_settings($set['setting'], $set);
				}
			}
		}
		
		function add_setting($key, $value, $comment = '', $type = 'text') {
			if ($key != '') {
				$setting = array('setting' => $key, 'value' => $value, 'comment' => $comment, 'type' => $type);
				ins('settings', $setting);
				$this->set_settings($key, $setting);
			}
		}
		
		function update_value($key, $value) {
			upd('settings', array('value' => $value), array('setting' => $key));
			$this->settings[$key]['value'] = $value;
		}
		
		function update_setting($key, $value, $comment, $type) {
			if ($key != '') {
				$setting = array('setting' => $key, 'value' => $value, 'comment' => $comment, 'type' => $type);
				upd('settings', $setting, array('setting' => $key));
				$this->set_settings($key, $setting);
			}
		}
		
		function delete_setting($key) {
			del('settings', array('setting' => $key));
			unset($this->settings[$key]);
		}
	}

?>