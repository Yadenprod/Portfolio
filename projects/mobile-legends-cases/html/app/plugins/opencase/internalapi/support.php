<?php

add_post('/api/support/tickets/', 'opencase_get_support_tickets');
add_post('/api/support/ticket/create/', 'opencase_support_tickets_create');

function opencase_get_support_tickets() {
	$json = ['success' => true, 'tickets' => []];
	if (is_login()) {
		$ticket = new ticket();
		$tickets = $ticket->get_tickets_with_message(' ticket.user_id = "' . user()->get_id() . '"', 'ticket_message.time_add DESC');
		foreach ($tickets as $ticket) {
			$ticketMessages = [];
			$messages = $ticket->get_messages();
			foreach ($messages as $message) {
				$ticketMessages[] = [
					'from' => $message->get_from(),
					'date' => replace_text_month($message->get_form_time_add('d F Y H:i')),
					'text' => str_replace(['\\\r', '\\\n'], ['', '<br>'], $message->get_text()),
					'attachments' => $message->get_attachments()
				];
			}
			$message = $ticket->get_first_message();
			$json['tickets'][] = [
				'id' => $ticket->get_id(),
				'theme' => $ticket->get_theme(),
				'status' => $ticket->get_status(),
				'statusText' => $ticket->get_user_status_text(),
				'shortText' => $message->get_short_text(),
				'date' => replace_text_month($message->get_form_time_add('d F Y H:i')),
				'userName' => $ticket->get_user_class()->get_name(),
				'messages' => $ticketMessages
			];
		}
	}
	echo_json($json);
}

function opencase_support_tickets_create() {
	$json = ['success' => false];
	if (is_login()) {
		if (!empty($_REQUEST['theme']) && !empty($_REQUEST['text'])) {
			$user = get_user();
			$ticket = new ticket();
			$ticket->set_theme(db()->nomysqlinj($_REQUEST['theme']));
			$ticket->set_user_id($user->get_id());
			$ticket->set_game_id(0);
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
			$json['success'] = true;
			$json['msg'] = 'Тикет успешно создан';
		} else {
			$json['error'] = 'Вы не заполнили все поля';
		}
	} else {
		$json['error'] = 'Вы не авторизовались на сайте';
	}
	echo_json($json);
}
