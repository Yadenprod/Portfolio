<?php

class centrifugo {

	const URL = 'http://127.0.0.1:8888/api';
	const API_KEY = '80b25548-dacf-4f49-af92-7ea723a9d79e';
	const ENABLED = true;

	protected static $instance = null;

	protected static function getInstance() {
		if (is_null(self::$instance)) {
			self::$instance = new CentrifugoClient(self::URL, self::API_KEY);
		}
		return self::$instance;
	}

	public static function sendItem($dItem, $time = 0) {
		if (!self::ENABLED) {
			return;
		}
		try {
			$json = [
				'items' => [
					[
						'id' => $dItem->get_id(),
						'rarity' => $dItem->get_item_class()->get_css_quality_class(),
						'from' => $dItem->get_from(),
						'image' => $dItem->get_item_class()->get_steam_image(),
						'name' => $dItem->get_item_name(),
						'short_name' => $dItem->get_item_class()->get_name_no_stattrack_no_quality(),
						'time' => $dItem->get_time_drop(),
						'price' => $dItem->get_price(),
						'alt_name' => $dItem->get_item_name_alt(),
						'user_id' => $dItem->get_user_class()->get_data('steam_id'),
						'user_img' => $dItem->get_user_class()->get_data('image'),
						'user_name' => $dItem->get_user_class()->get_name(),
						'source_img' => $dItem->get_source_image(),
						'source_img_alt' => $dItem->get_source_image_alt(),
						'source_css_class' => $dItem->get_source_css_class(),
						'source_link' => $dItem->get_source_link(),
						'waittime' => $time
					]
				],
				'success' => true
			];
			self::getInstance()->publish("addDroppedItem", $json);
		} catch (\Exception $ex) {
			
		}
	}

	public static function sendStats() {
		if (!self::ENABLED) {
			return;
		}
		try {
			$json = array(
				'success' => true,
				'count_open_case' => get_count_open_cases(),
				'count_create_contracts' => get_count_create_contracts(),
				'count_reg_users' => get_count_reg_users(),
				'online' => get_count_onlie(),
				'today_online' => get_count_today_online(),
				'today_count_open_case' => get_count_today_open_cases(),
				'today_count_create_contracts' => get_count_today_create_contracts(),
			);
			$json = array_merge($json, stats::getAdditionalStatsArray());
			self::getInstance()->publish("updateStats", $json);
		} catch (\Exception $ex) {
			
		}
	}

}
