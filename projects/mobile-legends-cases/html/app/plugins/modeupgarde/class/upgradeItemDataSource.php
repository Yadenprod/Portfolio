<?php

abstract class upgradeItemDataSource {

	public static function getImage($dItem) {
		$upgradeId = db()->query_once('SELECT id FROM opencase_upgrades WHERE item_id = ' . $dItem->get_id());
		if (isset($upgradeId['id'])) {
			$upgrade = new upgrade($upgradeId['id']);
			return $upgrade->getImage();
		}
		return '';
	}

	public static function getImageAlt($dItem) {
		return 'Апгрейд';
	}

	public static function getCssClass($dItem) {
		return 'upgrade';
	}

	public static function getLink($dItem) {
		return '/upgrade/';
	}

}
