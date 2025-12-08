<?php

add_app('/review/', 'review_index');
add_post('/review/add/', 'review_add');

function review_index() {
	set_content('');
	set_title('Отзывы');
	set_title_page('Отзывы');
	set_tpl('reviews.php');
	add_jscript('$(document).ready(function() {
			$(".review-form form").on("submit", function() {
				$(".review-form textarea").removeClass("err");
				if ($(".review-form textarea").val() == "") {
					$(".review-form textarea").addClass("err");
					return false;
				}
			});
		});', 10);
}

function review_add() {
	if (is_login() && !empty($_POST['text'])) {
		$review = new review();
		$review->set_user_id(user()->get_id());
		$review->set_text($_POST['text']);
		$review->add_review();
		redirect_srv_msg('', '/review/');
	}
	redirect_srv_msg('', '/review/');
}
