<?php

add_admin_get('/opencase/bots/(([0-9]+)/)?', 'admin_opencase_bots');
add_admin_get('/opencase/bot/([0-9]+)/', 'admin_opencase_bot');
add_admin_get('/opencase/botaddform/', 'admin_opencase_botaddform');
add_admin_post('/opencase/botadd/', 'admin_opencase_botadd');
add_admin_get('/opencase/boteditform/([0-9]+)/', 'admin_opencase_boteditform');
add_admin_post('/opencase/botedit/([0-9]+)/', 'admin_opencase_botedit');
add_admin_get('/opencase/botdelete/([0-9]+)/', 'admin_opencase_botdelete');
add_admin_get('/opencase/botitems/(([0-9]+)/)?', 'admin_opencase_botitems');
add_admin_post('/opencase/botitemsearch/', 'admin_opencase_botitemsearch');
add_admin_get('/opencase/updateinv/([0-9]+)/', 'admin_opencase_updateinv');
add_admin_post('/opencase/boteventadd/bot/([0-9]+)/', 'admin_opencase_boteventadd');
add_admin_post('/opencase/boteventadd/botitems/', 'admin_opencase_botitemseventadd');
add_admin_get('/opencase/botevents/(([0-9]+)/)?', 'admin_opencase_botevents');
add_admin_get('/opencase/boteventeditform/([0-9]+)/', 'admin_opencase_boteventeditform');
add_admin_post('/opencase/boteventedit/([0-9]+)/', 'admin_opencase_boteventedit');
add_admin_get('/opencase/boteventrepeat/([0-9]+)/', 'admin_opencase_boteventrepeat');

