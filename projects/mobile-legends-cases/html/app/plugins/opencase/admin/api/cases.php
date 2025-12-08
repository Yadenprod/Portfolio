<?php

add_admin_post('/api/opencase/updateitempos/', 'admin_opencase_updateitempos');
add_admin_post('/api/opencase/updatecatpos/', 'admin_opencase_updatecatpos');
add_admin_post('/api/opencase/searchitemsincase/', 'admin_opencase_searchitemsincase');
add_admin_post('/api/opencase/searchitemsincaseadd/', 'admin_opencase_searchitemsincaseadd');
add_admin_post('/api/opencase/itemsincase/changewithdrawable/([0-9]+)/', 'admin_opencase_itemsincase_change_withdrawable');
add_admin_post('/api/opencase/itemsincase/changeusable/([0-9]+)/', 'admin_opencase_itemsincase_change_usable');
add_admin_post('/api/opencase/itemsincase/changewithdrawable/all/([0-9]+)/', 'admin_opencase_itemsincase_change_withdrawable_all');
add_admin_post('/api/opencase/itemsincase/changeusable/all/([0-9]+)/', 'admin_opencase_itemsincase_change_usable_all');
add_admin_post('/api/opencase/updatecasepos/', 'admin_opencase_updatecasepos');

function admin_opencase_updateitempos() {
	$json = array('success' => false);
	if (isset($_POST['positions'])) {
		$position = explode(';', db()->nomysqlinj($_POST['positions']));
		if (is_array($position) && count($position) > 0) {
			foreach ($position as $pos) {
				$data = explode(':', $pos);
				$item = new itemincase($data[0]);
				$item->set_position($data[1]);
				$item->update_itemincase();
			}
			$json['success'] = true;
		} else {
			$json['error'] = 'Не верные данные';
		}
	} else {
		$json['error'] = 'Не указаны данные для обновления';
	}
	echo_json($json);
}

function admin_opencase_updatecatpos() {
	$json = array('success' => false);
	if (isset($_POST['positions'])) {
		$position = explode(';', db()->nomysqlinj($_POST['positions']));
		if (is_array($position) && count($position) > 0) {
			foreach ($position as $pos) {
				$data = explode(':', $pos);
				$category = new caseCategory($data[0]);
				$category->set_pos($data[1]);
				$category->update_caseCategory();
			}
			$json['success'] = true;
		} else {
			$json['error'] = 'Не верные данные';
		}
	} else {
		$json['error'] = 'Не указаны данные для обновления';
	}
	echo_json($json);
}

function admin_opencase_searchitemsincase() {
	$json = array('success' => false);
	if (isset($_POST['name'])) {
		$item = new item();
		$where = '1 = 0';
		$name = !empty($_POST['name']) ? $_POST['name'] : '';
		if (!empty($name)) {
			$where = 'name like "%' . db()->nomysqlinj(trim($name)) . '%"';
		}
		$allitems = $item->get_items($where, 'id DESC');
		$json['items'] = array();
		foreach ($allitems as $value) {
			array_push($json['items'], array(
				'id' => $value->get_id(),
				'name' => $value->get_name(),
				'image' => $value->get_steam_image('40f', '30f'),
				'count' => $value->get_count_on_bot(),
				'price' => $value->get_price(),
				'case' => strip_tags($_POST['case'])
			));
		}
		$json['success'] = true;
	}
	echo_json($json);
}

