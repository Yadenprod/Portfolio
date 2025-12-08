<?php
	function lang($key) {
		global $lang;
		echo $lang[$key];
	}
	
	function get_lang($key) {
		global $lang;
		return $lang[$key];
	}
?>