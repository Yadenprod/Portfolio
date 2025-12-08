<?php
	function checklastv() {
		$lastv = false;
		if (is_url_availible('http://'.UPDATEDOMEIN.'/update/lastversion/'))
			$lastv = file_get_contents('http://'.UPDATEDOMEIN.'/update/lastversion/');
		return $lastv;
	}
	
	function checkchanglog($ver = '') {
		$log = false;
		if ($ver == '')
			$ver = get_setval('cms_version');
		$ver = str_replace('.', '_', $ver);
		if (is_url_availible('http://'.UPDATEDOMEIN.'/update/changelog/'.$ver.'/'))
			$log = file_get_contents('http://'.UPDATEDOMEIN.'/update/changelog/'.$ver.'/');
		return $log;
	}
	
	function is_url_availible($domain) {
		if(!filter_var($domain, FILTER_VALIDATE_URL)){
			   return false;
		}
		$curlInit = curl_init($domain);
		curl_setopt($curlInit, CURLOPT_CONNECTTIMEOUT, 10);
		curl_setopt($curlInit, CURLOPT_HEADER, true);
		curl_setopt($curlInit, CURLOPT_NOBODY, true);
		curl_setopt($curlInit, CURLOPT_RETURNTRANSFER, true);
		$response = curl_exec($curlInit);
		$res = curl_getinfo ($curlInit);
		curl_close($curlInit);
		if ($res['http_code'] == 200) return true;
		return false;
   }
?>