function admin_opencase_searchitemsincaseadd() {
	$json = array('success' => false);
	if (!empty($_POST['case']) && !empty($_POST['id'])) {
		$case = new ocase($_POST['case']);
		$item = new item($_POST['id']);
		$count = db()->query_once('select count(id) from opencase_itemincase where case_id = "' . $case->get_id() . '" and item_id = "' . $item->get_id() . '"');
		$count = $count['count(id)'];
		if ($count == 0) {
			$itemincase = new itemincase();
			$itemincase->set_case_id($case->get_id());
			$itemincase->set_item_id($item->get_id());
			$itemincase->set_chance(100);
			$itemincase->set_count_items(-1);
			$itemincase->set_enabled(1);
			$itemincase->set_position($itemincase->get_position_max($case->get_id()) + 1);
			$itemincase->add_itemincase();
			$json['item'] = array(
				'id' => db()->get_last_id(),
				'image' => $itemincase->get_item_class()->get_steam_image('40f', '30f'),
				'name' => $itemincase->get_item_class()->get_name(),
				'count' => $itemincase->get_text_count_items(),
				'count_on_bot' => $itemincase->get_item_class()->get_count_on_bot(),
				'price' => $itemincase->get_item_class()->get_price(),
				'chance' => $itemincase->get_chance(),
				'withdrawable' => $itemincase->get_withdrawable(),
				'usable' => $itemincase->get_usable(),
				'label' => $itemincase->get_label_enabled()
			);
			$json['success'] = true;
		}
	}
	echo_json($json);
}

function admin_opencase_itemsincase_change_withdrawable($args) {
	$json = ['success' => false];
	$itemincase = new itemincase($args[0]);
	if ($itemincase->get_id() != '') {
		if ($itemincase->get_withdrawable()) {
			$itemincase->set_withdrawable(0);
		} else {
			$itemincase->set_withdrawable(1);
		}
		$itemincase->update_itemincase();
		$json['success'] = true;
		$json['withdrawable'] = $itemincase->get_withdrawable();
	}
	echo_json($json);
}

function admin_opencase_itemsincase_change_usable($args) {
	$json = ['success' => false];
	$itemincase = new itemincase($args[0]);
	if ($itemincase->get_id() != '') {
		if ($itemincase->get_usable()) {
			$itemincase->set_usable(0);
		} else {
			$itemincase->set_usable(1);
		}
		$itemincase->update_itemincase();
		$json['success'] = true;
		$json['usable'] = $itemincase->get_usable();
	}
	echo_json($json);
}

function admin_opencase_itemsincase_change_withdrawable_all($args) {
	$json = ['success' => false];
	$itemincase = new itemincase();
	$allitems = $itemincase->get_itemincases('case_id = "' . db()->nomysqlinj($args[0]) . '"', 'position ASC, id ASC');
	$allWithdrawable = false;
	if (is_array($allitems)) {
		foreach ($allitems as $item) {
			if ($item->get_withdrawable()) {
				$allWithdrawable = true;
				break;
			}
		}
		foreach ($allitems as $item) {
			if ($allWithdrawable) {
				$item->set_withdrawable(0);
			} else {
				$item->set_withdrawable(1);
			}
			$item->update_itemincase();
		}
		$json['success'] = true;
		$json['withdrawable'] = !$allWithdrawable;
	}
	echo_json($json);
}

function admin_opencase_itemsincase_change_usable_all($args) {
	$json = ['success' => false];
	$itemincase = new itemincase();
	$allitems = $itemincase->get_itemincases('case_id = "' . db()->nomysqlinj($args[0]) . '"', 'position ASC, id ASC');
	$allUsable = false;
	if (is_array($allitems)) {
		foreach ($allitems as $item) {
			if ($item->get_usable()) {
				$allUsable = true;
				break;
			}
		}
		foreach ($allitems as $item) {
			if ($allUsable) {
				$item->set_usable(0);
			} else {
				$item->set_usable(1);
			}
			$item->update_itemincase();
		}
		$json['success'] = true;
		$json['usable'] = !$allUsable;
	}
	echo_json($json);
}

function admin_opencase_updatecasepos() {
	$json = array('success' => false);
	if (isset($_POST['positions'])) {
		$position = explode(';', db()->nomysqlinj($_POST['positions']));
		if (is_array($position) && count($position) > 0) {
			foreach ($position as $pos) {
				$data = explode(':', $pos);
				$case = new ocase($data[0]);
				$case->set_position($data[1]);
				$case->update_ocase();
			}
			$json['success'] = true;
		} else {
			$json['error'] = 'Не верные данные';
		}
	} else {
		$json['error'] = 'Не указаны данные для обновления';
	}
	echo_json($json);
}
