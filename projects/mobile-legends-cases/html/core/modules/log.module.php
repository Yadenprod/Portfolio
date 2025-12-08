<?php
	function add_log($event, $type = 'default', $data = array()) {
		if (function_exists('ins')) {
			ins('logs', array('ip' => getip(), 'event' => $event, 'type' => $type, 'data' => json_encode($data)));
		}
	}
?>