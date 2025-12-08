<?php

add_loader('opencase_autosell_loader');

function opencase_autosell_loader() {
	if (get_setval('opencase_auto_sell')) {
		$items = db()->query('select * from opencase_droppeditems where status = 0 and (unix_timestamp(`time_drop`) - unix_timestamp(NOW()) + '. (get_setval('opencase_auto_sell_time') * 60) . ') < 0');
		if (count($items) > 0) {
			foreach ($items as $item) {
				sale_item($item);
			}
		}
	}
}

function sale_item($item) {
	if ($item['status'] == 0) {
		$user = new user($item['user_id']);
		inc_user_balance($user, $item['price']);
		add_balance_log($user->get_id(), $item['price'], 'Автоматическая продажа предмета №' . $item['id'], 2);
		db()->query_once('update opencase_droppeditems set status = 3 where id = ' . $item['id']);
		ch()->delete('droppedItem'.$item['id']);
	}
}
