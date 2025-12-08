<?php

add_post('/api/reviews/', 'opencase_get_reviews');
add_post('/api/review/add/', 'opencase_add_new_review');

function opencase_get_reviews() {
	$json = [
		'success' => true,
		'reviews' => []
	];
	$page = isset($_POST['page']) ? (int) $_POST['page'] : 0;
	$coutPerPage = 10;
	$reviews = get_reviews('moderate = 1 or user_id = ' . user()->get_id(), array('time_add' => 'DESC'), [$page * $coutPerPage, $coutPerPage]);
	$json['hasMore'] = (count($reviews) >= $coutPerPage);
	foreach ($reviews as $review) {
		$json['reviews'][] = [
			'id' => $review->get_id(),
			'text' => str_replace(['\\\r', '\\\n'], ['', '<br>'], $review->get_text()),
			'user' => [
				'name' => $review->get_user()->get_name(),
				'steamId' => $review->get_user()->get_data('steam_id'),
				'image' => $review->get_user()->get_data('image'),
			]
		];
	}
	echo_json($json);
}

function opencase_add_new_review() {
	$json = ['success' => false];
	if (is_login()) {
		if (!empty($_POST['text'])) {
			$review = new review();
			$review->set_user_id(user()->get_id());
			$review->set_text($_POST['text']);
			$review->add_review();
			$json['success'] = true;
			$json['msg'] = 'Отзыв успешно добавлен.';
		} else {
			$json['error'] = 'Вы не ввели отзыв';
		}
	} else {
		$json['error'] = 'Вы не авторизовались на сайте';
	}
	echo_json($json);
}
