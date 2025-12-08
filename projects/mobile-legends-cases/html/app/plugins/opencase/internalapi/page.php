<?php

add_post('/api/page/', 'opencase_get_page_data');

function opencase_get_page_data() {
	$json = ['success' => false];
	if (!isset($_POST['url'])) {
		$json['error'] = 'Не указана страница';
	} else {
		$webpage = selo('webpage', ['url' => db()->nomysqlinj($_POST['url'])], ['namepage' => 'DESC']);
		if (empty($webpage)) {
			$json['error'] = 'Cтраница не найдена';
		} else {
			$json['success'] = true;
			$json['page'] = [
				'title' => $webpage['title'],
				'pageTitle' => $webpage['title_page'],
				'metaDes' => $webpage['meta_des'],
				'metKey' => $webpage['meta_key'],
				'content' => $webpage['content'],
			];
		}
	}
	echo_json($json);
}
