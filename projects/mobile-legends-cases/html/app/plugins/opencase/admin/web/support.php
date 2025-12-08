<?php

add_admin_get('/support/(([0-9]+)/)?', 'admin_support_index');
add_admin_get('/support/view/(([0-9]+)/)?', 'admin_support_view');
add_admin_get('/support/admins/(([0-9]+)/)?', 'admin_support_admins');
add_admin_get('/support/active/(([0-9]+)/)?', 'admin_support_active');
add_admin_get('/support/close/(([0-9]+)/)?', 'admin_support_close');
add_admin_get('/support/ticket/([0-9]+)/', 'admin_support_ticket');
add_admin_get('/support/closeticket/([0-9]+)/', 'admin_support_closeticket');
add_admin_get('/support/openticket/([0-9]+)/', 'admin_support_openticket');
add_admin_post('/support/answer/([0-9]+)/', 'admin_support_answer');

function admin_support_index($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	admin_support_generate_page('', $page);
}

function admin_support_view($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	admin_support_generate_page('/view', $page, 'status = 1');
	set_active_admin_menu('supportview');
}

function admin_support_admins($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	admin_support_generate_page('/admins', $page, 'status = 7');
	set_active_admin_menu('supportadmins');
}

function admin_support_active($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	admin_support_generate_page('/active', $page, 'status = 2 or status = 3 or status = 8');
	set_active_admin_menu('supportactive');
}

function admin_support_close($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	admin_support_generate_page('/close', $page, 'status = 5 or status = 6');
	set_active_admin_menu('supportclose');
}

