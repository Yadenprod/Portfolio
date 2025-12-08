<?php
	function crypto_xor($str, $key) {
		$str = base64_encode($str);
		$keyIndex = 0;
		$result = '';
		for ($i = 0; $i < strlen($str); $i++) {
			$result .= $str[$i] ^ $key[$keyIndex];
			$keyIndex++;
			if ($keyIndex >= strlen($key))
				$keyIndex = 0;
		}
		return base64_encode($result);
	}
	
	function decrypto_xor($str, $key) {
		$str = base64_decode($str);
		$keyIndex = 0;
		$result = '';
		for ($i = 0; $i < strlen($str); $i++) {
			$result .= $str[$i] ^ $key[$keyIndex];
			$keyIndex++;
			if ($keyIndex >= strlen($key))
				$keyIndex = 0;
		}
		return base64_decode($result);
	}
?>