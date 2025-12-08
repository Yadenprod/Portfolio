<?php
    function curl($url, $params = array(), $header = array(), $method = 'POST', $proxy = false) {
		$curl = curl_init($url.($method == 'GET'? '?'.http_build_query($params) : ''));
		curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
		curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);
		curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
		if ($method == 'POST') {
            curl_setopt($curl, CURLOPT_POST, true);
            curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($params));
        }
		if ($proxy) {
			$proxy = explode('@', $proxy);
			if (count($proxy) == 2) {
				curl_setopt($curl, CURLOPT_PROXYUSERPWD, $proxy[0]);
				$proxy[0] = $proxy[1];
			}
			curl_setopt($curl, CURLOPT_PROXY, $proxy[0]);
		}
		$result = curl_exec($curl);
		curl_close($curl);
		return $result;
	}

	function get($url, $params = array(), $header = array(), $proxy = false) {
		return curl($url, $params, $header, 'GET', $proxy);
	}

	function post($url, $params = array(), $header = array(), $proxy = false) {
		return curl($url, $params, $header, 'POST', $proxy);
	}
?>