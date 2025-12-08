<?php
	function get_settings() {
		return ws()->get_settings();
	}
	
	function get_setval($key) {
		return ws()->get_settings()->get_setting_value($key);
	}
	
	function add_setval($key, $val, $comment = '', $type = 'text') {
		ws()->get_settings()->add_setting($key, $val, $comment, $type);
	}
	
	function update_setval($key, $val) {
		ws()->get_settings()->update_value($key, $val);
	}
	
	function delete_setval($key) {
		ws()->get_settings()->delete_setting($key);
	}
?>