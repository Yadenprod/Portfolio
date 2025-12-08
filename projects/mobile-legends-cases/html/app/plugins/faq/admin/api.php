<?php

add_admin_post('/api/updatefaqpos/', 'admin_updatefaqpos');

function admin_updatefaqpos() {
	$json = array('success' => false);
	if (isset($_POST['positions'])) {
		$position = explode(';', db()->nomysqlinj($_POST['positions']));
		if (is_array($position) && count($position) > 0) {
			foreach ($position as $pos) {
				$data = explode(':', $pos);
				$question = new FAQElement($data[0]);
				$question->setPosition($data[1]);
				$question->save();
			}
			$json['success'] = true;
		} else {
			$json['error'] = 'Неверные данные';
		}
	} else {
		$json['error'] = 'Не указаны данные для обновления';
	}
	echo_json($json);
}
