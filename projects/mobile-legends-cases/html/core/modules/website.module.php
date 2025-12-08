<?php
	function ws() {
		return WebSite::get_instance();
	}

	function wp() {
		return ws()->get_webpage();
	}
	
	function ch() {
		return ws()->get_cache();
	}
	
	function db() {
		return ws()->get_db();
	}
	
	function st() {
		return ws()->get_settings();
	}
	
	function pm() {
		return ws()->get_pluginmanager();
	}

	function device() {
        return ws()->get_device();
	}
	
	function user() {
		return ws()->get_user();
	}

	function admin() {
		return ws()->get_admin();
	}
	
	function wsexit() {
		ws()->close();
		exit();
	}
	
	function runtime($ms = true) {
		$time = microtime(true) - ws()->get_time_start();
		return $ms? intval($time * 1000) : $time;
	}
?>