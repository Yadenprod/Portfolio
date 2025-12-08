<?php 
	function get_host($host = false) {
		if (!$host) $host = $_SERVER['HTTP_HOST'];
		return parse_url($host , PHP_URL_HOST);
	}

	function uri() {
		return $_SERVER['REQUEST_URI'];
	}

	function get_current_url() {
		return get_site_url($_SERVER['REQUEST_URI']);
	}
	
	function get_back_url() {
		if ($_SERVER['HTTP_REFERER'] != '')
			$url = $_SERVER['HTTP_REFERER'];
		else
			$url = '/';
		return $url;
	}
	
	function get_site_url($uri = false) {
		$host_name = !empty($_SERVER['HTTP_HOST'])? $_SERVER['HTTP_HOST'] : $_SERVER['SERVER_NAME'];
		$url  = !empty($_SERVER['REQUEST_SCHEME'])? $_SERVER['REQUEST_SCHEME'].'://'.$host_name : (@($_SERVER['HTTPS'] != 'on')? 'http://'.$host_name :  'https://'.$host_name);
		$url .= ($_SERVER['SERVER_PORT'] != 80 && $_SERVER["SERVER_PORT"] != 443) ? ':'.$_SERVER['SERVER_PORT'] : '';
		$url .= $uri? $uri : '';
		return $url; 
	}
	
	function get_canonical() {
		if (!get_setval('site_url')) {
			return false;
		}
		if (empty(get_url())) {
			return false;
		}
		return get_setval('site_url').get_url();
	}
?>