<?php
add_post('/api/faq/', 'opencase_get_faq');

function opencase_get_faq() {
	$json = [
		'success' => true,
		'questions' => []
	];
	$questions = FAQElement::getAllEnabledQuestions();
	foreach ($questions as $question) {
		$json['questions'][] = [
			'question' => $question['question'],
			'answer' => $question['answer'],
		];
	}
	echo_json($json);
}


