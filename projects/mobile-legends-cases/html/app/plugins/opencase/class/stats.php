<?php

abstract class stats {
	
	private static $additionalStats = [];
	private static $additionalUserStats = [];
	
	public static function addAditionalStat($key, $settingsKey) {
		self::$additionalStats[$key] = $settingsKey;
	}
	
	public static function addAditionalUserStat($key, $functionName) {
		self::$additionalUserStats[$key] = $functionName;
	}
	
	public static function getAdditionalStatsArray() {
		$res = [];
		foreach (self::$additionalStats as $key => $settingsKey) {
			$res[$key] = number_format(get_setval($settingsKey), 0, '', ' ');
		}
		return $res;
	}
	
	public static function addAditionalUserStatsArray($user) {
		$res = [];
		foreach (self::$additionalUserStats as $key => $functionName) {
			$res[$key] = $functionName($user);
		}
		return $res;
	}
	
}