function admin_opencase_bots($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$botcount = db()->query_once('select count(id) from opencase_bot');
	$pages = new Pages();
	$pages->set_num_object($botcount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/bots/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/bots/');
	$pages->set_curent_page($page);
	$bot = new bot();
	$allbots = $bot->get_bots('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Имя</th>
									<th>Steam ID</th>
									<th>Статус</th>
									<th>Включен</th>
									<th>Маркет</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allbots as $value) {
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td>' . $value->get_name() . '</td>
					<td>' . $value->get_steam_id() . '</td>
					<td>' . $value->get_label_status() . '</td>
					<td>' . $value->get_label_enabled() . '</td>
					<td>' . $value->get_label_market_enable() . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/bot/' . $value->get_id() . '/" title="Просмотреть"><i class = "fa fa-eye"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/boteditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/botdelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/botaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить бота</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/deleteConfirm/deleteConfirm.js', 10, 'footer');
	set_active_admin_menu('bots');
	set_title('Упрвление ботами');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_bot($args) {
	$invItems = new invItems();
	$bot = new bot($args[0]);
	$allinvItems = $invItems->get_invItemss('bot_id = "' . $bot->get_id() . '" and status = 0', 'price DESC, name ASC');
	$botEvent = new botEvent();
	$eventSelect = '';
	foreach ($botEvent->get_array_event() as $key => $event) {
		if ($key < 50)
			$eventSelect .= '<option value = "' . $key . '">' . $event . '</option>';
	}
	$sum = 0;
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-header with-border">
						<h3 class = "box-title">Информация о боте</h3>
					</div>
					<div class="box-body">
						<table class = "table table-striped">
							<tr>
								<th>Имя бота</th>
								<td><a href = "https://steamcommunity.com/profiles/' . $bot->get_steam_id() . '/" target = "_blank">' . $bot->get_name() . '</a></td>
							</tr>
							<tr>
								<th>Steam ID</th>
								<td>' . $bot->get_steam_id() . '</td>
							</tr>
							<tr>
								<th>Включен</th>
								<td>' . $bot->get_label_enabled() . '</td>
							</tr>
							<tr>
								<th>Статус</th>
								<td>' . $bot->get_label_status() . '</td>
							</tr>
							<tr>
								<th>Ссылка на обмен</th>
								<td><a href = "' . $bot->get_offer_url() . '" target = "_blank">' . $bot->get_offer_url() . '</a></td>
							</tr>
							<tr>
								<th>Количество предметов</th>
								<td>' . count($allinvItems) . '</td>
							</tr>
							<tr>
								<th>Маркет</th>
								<td>' . $bot->get_label_market_enable() . '</td>
							</tr>
						</table>
					</div>
					<div class = "box-footer">
						<a href = "' .ADMINURL . '/opencase/boteditform/' . $bot->get_id() . '/" class = "btn btn-success"><i class = "fa fa-pencil"></i> Редактировать бота</a>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<form class="add-bot-event" action = "' .ADMINURL . '/opencase/boteventadd/bot/' . $bot->get_id() . '/" method = "POST">
						<div class="box-header with-border">
							<h3 class = "box-title">Инвентарь бота</h3>
						</div>
						<div class="box-header with-border">
							<div class = "row">
								<div class = "col-md-4">
									<select id = "event" name = "event" class = "form-control">
										<option value = "0">Выберите действие</option>
										' . $eventSelect . '
									</select>
								</div>
								<div class = "col-md-4">
									<input type = "text" name = "additional" value = "" placeholder = "Дополнительный параметр" class = "form-control">
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-success"><i class = "fa fa-play"></i> Выполнить</button>
								</div>
								<div class = "col-md-2">
									<a href = "' .ADMINURL . '/opencase/updateinv/' . $bot->get_id() . '/" class = "btn btn-primary pull-right"><i class = "fa fa-refresh"></i> Обновить инвентарь</a>
								</div>
							</div>
						</div>
						<div class="box-body">
							<div class = "row">
						';
	$where = '';
	foreach ($allinvItems as $item) {
		$content .= $item->get_html_item();
		$sum += $item->get_price();
	}
	$content .= '
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/invItems/invItems.js', 10, 'footer');
	add_css(get_admin_template_folder() . '/plugins/invItems/invItems.css');
	add_breadcrumb('Упрвление ботами', ADMINURL . '/opencase/bots/', 'fa-cog');
	set_active_admin_menu('bots');
	set_title('Просмотр бота №' . $bot->get_id());
	set_content($content);
	set_tpl('index.php');
	add_bot_event_js();
}

function admin_opencase_botaddform() {
	$bot = new bot();
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/botadd/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя бота: </label>
								<input type = "text" class="form-control" name="name" id="name">
							</div>
							<div class="form-group">
								<label for="steam_id">Steam ID: </label>
								<input type = "text" class="form-control" name="steam_id" id="steam_id">
							</div>
							<div class="form-group">
								<label for="password">Пароль: </label>
								<input type = "password" class="form-control" name="password" id="password">
							</div>
							<div class="form-group">
								<label for="shared_secret">Shared Secret: </label>
								<input type = "password" class="form-control" name="shared_secret" id="shared_secret">
							</div>
							<div class="form-group">
								<label for="identity_secret">Identity Secret: </label>
								<input type = "password" class="form-control" name="identity_secret" id="identity_secret">
							</div>
							<div class="form-group">
								<label for="api_key">API Key: </label>
								<input type = "password" class="form-control" name="api_key" id="api_key">
							</div>
							<div class="form-group">
								<label for="enabled">Включен: </label>
								<select id = "enabled" name = "enabled" class = "form-control">
									<option value = "1">Включен</option>
									<option value = "0">Отключен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="offer_url">Трейдоффер URL: </label>
								<input type = "text" class="form-control" name="offer_url" id="offer_url">
							</div>
							<div class="form-group">
								<label for="market_enable">Маркет: </label>
								<select id = "market_enable" name = "market_enable" class = "form-control">
									<option value = "0">Отключен</option>
									<option value = "1">Включен</option>									
								</select>
							</div>
							<div class="form-group">
								<label for="market_key">Маркет API ключ: </label>
								<input type = "password" class="form-control" name="market_key" id="market_key">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить бота</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('botadd');
	add_breadcrumb('Упрвление ботами', ADMINURL . '/opencase/bots/', 'fa-cog');
	set_title('Добавление бота');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_botadd() {
	if ($_POST['name'] != '') {
		$warning = '';
		$bot = new bot();
		$bot->set_parametrs_from_request();
		if ($bot->get_market_enable()) {
			if (empty($bot->get_decrypted_market_key()) || !check_market_api_key($bot->get_decrypted_market_key())) {
				$bot->set_market_enable(0);
				$warning = 'Указан некорректный ключ для API маркета, поэтому маркет выключен';
			}
		}
		$bot->add_bot();
		if (!empty($warning)) {
			alertW('Бот успешно добавлен. ' . $warning, ADMINURL . '/opencase/bots/');
		} else {
			alertS('Бот успешно добавлен', ADMINURL . '/opencase/bots/');
		}
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/opencase/botaddform/');
	}
}

function admin_opencase_boteditform($args) {
	$bot = new bot($args[0]);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/botedit/' . $bot->get_id() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя бота: </label>
								<input type = "text" class="form-control" name="name" id="name" value = "' . $bot->get_name() . '">
							</div>
							<div class="form-group">
								<label for="steam_id">Steam ID: </label>
								<input type = "text" class="form-control" name="steam_id" id="steam_id" value = "' . $bot->get_steam_id() . '">
							</div>
							<div class="form-group">
								<label for="password">Пароль: </label>
								<input type = "password" class="form-control" name="password" id="password" value = "' . $bot->get_encrypted_data_input_text($bot->get_password()) . '">
							</div>
							<div class="form-group">
								<label for="shared_secret">Shared Secret: </label>
								<input type = "password" class="form-control" name="shared_secret" id="shared_secret" value = "' . $bot->get_encrypted_data_input_text($bot->get_shared_secret()) . '">
							</div>
							<div class="form-group">
								<label for="identity_secret">Identity Secret: </label>
								<input type = "password" class="form-control" name="identity_secret" id="identity_secret" value = "' . $bot->get_encrypted_data_input_text($bot->get_identity_secret()) . '">
							</div>
							<div class="form-group">
								<label for="api_key">API Key: </label>
								<input type = "password" class="form-control" name="api_key" id="api_key" value = "' . $bot->get_encrypted_data_input_text($bot->get_api_key()) . '">
							</div>
							<div class="form-group">
								<label for="enabled">Включен: </label>
								<select id = "enabled" name = "enabled" class = "form-control">
									<option value = "1"' . ($bot->get_enabled() ? ' selected = "selected"' : '') . '>Включен</option>
									<option value = "0"' . ($bot->get_enabled() ? '' : ' selected = "selected"') . '>Отключен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="offer_url">Трейдоффер URL: </label>
								<input type = "text" class="form-control" name="offer_url" id="offer_url" value = "' . $bot->get_offer_url() . '">
							</div>
							<div class="form-group">
								<label for="market_enable">Маркет: </label>
								<select id = "market_enable" name = "market_enable" class = "form-control">
									<option value = "0"' . ($bot->get_market_enable() ? '' : ' selected = "selected"') . '>Отключен</option>
									<option value = "1"' . ($bot->get_market_enable() ? ' selected = "selected"' : '') . '>Включен</option>									
								</select>
							</div>
							<div class="form-group">
								<label for="market_key">Маркет API ключ: </label>
								<input type = "password" class="form-control" name="market_key" id="market_key" value = "' . $bot->get_encrypted_data_input_text($bot->get_market_key()) . '">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
							<a href = "' .ADMINURL . '/opencase/bot/' . $bot->get_id() . '/" class = "btn btn-primary"><i class = "fa fa-eye"></i> Просмотр бота</a>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('bots');
	add_breadcrumb('Упрвление ботами', ADMINURL . '/opencase/bots/', 'fa-cog');
	set_title('Редактирование бота');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_botedit($args) {
	$bot = new bot($args[0]);
	if ($_POST['name'] != '') {
		$warning = '';
		$bot->set_parametrs_from_request();
		if ($bot->get_market_enable()) {
			if (empty($bot->get_decrypted_market_key()) || !check_market_api_key($bot->get_decrypted_market_key())) {
				$bot->set_market_enable(0);
				$warning = 'Указан некорректный ключ для API маркета, поэтому маркет выключен';
			}
		}
		$bot->update_bot();
		if (!empty($warning)) {
			alertW('Изменения успешно сохранены. ' . $warning, ADMINURL . '/opencase/boteditform/' . $bot->get_id() . '/');
		} else {
			alertS('Изменения успешно сохранены', ADMINURL . '/opencase/boteditform/' . $bot->get_id() . '/');
		}
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/opencase/boteditform/' . $bot->get_id() . '/');
	}
}

function admin_opencase_botdelete($args) {
	$bot = new bot($args[0]);
	$bot->delete_bot();
	alertS('Бот успешно удален', ADMINURL . '/opencase/bots/');
}

function admin_opencase_botitems($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$botitemscount = db()->query_once('select count(id) from opencase_invitems');
	$pages = new Pages();
	$pages->set_num_object($botitemscount['count(id)']);
	$pages->set_object_in_page(120);
	$pages->set_format_url(ADMINURL . '/opencase/botitems/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/botitems/');
	$pages->set_curent_page($page);
	$invItems = new invItems();
	$allinvItems = $invItems->get_invItemss('status = 0', 'price DESC, name ASC', (($page - 1) * 120) . ', 120');
	$bots = new bot();
	$bots = $bots->get_bots('', 'id DESC');
	$botSelect = '<option value = "0">Выберите бота</option>';
	foreach ($bots as $bot) {
		$botSelect .= '<option value = "' . $bot->get_id() . '">Бот №' . $bot->get_id() . ' (' . $bot->get_name() . ')</option>';
	}
	$botEvent = new botEvent();
	$eventSelect = '';
	foreach ($botEvent->get_array_event() as $key => $event) {
		if ($key < 50)
			$eventSelect .= '<option value = "' . $key . '">' . $event . '</option>';
	}
	$sum = db()->query_once('select sum(price) from opencase_invitems');
	$sum = $sum['sum(price)'];
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/botitemsearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-5">
									<input type = "text" name = "name" value = "' . (isset($_POST['name']) ? $_POST['name'] : '') . '" placeholder = "Название предмета" class = "form-control">
								</div>
								<div class = "col-md-5">
									<select id = "bot_id" name = "bot_id" class = "form-control">
										' . $botSelect . '
									</select>
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-primary pull-right"><i class = "fa fa-search"></i> Поиск</button>
								</div>
							</div>
						</form>
					</div>
					<form class="add-bot-event" action = "' .ADMINURL . '/opencase/boteventadd/botitems/" method = "POST">
						<div class="box-header with-border">
							<div class = "row">
								<div class = "col-md-4">
									<select id = "event" name = "event" class = "form-control">
										<option value = "0">Выберите действие</option>
										' . $eventSelect . '
									</select>
								</div>
								<div class = "col-md-4">
									<input type = "text" name = "additional" value = "" placeholder = "Дополнительный параметр" class = "form-control">
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-success"><i class = "fa fa-play"></i> Выполнить</button>
								</div>
							</div>
						</div>
						<div class="box-body">
							<div class = "row">
						';
	foreach ($allinvItems as $item) {
		$content .= $item->get_html_item();
	}
	$content .= '
							</div>
						</div>
						
						<div class = "box-footer">
							<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
						</div>
					</from>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/invItems/invItems.js', 10, 'footer');
	add_css(get_admin_template_folder() . '/plugins/invItems/invItems.css');
	set_active_admin_menu('botistems');
	set_title('Инвентарь ботов');
	set_content($content);
	set_tpl('index.php');
	add_bot_event_js();
}

function admin_opencase_botitemsearch() {
	if ($_POST['name'] == '' && ($_POST['bot_id'] == '' || $_POST['bot_id'] == 0))
		redirect_srv_msg('', ADMINURL . '/opencase/botitems/');
	$invItems = new invItems();
	$bots = new bot();
	$bots = $bots->get_bots('', 'id DESC');
	$botSelect = '<option value = "0">Выберите бота</option>';
	foreach ($bots as $bot) {
		$botSelect .= '<option value = "' . $bot->get_id() . '"' . (isset($_POST['bot_id']) && $_POST['bot_id'] != '0' && $_POST['bot_id'] == $bot->get_id() ? ' selected = "selected"' : '') . '>Бот №' . $bot->get_id() . ' (' . $bot->get_name() . ')</option>';
	}
	$botEvent = new botEvent();
	$eventSelect = '';
	foreach ($botEvent->get_array_event() as $key => $event) {
		if ($key < 50)
			$eventSelect .= '<option value = "' . $key . '">' . $event . '</option>';
	}
	$sum = 0;
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/botitemsearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-5">
									<input type = "text" name = "name" value = "' . (isset($_POST['name']) ? $_POST['name'] : '') . '" placeholder = "Название предмета" class = "form-control">
								</div>
								<div class = "col-md-5">
									<select id = "bot_id" name = "bot_id" class = "form-control">
										' . $botSelect . '
									</select>
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-primary pull-right"><i class = "fa fa-search"></i> Поиск</button>
								</div>
							</div>
						</form>
					</div>
					<form class="add-bot-event" action = "' .ADMINURL . '/opencase/boteventadd/botitems/" method = "POST">
						<div class="box-header with-border">
							<div class = "row">
								<div class = "col-md-4">
									<select id = "event" name = "event" class = "form-control">
										<option value = "0">Выберите действие</option>
										' . $eventSelect . '
									</select>
								</div>
								<div class = "col-md-4">
									<input type = "text" name = "additional" value = "" placeholder = "Дополнительный параметр" class = "form-control">
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-success"><i class = "fa fa-play"></i> Выполнить</button>
								</div>
							</div>
						</div>
						<div class="box-body">
							<div class = "row">
						';
	$where = '';
	if (isset($_POST['name']) && $_POST['name'] != '') {
		$where .= 'market_hash_name like "%' . db()->nomysqlinj(trim($_POST['name'])) . '%"';
	}
	if (isset($_POST['bot_id']) && $_POST['bot_id'] != '0') {
		$where .= (strlen($where) > 0 ? ' and ' : '') . 'bot_id = "' . db()->nomysqlinj($_POST['bot_id']) . '"';
	}
	if (strlen($where) == 0) {
		$where = '1 = 0';
	}
	$allinvItems = $invItems->get_invItemss($where, 'price DESC, name ASC');
	foreach ($allinvItems as $item) {
		$content .= $item->get_html_item();
		$sum += $item->get_price();
	}
	$content .= '
							</div>
						</div>
					</form>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/invItems/invItems.js', 10, 'footer');
	add_css(get_admin_template_folder() . '/plugins/invItems/invItems.css');
	set_active_admin_menu('botistems');
	set_title('Инвентарь ботов');
	set_content($content);
	set_tpl('index.php');
	add_bot_event_js();
}

function admin_opencase_updateinv($args) {
	$bot = new bot($args[0]);
	if ($bot->update_inventory_from_steam()) {
		alertS('Инвентарь успешно обновлен', ADMINURL . '/opencase/bot/' . $bot->get_id() . '/');
	} else {
		alertE('Не удалось обновить инвентарь бота', ADMINURL . '/opencase/bot/' . $bot->get_id() . '/');
	}
}

function admin_opencase_boteventadd($args) {
	$url = 'bot/' . $args[0];
	if ($_POST['event'] > 0) {
		$bot = new bot($args[0]);
		$botEvent = new botEvent();
		$botEvent->set_parametrs_from_request();
		if ($botEvent->get_event() == 1) {
			$itemsNames = [];
			$invItems = [];
			foreach ($_POST['items'] as $item) {
				$invItem = new invItems($item);
				if ($invItem->get_status() != 0) {
					alertE('Не удалось добавит задачу. Один или несколько из предметов уже используются', ADMINURL . '/opencase/' . $url . '/');
				} elseif (!$invItem->get_tradable()) {
					alertE('Не удалось добавит задачу. Один или несколько из предметов не доступны для трейда в стим', ADMINURL . '/opencase/' . $url . '/');
				}
				$invItems[] = $invItem;
			}
			foreach ($invItems as $invItem) {
				$invItem->set_status(1);
				$invItem->update_invItems();
				$itemsNames[] = $invItem->get_market_hash_name();
			}
			$additional = array(
				'msg' => '',
				'tradeUrl' => $botEvent->get_additional(),
				'ditem' => '',
				'appid' => get_setval('opencase_gameid'),
				'itemName' => implode(', ', $itemsNames)
			);
			$botEvent->set_additional(json_encode($additional));
		}
		$botEvent->set_bot_id($bot->get_id());
		$botEvent->set_items_id(implode(',', $_POST['items']));
		$botEvent->add_botEvent();
		alertS('Задача добавленна в очередь на выполнение', ADMINURL . '/opencase/' . $url . '/');
	} else {
		alertE('Не выбрана задача для выполнения', ADMINURL . '/opencase/' . $url . '/');
	}
}

function admin_opencase_botitemseventadd() {
	if ($_POST['event'] > 0) {
		$bots = array();
		$itemsNames = [];
		$invItems = [];
		foreach ($_POST['items'] as $item) {
			$invItem = new invItems($item);
			if ($invItem->get_status() != 0) {
				alertE('Не удалось добавит задачу. Один или несколько из предметов уже помечены для вывода', ADMINURL . '/opencase/botitems/');
			} elseif (!$invItem->get_tradable()) {
				alertE('Не удалось добавит задачу. Один или несколько из предметов не доступны для трейда в стим', ADMINURL . '/opencase/botitems/');
			}
			$invItems[] = $invItem;
		}
		foreach ($invItems as $invItem) {
			$invItem->set_status(1);
			$invItem->update_invItems();
			$bots[$invItem->get_bot_id()][] = $item;
			$itemsNames[] = $invItem->get_market_hash_name();
		}
		foreach ($bots as $key => $bot_items) {
			$bot = new bot($key);
			$botEvent = new botEvent();
			$botEvent->set_parametrs_from_request();
			if ($botEvent->get_event() == 1) {
				$additional = array(
					'msg' => '',
					'tradeUrl' => $botEvent->get_additional(),
					'ditem' => '',
					'appid' => get_setval('opencase_gameid'),
					'itemName' => implode(', ', $itemsNames)
				);
				$botEvent->set_additional(json_encode($additional));
			}
			$botEvent->set_bot_id($bot->get_id());
			$botEvent->set_items_id(implode(',', $bot_items));
			$botEvent->add_botEvent();
		}
		alertS('Задача добавленна в очередь на выполнение', ADMINURL . '/opencase/botitems/');
	} else {
		alertE('Не выбрана задача для выполнения', ADMINURL . '/opencase/botitems/');
	}
}

function admin_opencase_botevents($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$botEventCount = db()->query_once('select count(id) from opencase_botevents');
	$pages = new Pages();
	$pages->set_num_object($botEventCount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/botevents/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/botevents/');
	$pages->set_curent_page($page);
	$botEvent = new botEvent();
	$allbotEvents = $botEvent->get_botEvents('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Бот</th>
									<th>Задача</th>
									<th>Пользователь</th>
									<th>Предмет</th>
									<th>Статус</th>
									<th>Время создания</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allbotEvents as $value) {
		$addition = $value->get_parsed_additional();
		$dItem = false;
		if (!empty($addition->ditem)) {
			$dItem = new droppedItem($addition->ditem);
		}
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td><a href = "' .ADMINURL . '/opencase/bot/' . $value->get_bot_id() . '/">' . $value->get_bot_class()->get_name() . '</a></td>
					<td>' . $value->get_text_event() . '</td>
					<td>' . ($dItem ? '<a href = "' .ADMINURL . '/opencase/user/' . $dItem->get_user_class()->get_id() . '/">' . $dItem->get_user_class()->get_name() . '</a>' : (!empty($addition->tradeUrl) ? ('<a href="' . $addition->tradeUrl . '">По ссылке</a>') : 'Неизвестно')) . '</td>
					<td>' . ($dItem ? $dItem->get_item_name_alt() : (!empty($addition->itemName) ? $addition->itemName : 'Неизвестно')) . '</td>
					<td>' . $value->get_label_status() . '</td>
					<td>' . $value->get_format_time_add() . '</td>
					<td>
						' . ($value->get_status() == 3 ?
				'<a href="' .ADMINURL . '/opencase/boteventeditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>' :
				'') . '
					</td>
					<td>
						' . ($value->get_status() == 3 ?
				'<a href="' .ADMINURL . '/opencase/boteventrepeat/' . $value->get_id() . '/" title="Повторить"><i class = "fa fa-repeat"></i></a>' :
				'<i class = "fa fa-chevron-down" title = "Выполненно"></i>') . '
					</td>
				</tr>
			';
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
	set_active_admin_menu('botevents');
	set_title('Задачи ботов');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_boteventeditform($args) {
	$botEvent = new botEvent($args[0]);
	$additionals = (array) $botEvent->get_parsed_additional();
	$bots = new bot();
	$bots = $bots->get_bots();
	$events = $botEvent->get_array_event();
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/boteventedit/' . $botEvent->get_id() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="bot_id">Бот: </label>
								<select name = "bot_id" id = "bot_id" class="form-control">';
	foreach ($bots as $bot) {
		$content .= '<option value = "' . $bot->get_id() . '"' . ($bot->get_id() == $botEvent->get_bot_id() ? ' selected = "selected"' : '') . '>' . $bot->get_name() . '</option>';
	}
	$content .= '			</select>
							</div>
							<div class="form-group">
								<label for="event">Задача: </label>
								<select name = "event" id = "event" class="form-control">';
	foreach ($events as $key => $event) {
		$content .= '<option value = "' . $key . '"' . ($key == $botEvent->get_event() ? ' selected = "selected"' : '') . '>' . $event . '</option>';
	}
	$content .= '			</select>
							</div>';
	foreach ($additionals as $key => $addition) {
		$content .= '
									<div class="form-group">
										<label for="' . $key . '">' . $key . ': </label>
										<input type = "text" class="form-control" name="additional[' . $key . ']" id="' . $key . '" value = "' . $addition . '">
									</div>
								';
	}
	$content .= '		<div class="form-group">
								<label for="items_id">ID предметов: </label>
								<input type = "text" class="form-control" name="items_id" id="items_id" value = "' . $botEvent->get_items_id() . '">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('botevents');
	set_title('Редактирование задачи');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_boteventedit($args) {
	$botEvent = new botEvent($args[0]);
	$_REQUEST['additional'] = json_encode($_REQUEST['additional']);
	$botEvent->set_parametrs_from_request();
	$botEvent->update_botEvent();
	alertS('Изменения успешно сохранены', ADMINURL . '/opencase/boteventeditform/' . $botEvent->get_id() . '/');
}

function admin_opencase_boteventrepeat($args) {
	if (isset($args[0])) {
		$botEvent = new botEvent($args[0]);
		if ($botEvent->get_status() == 3) {
			$botEvent->set_status(0);
			$botEvent->set_iteration(0);
			$botEvent->update_botEvent();
			$addition = $botEvent->get_parsed_additional();
			if (!empty($addition->ditem)) {
				$dItem = new droppedItem($addition->ditem);
				if ($dItem->get_id() != '') {
					$dItem->set_status(1);
					$dItem->update_droppedItem();
				}
			}
			alertS('Задание поставлено в очередь на повторное выполнение', ADMINURL . '/opencase/botevents/');
		} else {
			alertE('Это задание уже выполнено. Его нельзя выполнить повторно', ADMINURL . '/opencase/botevents/');
		}
	} else {
		alertE('Не удалось найти задачу для повторного выполнения задания', ADMINURL . '/opencase/botevents/');
	}
}

function add_bot_event_js() {
	add_jscript(
			'﻿$(document).ready(function() {
			$(".add-bot-event [name =\'event\']").on("change", function () {
				if ($(this).val() == 1) {
					$(this).parents(".add-bot-event").find("[name =\'additional\']").attr("placeholder", "Trade-ссылка");
				} else {
					$(this).parents(".add-bot-event").find("[name =\'additional\']").attr("placeholder", "Дополнительный параметр");
				}
			});
		});'
	);
}
