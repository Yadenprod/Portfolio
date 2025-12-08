<?php

add_post('/api/support/sendmsg/([0-9]+)/', 'support_sendmsg');
add_post('/api/support/open/([0-9]+)/', 'support_open');

function support_sendmsg($args) {
	$json = array('success' => false);
	if (!empty($_POST['text'])) {
		if (is_login()) {
			$user = get_user();
			$ticket = new ticket($args[0]);
			if ($ticket->get_user_id() == $user->get_id()) {
				if ($ticket->get_status() != 5 && $ticket->get_status() != 6) {
					$ticket->set_status(4);
					$ticket->update_ticket();
					$attachment = '';
					if (isset($_FILES) && is_array($_FILES) && count($_FILES) > 0) {
						$files = array();
						foreach ($_FILES as $id => $file) {
							$file = upload($file, array('png', 'jpg'), 2048);
							if ($file) {
								array_push($files, $file);
							}
						}
						if (count($files) > 0) {
							$attachment = implode(';', $files);
						}
					}
					$message = new ticket_message();
					$message->set_ticket_id($ticket->get_id());
					$message->set_text($_POST['text']);
					$message->set_attachment($attachment);
					$message->set_from(0);
					$message->add_ticket_message();
					$lstID = db()->get_last_id();
					$message->load_ticket_message($lstID);
					$json['success'] = true;
					$json['name'] = $ticket->get_user_class()->get_name();
					$json['date'] = replace_text_month($message->get_form_time_add('d F Y H:i'));
					$json['status'] = $ticket->get_user_status_text();
					$json['attachment'] = $message->get_attachments();
				} else {
					$json['error'] = 'Тикет закрыт. Вы больше не можете отправлять сообщения в рамках данного тикета';
				}
			} else {
				$json['error'] = 'Этот тикет не принадлежит Вам';
			}
		} else {
			$json['error'] = 'Вы не авторизовались на сайте';
		}
	} else {
		$json['error'] = 'Вы не ввели сообщение';
	}
	echo_json($json);
}

function support_open($args) {
	$json = array('success' => false);
	if (is_login()) {
		$user = get_user();
		$ticket = new ticket($args[0]);
		if ($ticket->get_user_id() == $user->get_id()) {
			if ($ticket->get_status() == 3) {
				$ticket->set_status(8);
				$ticket->update_ticket();
			}
			$json['success'] = true;
			$json['status'] = $ticket->get_user_status_text();
		}
	}
	echo_json($json);
}
