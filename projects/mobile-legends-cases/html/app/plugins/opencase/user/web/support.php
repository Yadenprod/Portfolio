<?php

add_app('/support/', 'support_index');
add_post('/support/send/', 'support_send');

function support_index($args) {
	set_content('');
	set_title('Тех. поддержка');
	set_title_page('Тех. поддержка');
	set_tpl('support.php');
}

function support_send() {
	if (is_login()) {
		$user = get_user();
		$ticket = new ticket();
		$ticket->set_theme(db()->nomysqlinj($_REQUEST['theme']));
		$ticket->set_game_id(db()->nomysqlinj(str_replace('№', '', str_replace('#', '', $_REQUEST['game_id']))));
		$ticket->set_user_id($user->get_id());
		$ticket->set_status(0);
		$ticket->set_assessment(0);
		$ticket->add_ticket();
		$lstID = db()->get_last_id();
		$attachment = '';
		if (isset($_FILES['attachments'])) {
			$files = array();
			foreach ($_FILES['attachments']['name'] as $id => $file) {
				$file = upload_file('attachments', $id, array('png', 'jpg'), 2048);
				if ($file) {
					array_push($files, $file);
				}
			}
			if (count($files) > 0) {
				$attachment = implode(';', $files);
			}
		}
		$message = new ticket_message();
		$message->set_ticket_id($lstID);
		$message->set_text($_REQUEST['text']);
		$message->set_attachment($attachment);
		$message->set_from(0);
		$message->add_ticket_message();
		redirect_srv_msg('', '/support/');
	} else {
		redirect_srv_msg('', '/');
	}
	exit();
}
