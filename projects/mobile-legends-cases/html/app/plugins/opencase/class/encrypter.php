<?php

abstract class encrypter {

	const OUTPUT_FOLDER = CMSFOLDER . 'ssl/';
	const KEY_BYTE_LENGTH = 128;
	const KEY_TYPE_PRIVATE = 1;
	const KEY_TYPE_PUBLIC = 2;
	const BOT_KEY_NAME = 'bot';
	const SITE_KEY_NAME = 'site';

	private static $keys = [];

	public static function generateKeyPair($keyName) {
		$config = [
			"digest_alg" => "sha256",
			"private_key_bits" => self::KEY_BYTE_LENGTH * 8,
			"private_key_type" => OPENSSL_KEYTYPE_RSA,
		];
		$key = openssl_pkey_new($config);
		$details = openssl_pkey_get_details($key);
		$publicKey = $details['key'];
		openssl_pkey_export($key, $privateKey);
		if (!is_dir(self::OUTPUT_FOLDER)) {
			mkdir(self::OUTPUT_FOLDER);
		}
		file_put_contents(self::OUTPUT_FOLDER . $keyName . '.pub', $publicKey);
		file_put_contents(self::OUTPUT_FOLDER . $keyName . '.key', $privateKey);
	}

	private static function getKey($keyName, $keyType) {
		switch ($keyType) {
			case self::KEY_TYPE_PRIVATE:
				$ext = '.key';
				break;
			case self::KEY_TYPE_PUBLIC:
				$ext = '.pub';
				break;
			default:
				return '';
		}
		if (!isset(self::$keys[$keyName][$keyType])) {
			self::$keys[$keyName][$keyType] = file_get_contents(self::OUTPUT_FOLDER . $keyName . $ext);
		}
		return self::$keys[$keyName][$keyType];
	}

	public static function encrypt($data, $keyName) {
		if (empty($data)) {
			return '';
		}
		$maxLen = self::KEY_BYTE_LENGTH - 11;
		$output = '';
		$publicKey = self::getKey($keyName, self::KEY_TYPE_PUBLIC);
		while ($data) {
			$input = substr($data, 0, $maxLen);
			$data = substr($data, $maxLen);
			openssl_public_encrypt($input, $encrypted, $publicKey);
			$output .= $encrypted;
		}
		return base64_encode($output);
	}

	public static function decrypt($data, $keyName) {
		if (empty($data)) {
			return '';
		}
		$data = base64_decode($data);
		$maxLen = self::KEY_BYTE_LENGTH;
		$output = '';
		$privateKey = self::getKey($keyName, self::KEY_TYPE_PRIVATE);
		while ($data) {
			$input = substr($data, 0, $maxLen);
			$data = substr($data, $maxLen);
			openssl_private_decrypt($input, $decrypted, $privateKey);
			$output .= $decrypted;
		}
		return $output;
	}

}