function admin_support_generate_page($suburi, $page, $where = '') {
	if ($where == '') {
		$where = 'status = 0 or status = 4';
	}
	$tiketCount = db()->query_once('select count(id) from ticket where ' . $where);
	$pages = new Pages();
	$pages->set_num_object($tiketCount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/support' . $suburi . '/{p}/');
	$pages->set_first_url(ADMINURL . '/support' . $suburi . '/');
	$pages->set_curent_page($page);
	$tikets = new ticket();
	$tikets = $tikets->get_tickets_with_message($where, ' ticket_message.time_add DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class = "row">
			<div class = "col-xs-12">
				<div class = "box">
					<div class = "box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Пользователь</th>
									<th>Тема</th>
									<th>Статус</th>
									<th>Дата подачи</th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
						';
	if (is_array($tikets)) {
		foreach ($tikets as $ticket) {
			$content .= ' 
									<tr> 
										<td>' . $ticket->get_id() . '</td>
										<td><a href = "' .ADMINURL . '/opencase/user/' . $ticket->get_user_class()->get_id() . '/">' . $ticket->get_user_class()->get_name() . '</a></td>
										<td>' . $ticket->get_theme() . '</td>
										<td>' . $ticket->get_admin_status_text() . '</td>
										<td>' . $ticket->get_first_message()->get_form_time_add('d.m.Y H:i') . '</td>
										<td>	
											<a href="' .ADMINURL . '/support/ticket/' . $ticket->get_id() . '/" title="Просмотреть"><i class = "fa fa-eye"></i></a>
										</td>
									</tr>
								';
		}
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	if ($where == 'status = 0 or status = 4')
		set_active_admin_menu('support');
	set_title('Тех. поддержка');
	set_content($content);
	set_tpl('index.php');
}

function admin_support_ticket($args) {
	$ticketid = $args[0];
	$ticket = new ticket($ticketid);
	$user = $ticket->get_user_class();
	$content = '
		<div class = "row">
			<div class = "col-md-12">
				<div class = "box">
					<div class = "box-body">
						<div class = "row">
							<div class = "col-md-2">
								<img src = "' . $user->get_data('image') . '" alt = "Аватар" class = "img-responsive" style = "margin: 0 auto; padding: 10px 10%;">
							</div>
							<div class = "col-md-10">
								<div class = "table-responsive">
									<div class = "box-body">
										<table class = "table table-striped">
											<tr>
												<th>Пользователь: </th> <td><a href = "/opencase/user/' . $user->get_id() . '/">' . $user->get_name() . '</a></td>
											</tr>
											<tr>
												<th>Тема: </th> <td>' . $ticket->get_theme() . '</td>
											</tr>
											<tr>
												<th>Статус</th> <td>' . $ticket->get_admin_status_text() . '</td>
											</tr>
											<tr>
												<th>Дата создания:</th> <td>' . $ticket->get_first_message()->get_form_time_add('d.m.Y H:i') . '</td>
											</tr>
											<tr>
												<th>Ссылка на обмен:</th> <td><a href = "' . $user->get_data('trade_link') . '" target = "_blank">' . $user->get_data('trade_link') . '</a></td>
											</tr>
										</table>
									</div>
								</div>
							</div>	
						</div>	
					</div>	
				</div>
			</div>
		</div>
		';
	foreach ($ticket->get_messages() as $message) {
		$attach = '';
		$attachments = $message->get_attachments();
		if (is_array($attachments) && count($attachments) > 0) {
			$attach .= '<div class = "attachment_place clearfix">';
			foreach ($attachments as $file) {
				$attach .= '<a href = "/uploads/' . $file . '" target = "_blank"><img src = "/uploads/' . $file . '" alt = "' . $file . '" height = "75px"></a>';
			}
			$attach .= '</div>';
		}
		$ansAdmin = new admin($message->get_from());
		$content .= '
			<div class = "row">
				<div class = "col-xs-12">
					<div class = "box">
						<div class = "box-header with-border">
							<div class = "name pull-left">' . ($message->get_from() ? '<a href = "' .ADMINURL . '/admins/editform/' . $ansAdmin->get_id() . '/">' . $ansAdmin->get_name() . '</a>' : '<a href = "' .ADMINURL . '/opencase/user/' . $ticket->get_user_class()->get_id() . '/">' . $ticket->get_user_class()->get_name() . '</a>') . '</div>
							<div class = "date pull-right">' . $message->get_form_time_add('d.m.Y H:i') . '</div>
						</div>
						<div class = "box-body">
							' . str_replace(['\\\r', '\\\n'], ['', '<br>'], $message->get_text()) . '
							' . $attach . '
						</div>
					</div>
				</div>
			</div>
			';
	}
	$content .= '
		<div class = "row">
			<div class = "col-xs-12">
				<div class = "box">
					<form method = "post" action = "' .ADMINURL . '/support/answer/' . $ticket->get_id() . '/" enctype="multipart/form-data">
						<div class = "box-header with-border">
							Текст ответа:
						</div>
						<div class = "box-body">
							<div class = "form-group">
								<textarea name = "text" id = "text" class = "form-control" style = "height: 120px"></textarea>
							</div>
							<p>Шаболны ответов: </p>
							<p class = "template_q"><a href = "#">Здравствуйте, выигрыш отправлен повторно</a></p>
							<p class = "template_q"><a href = "#">Всегда пожалуйста, рад был помочь</a></p>
							<input type = "file" name = "attachments[]" class = "attachment_input" multiple accept="image/jpeg,image/png">
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-pencil"></i> Добавить ответ</button>
		';

	$content .= '';
	if ($ticket->get_status() != 5 && $ticket->get_status() != 6)
		$content .= ' <a class="btn btn-primary" href = "' .ADMINURL . '/support/closeticket/' . $ticketid . '/">Закрыть заявку</a>';
	else
		$content .= ' <a class="btn btn-primary" href = "' .ADMINURL . '/support/openticket/' . $ticketid . '/">Открыть заявку</a>';
	$content .= '
						</div>
					</form>
				</div>
			</div>
		</div>';
	if ($ticket->get_status() == 4 || $ticket->get_status() == 0) {
		$ticket->set_status(1);
		$ticket->update_ticket();
	}
	add_jscript('
		$(document).on("click", ".template_q a", function() {
			$("#text").val($(this).html());
			return false;
		});');
	if ($ticket->get_status() == 4 || $ticket->get_status() == 0)
		set_active_admin_menu('support');
	else if ($ticket->get_status() == 1)
		set_active_admin_menu('supportview');
	else if ($ticket->get_status() == 7)
		set_active_admin_menu('supportadmins');
	else if ($ticket->get_status() == 5 || $ticket->get_status() == 6)
		set_active_admin_menu('supportclose');
	else if ($ticket->get_status() == 2 || $ticket->get_status() == 3 || $ticket->get_status() == 8)
		set_active_admin_menu('supportactive');
	add_breadcrumb('Тех. поддержка', ADMINURL . '/support/', 'fa-warning');
	set_title('Просмотр заявки №' . $ticketid);
	set_content($content);
	set_tpl('index.php');
}

function admin_support_closeticket($args) {
	$ticket = new ticket($args[0]);
	$ticket->set_status(5);
	$ticket->update_ticket();
	alertS('Заявка успешно закрыта', ADMINURL . '/support/ticket/' . $ticket->get_id() . '/');
}

function admin_support_openticket($args) {
	$ticket = new ticket($args[0]);
	$ticket->set_status(2);
	$ticket->update_ticket();
	alertS('Заявка успешно открыта', ADMINURL . '/support/ticket/' . $ticket->get_id() . '/');
}

function admin_support_answer($args) {
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
	$ticket = new ticket($args[0]);
	$ticket->set_status(3);
	$ticket->update_ticket();
	$message = new ticket_message();
	$message->set_ticket_id($ticket->get_id());
	$message->set_text($_POST['text']);
	$message->set_attachment($attachment);
	$message->set_from(user()->get_id());
	$message->add_ticket_message();
	redirect_srv_msg('<div class="n_ok"><p>Ваш ответ успешно добавлен</p></div>', ADMINURL . '/support/ticket/' . $ticket->get_id() . '/');
	exit();
}
