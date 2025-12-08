<?php
	function debug($flag = false) {
		if ($flag) {
			ini_set('error_reporting', E_ALL);
			ini_set('display_errors', 1);
			ini_set('display_startup_errors', 1);
		} else {
			ini_set('error_reporting', 0);
			ini_set('display_errors', 0);
			ini_set('display_startup_errors', 0);
		}
	}

	function ww($elem) {
		echo '<pre>';
		var_dump($elem);
		echo '</pre>';
	}
	
	function we($elem = '') {
		ww($elem);
		wsexit();
	}
	
	function wt($exit = false) {
		ww(runtime());
		if ($exit)
			wsexit();
	}
	
	function dt($exit = false) {
		ww(timesq());
		if ($exit)
			wsexit();
	}
	
	function dc($exit = false) {
		ww(countq());
		if ($exit)
			wsexit();
	}
	
	function getLA($time = false) {
		if (function_exists('sys_getloadavg')) {
			$la = sys_getloadavg();
			if ($time) {
				if ($time == 15) {
					return $la[2];
				} elseif ($time == 5) {
					return $la[1];
				} else {
					return $la[0];
				}
			} else {
				return sys_getloadavg();
			}
		} else {
			return false;
		}
	}
?>