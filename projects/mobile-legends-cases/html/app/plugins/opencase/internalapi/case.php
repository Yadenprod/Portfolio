<?php

add_post('/api/casesbycategory/', 'opencase_get_all_case_data_by_category');
add_post('/api/case/([^\/]+)/', 'opencase_get_case_data');
add_post('/api/casesbycategory/default/', 'opencase_get_default_cases_data_by_category');

function opencase_get_all_case_data_by_category() {
	$json = ['success' => true];
	$caseInst = new ocase();
	$json['casesData'] = [];
	foreach (get_case_category() as $caseCategory) {
		$cases = $caseInst->get_ocases('enable = 1 AND category = ' . $caseCategory->get_id(), 'position ASC');
		if (empty($cases)) {
			continue;
		}
		$casesData = [];
		foreach ($cases as $case) {
			if (!$case->is_available()) {
				continue;
			}
			$casesData[] = [
				'id' => $case->get_id(),
				'name' => $case->get_name(),
				'label' => $case->get_label(),
				'type' => $case->get_type(),
				'cssRarity' => $case->get_rarity_css(),
				'key' => $case->get_key(),
				'sale' => $case->get_total_sale(),
				'price' => $case->get_price(),
				'salePrice' => $case->get_sale_price(),
				'availTime' => (!empty($case->get_time_limit()) ? ($case->get_time_limit() - time()) : false),
				'caseImage' => $case->get_src_image() != '/uploads/' ? $case->get_src_image() : false,
				'itemImage' => $case->get_src_item_image() != '/uploads/' ? $case->get_src_item_image() : false,
			];
		}
		if (empty($casesData)) {
			continue;
		}
		$json['casesData'][] = [
			'id' => $caseCategory->get_id(),
			'name' => $caseCategory->get_name(),
			'cases' => $casesData
		];
	}
	echo_json($json);
}

function opencase_get_case_data($args) {
	$json = ['success' => false];
	$caseKey = db()->nomysqlinj($args[0]);
	$case = new ocase();
	$case->load_from_key($caseKey);
	if ($case->get_id() != '') {
		if (!$case->is_available()) {
			$json['case'] = [
				'enable' => false
			];
		} else {
			$countOpenPerPeriod = 0;
			$sumDepPerPeriod = 0;
			if (is_login()) {
				$countOpenPerPeriod = get_count_case_per_period($case->get_id());
				$sumDepPerPeriod = get_count_deposite_per_period();
			}
			$json['case'] = [
				'enable' => true,
				'id' => $case->get_id(),
				'name' => $case->get_name(),
				'label' => $case->get_label(),
				'category' => $case->get_category(),
				'description' => $case->get_description(),
				'type' => $case->get_type(),
				'key' => $case->get_key(),
				'salePrice' => $case->get_sale_price(),
				'finalPrice' => $case->get_final_price(),
				'cssRarity' => $case->get_rarity_css(),
				'availTime' => (!empty($case->get_time_limit()) ? ($case->get_time_limit() - time()) : false),
				'caseImage' => $case->get_src_image() != '/uploads/' ? $case->get_src_image() : false,
				'allowOpen' => ($case->get_type() == ocase::TYPE_DEFAULT && $case->get_price() > 0) || ($case->get_type() == ocase::TYPE_DEPOSITE && can_open_free_case($case, $countOpenPerPeriod, $sumDepPerPeriod)) || ($case->get_type() == ocase::TYPE_PROMOCODE),
				'openCount' => $case->get_open_count(),
				'maxOpenCount' => $case->get_max_open_count() > 0 ? $case->get_max_open_count() : false,
			];
			if ($case->get_type() == ocase::TYPE_DEFAULT) {
				if (is_login() && get_setval('opencase_freeopen') == 1) {
					$countOpencase = get_count_opencase($case->get_id()) % 6;
					$caseLeft = 5 - $countOpencase;
					$json['case']['freeopen'] = [
						'enable' => true,
						'opened' => $countOpencase,
						'left' => $caseLeft
					];
				} else {
					$json['case']['freeopen'] = [
						'enable' => false,
					];
				}
			} elseif ($case->get_type() == ocase::TYPE_DEPOSITE) {
				$timeBeforeOpen = 0;
				if ($countOpenPerPeriod >= $case->get_dep_open_count()) {
					$timeBeforeOpen = get_time_before_deposit_case_free_open($case->get_id());
				}
				$json['case']['deposit'] = [
					'openedCount' => $countOpenPerPeriod,
					'daySum' => $sumDepPerPeriod,
					'minForOpen' => $case->get_dep_for_open(),
					'possibleCount' => $case->get_dep_open_count(),
					'checkDayCount' => get_setval('opencase_deposit_check_day'),
					'timeBeforeOpen' => $timeBeforeOpen
				];
			}
		}
		$json['items'] = [];
		$item = new itemincase();
		$items = $item->get_itemincases('case_id = ' . $case->get_id(), 'position ASC, id ASC');
		$caseItems = [];
		foreach ($items as $item) {
			$caseItems[$item->get_item_class()->get_clear_name_key()] = $item;
		}
		foreach ($caseItems as $item) {
			$json['items'][] = [
				'name' => $item->get_item_class()->get_name_no_stattrack_no_quality(),
				'image' => $item->get_item_class()->get_steam_image(),
				'rarity' => $item->get_item_class()->get_css_quality_class(),
				'quality' => $item->get_item_class()->get_quality()
			];
		}
		$json['success'] = true;
	}
	echo_json($json);
}

function opencase_get_default_cases_data_by_category() {
	$json = ['success' => true];
	$caseInst = new ocase();
	$json['casesData'] = [];
	foreach (get_case_category() as $caseCategory) {
		$cases = $caseInst->get_ocases('enable = 1 AND type = 0 AND category = ' . $caseCategory->get_id(), 'position ASC');
		if (empty($cases)) {
			continue;
		}
		$casesData = [];
		foreach ($cases as $case) {
			if (!$case->is_available()) {
				continue;
			}
			$casesData[] = [
				'id' => $case->get_id(),
				'name' => $case->get_name(),
				'label' => $case->get_label(),
				'cssRarity' => $case->get_rarity_css(),
				'key' => $case->get_key(),
				'sale' => $case->get_total_sale(),
				'price' => $case->get_price(),
				'salePrice' => $case->get_sale_price(),
				'availTime' => (!empty($case->get_time_limit()) ? ($case->get_time_limit() - time()) : false),
				'caseImage' => $case->get_src_image() != '/uploads/' ? $case->get_src_image() : false,
				'itemImage' => $case->get_src_item_image() != '/uploads/' ? $case->get_src_item_image() : false,
			];
		}
		if (empty($casesData)) {
			continue;
		}
		$json['casesData'][] = [
			'id' => $caseCategory->get_id(),
			'name' => $caseCategory->get_name(),
			'cases' => $casesData
		];
	}
	echo_json($json);
}
