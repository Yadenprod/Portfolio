<?php

abstract class battleItemDataSource {

	public static function getImage($dItem) {
		return 'data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA=';
	}

	public static function getImageAlt($dItem) {
		return 'Сражения';
	}

	public static function getCssClass($dItem) {
		return 'battle';
	}

	public static function getLink($dItem) {
		return '/battles/';
	}

}
