<?php

add_admin_get('/opencase/users/(([0-9]+)/)?', 'admin_opencase_users');
add_admin_app('/opencase/usersearch/', 'admin_opencase_usersearch');
add_admin_get('/opencase/user/([0-9]+)/', 'admin_opencase_user');
add_admin_get('/opencase/useraddform/', 'admin_opencase_useraddform');
add_admin_post('/opencase/useradd/', 'admin_opencase_useradd');
add_admin_get('/opencase/usereditform/([0-9]+)/', 'admin_opencase_usereditform');
add_admin_post('/opencase/useredit/([0-9]+)/', 'admin_opencase_useredit');
add_admin_get('/opencase/userdelete/([0-9]+)/', 'admin_opencase_userdelete');
add_admin_get('/opencase/fakeopen/', 'admin_opencase_fakeopen');
add_admin_app('/opencase/fakestart/', 'admin_opencase_fakestart');

function admin_opencase_users($args) {
    $page = isset($args[1]) ? $args[1] : 1;
    $usercount = db()->query_once('select count(id) from users');
    $pages = new Pages();
    $pages->set_num_object($usercount['count(id)']);
    $pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
    $pages->set_format_url(ADMINURL . '/opencase/users/{p}/');
    $pages->set_first_url(ADMINURL . '/opencase/users/');
    $pages->set_curent_page($page);
    $user = new user();
    $allusers = $user->get_users('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/usersearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-10">
									<input type = "text" name = "search" value = "" placeholder = "SteamID или имя пользователя" class = "form-control">
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-primary pull-right"><i class = "fa fa-search"></i> Поиск</button>
								</div>
							</div>
						</form>
					</div>
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Аватар</th>
									<th>Имя</th>
									<th>Steam ID</th>
									<th>VK ID</th>
									<th>Баланс</th>
									<th>Открыто кейсов</th>
									<th>Контракты</th>
									<th>Статус</th>
									<th>Бан</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
    foreach ($allusers as $value) {
        $content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td><img src = "' . $value->get_data('image') . '" width = "30px"></td>
					<td>' . $value->get_name() . '</td>
					<td>' . $value->get_data('steam_id') . '</td>
					<td>' . $value->get_data('vk_id') . '</td>
					<td>' . get_user_balance($value) . '</td>
					<td>' . get_user_count_cases($value) . '</td>
					<td>' . get_user_count_contracts($value) . '</td>
					<td>' . get_user_status_text($value) . '</td>
					<td>' . get_user_banned_label($value) . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/user/' . $value->get_id() . '/" title="Просмотр"><i class = "fa fa-eye"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/usereditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/userdelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
    }
    $content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/useraddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить пользователя</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
    add_script(get_admin_template_folder() . '/plugins/deleteConfirm/deleteConfirm.js', 10, 'footer');
    set_active_admin_menu('users');
    set_title('Управление пользователями');
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_usersearch() {
    if (empty($_POST['search'])) {
        $allusers = [];
    } else {
        $allusers = search_user($_POST['search']);
    }
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/usersearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-10">
									<input type = "text" name = "search" value = "' . (isset($_POST['search']) ? $_POST['search'] : '') . '" placeholder = "SteamID или имя пользователя" class = "form-control">
								</div>
								<div class = "col-md-2">
									<button type = "submit" class = "btn btn-primary pull-right"><i class = "fa fa-search"></i> Поиск</button>
								</div>
							</div>
						</form>
					</div>
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Аватар</th>
									<th>Имя</th>
									<th>Steam ID</th>
									<th>VK ID</th>
									<th>Баланс</th>
									<th>Открыто кейсов</th>
									<th>Контракты</th>
									<th>Статус</th>
									<th>Бан</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
    foreach ($allusers as $value) {
        $content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td><img src = "' . $value->get_data('image') . '" width = "30px"></td>
					<td>' . $value->get_name() . '</td>
					<td>' . $value->get_data('steam_id') . '</td>
					<td>' . $value->get_data('vk_id') . '</td>
					<td>' . get_user_balance($value) . '</td>
					<td>' . get_user_count_cases($value) . '</td>
					<td>' . get_user_count_contracts($value) . '</td>
					<td>' . get_user_status_text($value) . '</td>
					<td>' . get_user_banned_label($value) . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/user/' . $value->get_id() . '/" title="Просмотр"><i class = "fa fa-eye"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/usereditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/userdelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
    }
    $content .= '
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
		';
    set_active_admin_menu('usersearch');
    set_title('Поиск пользователей');
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_user($args) {
    $user = new user($args[0]);
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
													<th>Имя</th> <td><a href = "https://steamcommunity.com/profiles/' . $user->get_data('steam_id') . '/" target = "_blank">' . $user->get_name() . '</a></td>
												</tr>
												<tr>
													<th>Steam ID</th> <td>' . $user->get_data('steam_id') . '</td>
												</tr>
												<tr>
													<th>VK ID</th> <td>' . $user->get_data('vk_id') . '</td>
												</tr>
												<tr>
													<th>Ссылка на обмен:</th> <td><a href = "' . $user->get_data('trade_link') . '" target = "_blank">' . $user->get_data('trade_link') . '</a></td>
												</tr>
												<tr>
													<th>Баланс:</th> <td>' . get_user_balance($user) . '</td>
												</tr>
												<tr>
													<th>Изменение шанса:</th> <td>' . $user->get_data('chance') . '%</td>
												</tr>
												<tr>
													<th>Статус:</th> <td>' . get_user_status_text($user) . '</td>
												</tr>
												<tr>
													<th>Бан:</th> <td>' . get_user_banned_label($user) . '</td>
												</tr>
												<tr>
													<th>Блокировка вывода:</th> <td>' . ($user->get_data('withdraw_disabled') ? '<span class="label label-danger">Заблокирован</span>' : '<span class="label label-success">Разблокировн</span>') . '</td>
												</tr>
												<tr>
													<th>Блокировка депозита:</th> <td>' . ($user->get_data('deposite_disabled') ? '<span class="label label-danger">Заблокирован</span>' : '<span class="label label-success">Разблокировн</span>') . '</td>
												</tr>
												<tr>
													<th>Скрывать в топе:</th> <td>' . ($user->get_data('top_disabled') ? '<span class="label label-danger">Да</span>' : '<span class="label label-success">Нет</span>') . '</td>
												</tr>
												<tr>
													<th>Использовать личный профит:</th> <td>' . ($user->get_data('use_self_profit') ? '<span class="label label-danger">Да</span>' : '<span class="label label-success">Нет</span>') . '</td>
												</tr>
												<tr>
													<th>Открыто кейсов:</th> <td>' . get_user_count_cases($user) . '</td>
												</tr>
												<tr>
													<th>Контракты:</th> <td>' . get_user_count_contracts($user) . '</td>
												</tr>
												<tr>
													<th>Доступность обменов:</th> <td>' . (is_escrow($user->get_id()) ? '<span class="label label-success">Доступны</span>' : '<span class="label label-danger">Не доступны</span>') . '</td>
												</tr>
											</table>
										</div>
									</div>
								</div>	
							</div>	
						</div>	
						<div class = "box-footer">
							<a href = "' .ADMINURL . '/opencase/usereditform/' . $user->get_id() . '/" class = "btn btn-success"><i class = "fa fa-pencil"></i> Редактировать пользователя</a>
							<a href = "http://steam.tools/itemvalue/#/' . $user->get_data('steam_id') . '-730" class = "btn btn-primary" target = "_blank"><i class = "fa fa-suitcase"></i> Инвентарь пользователя</a>
						</div>
					</div>
				</div>
			</div>
			<div class = "row">
				<div class = "col-xs-12">
					<div class="nav-tabs-custom">
						<ul class="nav nav-tabs">
							<li class="active"><a href="#opencases" data-toggle="tab">Открытые кейсы</a></li>
							<li><a href="#contracts" data-toggle="tab">Контракты</a></li>
							<li><a href="#deposites" data-toggle="tab">Депозиты</a></li>
							<li><a href="#withdraws" data-toggle="tab">Выводы</a></li>
							<li><a href="#balancelog" data-toggle="tab">Баланс лог</a></li>
						</ul>
						<div class="tab-content">
							<div class="active tab-pane" id="opencases">
								<table class = "table table-bordered table-striped">
									<thead>
										<tr>
											<th>ID</th>
											<!--<th>Пользователь</th>-->
											<th>Кейс</th>
											<th>Предмет</th>
											<th>Цена предмета</th>
											<th>Цена кейса</th>
											<th>Профит</th>
											<th>Время</th>
											<th>Статус</th>
										</tr>
									</thead>
										
									<tbody>
							';
    $openCase = new openCase();
    $allcases = $openCase->get_openCases('user_id = ' . $user->get_id(), 'id DESC', 100);
    foreach ($allcases as $value) {
        if ($value->get_profit() > 0) {
            $label_class = 'label-success';
        } else if ($value->get_profit() < 0) {
            $label_class = 'label-danger';
        } else {
            $label_class = 'label-warning';
        }
        $content .= '
										<tr>
											<td>' . $value->get_id() . '</td>
											<td><a href = "' .ADMINURL . '/opencase/caseitems/' . $value->get_case_id() . '/">' . $value->get_case_class()->get_name() . '</a></td>
											<td>' . $value->get_item_class()->get_item_class()->get_name() . ' ' . ($value->get_item_class()->get_text_quality_en() ? '(' . $value->get_item_class()->get_text_quality_en() . ')' : '' ) . '</td>
											<td>' . $value->get_item_class()->get_price() . ' руб</td>
											<td>' . $value->get_case_price() . ' руб</td>
											<td><span class = "label ' . $label_class . '">' . $value->get_profit() . ' руб</span></td>
											<td>' . $value->get_format_time_open() . '</td>
											<td>' . $value->get_item_class()->get_label_status() . '</td>
										</tr>
									';
    }
    $content .= '	
									</tbody>
								</table>
							</div>
							<div class="tab-pane" id="contracts">
								<table class = "table table-bordered table-striped">
									<thead>
										<tr>
											<th>ID</th>
											<!--<th>Пользователь</th>-->
											<th>Предмет</th>
											<th>Цена предмета</th>
											<th>Цена контракта</th>
											<th>Профит</th>
											<th>Время</th>
											<th>Статус</th>
										</tr>
									</thead>
										
									<tbody>
							';
    $contract = new contract();
    $allcontracts = $contract->get_contracts('user_id = ' . $user->get_id(), 'id DESC', 100);
    foreach ($allcontracts as $value) {
        if ($value->get_profit() > 0) {
            $label_class = 'label-success';
        } else if ($value->get_profit() < 0) {
            $label_class = 'label-danger';
        } else {
            $label_class = 'label-warning';
        }
        $content .= '
										<tr>
											<td>' . $value->get_id() . '</td>
											<td>' . $value->get_item_class()->get_item_class()->get_name() . ' (' . $value->get_item_class()->get_text_quality_en() . ')</td>
											<td>' . $value->get_item_class()->get_price() . ' руб</td>
											<td>' . $value->get_items_price() . ' руб</td>
											<td><span class = "label ' . $label_class . '">' . $value->get_profit() . ' руб</span></td>
											<td>' . $value->get_format_time_open() . '</td>
											<td>' . $value->get_item_class()->get_label_status() . '</td>
										</tr>
									';
    }
    $content .= '	
									<tbody>
								</table>
							</div>
							<div class="tab-pane" id="deposites">
								<table class = "table table-bordered table-striped">
									<thead>
										<tr>
											<th>ID</th>
											<th>Номер платежа</th>
											<!--<th>Пользователь</th>-->
											<th>Сумма</th>
											<th>Платежная система</th>
											<th>Статус</th>
											<th>Время</th>
										</tr>
									</thead>
										
									<tbody>
							';
    $deposite = new deposite();
    $alllogs = $deposite->get_deposites('user_id = ' . $user->get_id(), 'id DESC', 100);
    foreach ($alllogs as $value) {
        $content .= '
										<tr>
											<td>' . $value->get_id() . '</td>
											<td>' . $value->get_num() . '</td>
											<!--<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>-->
											<td>' . $value->get_sum() . ' руб</td>
											<td>' . $value->get_from_text() . '</td>
											<td>' . $value->get_status_label() . '</td>
											<td>' . $value->get_format_time_add() . '</td>
										</tr>
									';
    }
    $content .= '	
									</tbody>
								</table>
							</div>
							<div class="tab-pane" id="withdraws">
								<table class = "table table-bordered table-striped">
									<thead>
										<tr>
											<th>ID</th>
											<!--<th>Пользователь</th>-->
											<th>Предмет</th>
											<th>Цена</th>
											<th>Статус</th>
											<th>Время</th>
										</tr>
									</thead>
										
									<tbody>
							';
    $dItem = new droppedItem();
    $alldItems = $dItem->get_droppedItems('(status = 1 or status = 2 or status = 5) and user_id = ' . $user->get_id(), 'id DESC', 100);
    foreach ($alldItems as $value) {
        $content .= '
										<tr>
											<td>' . $value->get_id() . '</td>
											<!--<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>-->
											<td>' . $value->get_item_name_alt() . '</td>
											<td>' . $value->get_price() . ' руб</td>
											<td>' . $value->get_label_status() . '</td>
											<td>' . $value->get_format_time_drop() . '</td>
										</tr>
									';
    }
    $content .= '	
									</tbody>
								</table>
							</div>
							<div class="tab-pane" id="balancelog">
								<table class = "table table-bordered table-striped">
									<thead>
										<tr>
											<th>ID</th>
											<!--<th>Пользователь</th>-->
											<th>Комментарий</th>
											<th>Изменение</th>
											<th>Время</th>
											<th>Тип</th>
										</tr>
									</thead>
										
									<tbody>
							';
    $balanceLog = new balanceLog();
    $alllogs = $balanceLog->get_balanceLogs('user_id = ' . $user->get_id(), 'id DESC', 100);
    foreach ($alllogs as $value) {
        $content .= '
										<tr>
											<td>' . $value->get_id() . '</td>
											<!--<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>-->
											<td>' . $value->get_comment() . '</td>
											<td><span class = "label label-' . ($value->get_change() >= 0 ? 'success' : 'danger') . '">' . $value->get_change() . ' руб</span></td>
											<td>' . $value->get_format_time() . '</td>
											<td>' . $value->get_text_type() . '</td>
										</tr>
									';
    }
    $content .= '	
									</tbody>
								</table>
							</div>
						</div>
					</div>
				</div>
			</div>
		';
    set_active_admin_menu('users');
    add_breadcrumb('Управление пользователями', ADMINURL . '/opencase/users/', 'fa-users');
    set_title('Просмотр пользователя ' . $user->get_name());
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_useraddform() {
    $user = new user();
    $status = '';
    foreach (get_user_status_array() as $key => $value) {
        $status .= '<option value = "' . $key . '">' . $value . '</option>';
    }
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/useradd/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя пользователя: </label>
								<input type = "text" class="form-control" name="name" id="name">
							</div>
							<div class="form-group">
								<label for="steam_id">Steam ID: </label>
								<input type = "text" class="form-control" name="steam_id" id="steam_id">
							</div>
							<div class="form-group">
								<label for="vk_id">VK ID: </label>
								<input type = "text" class="form-control" name="vk_id" id="vk_id">
							</div>
							<div class="form-group">
								<label for="image">Аватар пользователя: </label>
								<input type = "text" class="form-control" name="image" id="image">
							</div>
							<div class="form-group">
								<label for="trade_link">Ссылка на обмен: </label>
								<input type = "text" class="form-control" name="trade_link" id="trade_link">
							</div>
							<div class="form-group">
								<label for="balance">Баланс: </label>
								<input type = "text" class="form-control" name="balance" id="balance">
							</div>
							<div class="form-group">
								<label for="chance">Изменение шанса: </label>
								<input type = "text" class="form-control" name="chance" id="chance" value = "100">
							</div>
							<div class="form-group">
								<label for="status">Статус: </label>
								<select id = "status" name = "status" class = "form-control">
									' . $status . '
								</select>
							</div>
							<div class="form-group">
								<label for="banned">Бан: </label>
								<select id = "banned" name = "banned" class = "form-control">
									<option value = "0">Разбанен</option>
									<option value = "1">Забанен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="timecreated">Дата регистрации в стим: </label>
								<input type = "text" class="form-control" name="timecreated" id="timecreated">
							</div>
							<div class="form-group">
								<label for="withdraw_disabled">Блокировка вывода: </label>
								<select id = "withdraw_disabled" name = "withdraw_disabled" class = "form-control">
									<option value = "0">Разблокировн</option>
									<option value = "1">Заблокирован</option>
								</select>
							</div>							
							<div class="form-group">
								<label for="deposite_disabled">Блокировка депозита: </label>
								<select id = "deposite_disabled" name = "deposite_disabled" class = "form-control">
									<option value = "0">Разблокировн</option>
									<option value = "1">Заблокирован</option>
								</select>
							</div>
							<div class="form-group">
								<label for="top_disabled">Скрывать в топе: </label>
								<select id = "top_disabled" name = "top_disabled" class = "form-control">
									<option value = "0">Нет</option>
									<option value = "1">Да</option>
								</select>
							</div>
							<div class="form-group">
								<label for="use_self_profit">Использовать личный профит: </label>
								<select id = "use_self_profit" name = "use_self_profit" class = "form-control">
									<option value = "0">Нет</option>
									<option value = "1">Да</option>
								</select>
							</div>
							<div class="form-group" id="selfProfitWrap" style="display:none">
								<label for="self_profit">Личный профит для пользователя: </label>
								<input type = "text" class="form-control" name="self_profit" value="0" id="self_profit">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить пользователя</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
    add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
    add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
    add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
    add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 1500,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
    add_jscript(' $(function () {
			$("#use_self_profit").on("change", function() {
				let enable = $(this).val();
				if (enable == 1) {
					$("#selfProfitWrap").show();
				} else {
					$("#selfProfitWrap").hide();
				}
			});
		});');
    set_active_admin_menu('useradd');
    add_breadcrumb('Управление пользователями', ADMINURL . '/opencase/users/', 'fa-users');
    set_title('Добавление пользователя');
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_useradd() {
    if ($_POST['name'] != '' && $_POST['steam_id'] != '' && $_POST['image'] != '') {
        $user = new user();
        $user->set_from_array($_POST);
        $user->add();
        $user->set_data('steam_id', $_POST['steam_id']);
        $user->set_data('vk_id', $_POST['vk_id']);
        $user->set_data('image', $_POST['image']);
        $user->set_data('timecreated', $_POST['timecreated']);
        $user->set_data('balance', $_POST['balance']);
        $user->set_data('trade_link', $_POST['trade_link']);
        $user->set_data('chance', $_POST['chance']);
        $user->set_data('withdraw_disabled', $_POST['withdraw_disabled']);
        $user->set_data('deposite_disabled', $_POST['deposite_disabled']);
        $user->set_data('top_disabled', $_POST['top_disabled']);
        $user->set_data('use_self_profit', $_POST['use_self_profit']);
        $user->set_data('self_profit', max(0, $_POST['self_profit']));
        $user->set_data('status', $_POST['status']);
        $user->update_user_data();
        alertS('Пользователь успешно добавлен', ADMINURL . '/opencase/users/');
    } else {
        alertE('Не все поля заполнены', ADMINURL . '/opencase/useraddform/');
    }
}

function admin_opencase_usereditform($args) {
    $user = new user($args[0]);
    $status = '';
    foreach (get_user_status_array() as $key => $value) {
        $status .= '<option value = "' . $key . '"' . ($key == $user->get_data('status') ? ' selected = "selected"' : '') . '>' . $value . '</option>';
    }
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/useredit/' . $user->get_id() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя пользователя: </label>
								<input type = "text" class="form-control" name="name" id="name" value = "' . $user->get_name() . '">
							</div>
							<div class="form-group">
								<label for="steam_id">Steam ID: </label>
								<input type = "text" class="form-control" name="steam_id" id="steam_id" value = "' . $user->get_data('steam_id') . '">
							</div>
							<div class="form-group">
								<label for="vk_id">VK ID: </label>
								<input type = "text" class="form-control" name="vk_id" id="vk_id" value = "' . $user->get_data('vk_id') . '">
							</div>
							<div class="form-group">
								<label for="image">Аватар пользователя: </label>
								<input type = "text" class="form-control" name="image" id="image" value = "' . $user->get_data('image') . '">
							</div>
							<div class="form-group">
								<label for="trade_link">Ссылка на обмен: </label>
								<input type = "text" class="form-control" name="trade_link" id="trade_link" value = "' . $user->get_data('trade_link') . '">
							</div>
							<div class="form-group">
								<label for="balance">Баланс: </label>
								<input type = "text" class="form-control" name="balance" id="balance" value = "' . get_user_balance($user) . '">
							</div>
							<div class="form-group">
								<label for="chance">Изменение шанса: </label>
								<input type = "text" class="form-control" name="chance" id="chance" value = "' . $user->get_data('chance') . '">
							</div>
							<div class="form-group">
								<label for="status">Статус: </label>
								<select id = "status" name = "status" class = "form-control">
									' . $status . '
								</select>
							</div>
							<div class="form-group">
								<label for="banned">Бан: </label>
								<select id = "banned" name = "banned" class = "form-control">
									<option value = "0"' . ($user->get_banned() ? '' : ' selected = "selected"') . '>Разбанен</option>
									<option value = "1"' . ($user->get_banned() ? ' selected = "selected"' : '') . '>Забанен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="withdraw_disabled">Блокировка вывода: </label>
								<select id = "withdraw_disabled" name = "withdraw_disabled" class = "form-control">
									<option value = "0"' . ($user->get_data('withdraw_disabled') ? '' : ' selected = "selected"') . '>Разблокировн</option>
									<option value = "1"' . ($user->get_data('withdraw_disabled') ? ' selected = "selected"' : '') . '>Заблокирован</option>
								</select>
							</div>							
							<div class="form-group">
								<label for="deposite_disabled">Блокировка депозита: </label>
								<select id = "deposite_disabled" name = "deposite_disabled" class = "form-control">
									<option value = "0"' . ($user->get_data('deposite_disabled') ? '' : ' selected = "selected"') . '>Разблокировн</option>
									<option value = "1"' . ($user->get_data('deposite_disabled') ? ' selected = "selected"' : '') . '>Заблокирован</option>
								</select>
							</div>
							<div class="form-group">
								<label for="top_disabled">Скрывать в топе: </label>
								<select id = "top_disabled" name = "top_disabled" class = "form-control">
									<option value = "0"' . ($user->get_data('top_disabled') ? '' : ' selected = "selected"') . '>Нет</option>
									<option value = "1"' . ($user->get_data('top_disabled') ? ' selected = "selected"' : '') . '>Да</option>
								</select>
							</div>
							<div class="form-group">
								<label for="use_self_profit">Использовать личный профит: </label>
								<select id = "use_self_profit" name = "use_self_profit" class = "form-control">
									<option value = "0"' . ($user->get_data('use_self_profit') ? '' : ' selected = "selected"') . '>Нет</option>
									<option value = "1"' . ($user->get_data('use_self_profit') ? ' selected = "selected"' : '') . '>Да</option>
								</select>
							</div>
							<div class="form-group" id="selfProfitWrap"' . ($user->get_data('use_self_profit') ? '' : ' style="display:none"') . '>
								<label for="self_profit">Личный профит для пользователя: </label>
								<input type = "text" class="form-control" name="self_profit" value="' . $user->get_data('self_profit') . '" id="self_profit">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-pencil"></i> Сохранить</button>
							<a href = "' .ADMINURL . '/opencase/user/' . $user->get_id() . '/" class = "btn btn-primary"><i class = "fa fa-eye"></i> Просмотр пользователя</a>
						</div>
					</form>
				</div>
			</div>
		</div>';
    add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
    add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
    add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
    add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 1500,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
    add_jscript(' $(function () {
			$("#use_self_profit").on("change", function() {
				let enable = $(this).val();
				if (enable == 1) {
					$("#selfProfitWrap").show();
				} else {
					$("#selfProfitWrap").hide();
				}
			});
		});');
    set_active_admin_menu('users');
    add_breadcrumb('Управление пользователями', ADMINURL . '/opencase/users/', 'fa-users');
    set_title('Редактирование пользователя');
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_useredit($args) {
    $user = new user($args[0]);
    if ($_POST['name'] != '' && ($_POST['steam_id'] != '' || $_POST['vk_id'] != '') && $_POST['image'] != '') {
        if (get_user_balance($user) != $_POST['balance']) {
            add_balance_log($user->get_id(), ($_POST['balance'] - get_user_balance($user)), 'Изменение баланса администратором', 6);
        }
        $user->set_from_array($_POST);
        $user->set_data('steam_id', $_POST['steam_id']);
        $user->set_data('vk_id', $_POST['vk_id']);
        $user->set_data('image', $_POST['image']);
        $user->set_data('timecreated', $_POST['timecreated']);
        $user->set_data('balance', $_POST['balance']);
        $user->set_data('trade_link', $_POST['trade_link']);
        $user->set_data('chance', $_POST['chance']);
        $user->set_data('withdraw_disabled', $_POST['withdraw_disabled']);
        $user->set_data('deposite_disabled', $_POST['deposite_disabled']);
        $user->set_data('top_disabled', $_POST['top_disabled']);
        $user->set_data('use_self_profit', $_POST['use_self_profit']);
        $user->set_data('self_profit', max(0, $_POST['self_profit']));
        $user->set_data('status', $_POST['status']);
        $user->update();
        alertS('Изменения успешно сохранены', ADMINURL . '/opencase/usereditform/' . $user->get_id() . '/');
    } else {
        alertE('Не все поля заполнены', ADMINURL . '/opencase/usereditform/' . $user->get_id() . '/');
    }
}

function admin_opencase_userdelete($args) {
    $user = new user($args[0]);
    $user->delete();
    alertS('Пользователь успешно удален', ADMINURL . '/opencase/users/');
}

function admin_opencase_fakeopen() {
    $content = '
		<div class = "row">
			<div class = "col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/fakestart/">
						<div class="box-body">
							<div class="form-group">
								<label for="limit">Использовать ботов (0 - все боты): </label>
								<input type = "text" class="form-control" name="limit" id="limit" value = "0">
							</div>
							<div class="form-group">
								<label for="count">Максимальное количество открытий на каждого: </label>
								<input type = "count" class="form-control" name="count" id="count" value = "30">
							</div>
							<div class="form-group">
								<label for="freq">Частота открытий (секунд): </label>
								<input type = "count" class="form-control" name="freq" id="freq" value = "30">
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit">Запустить фейк открытия</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
    set_active_admin_menu('userfake');
    add_breadcrumb('Управление пользователями', ADMINURL . '/opencase/users/', 'fa-users');
    set_title('Фейк открытия');
    set_content($content);
    set_tpl('index.php');
}

function admin_opencase_fakestart() {
    $user_ids = get_user_ids_by_status(100, 'rand()', !empty($_POST['limit']) ? (int) $_POST['limit'] : false);
    foreach ($user_ids as $i => $user_id) {
        bot_fake_open($user_id, !empty($_POST['count']) ? rand(1, (int) $_POST['count']) : 30, $i * 600, !empty($_POST['freq']) ? (int) $_POST['freq'] : 30);
    }
    alertS('Фейк открытия успешно добавлены', ADMINURL . '/opencase/fakeopen/');
}

function bot_fake_open($user_id, $count = 1, $start = 0, $freq = 30) {
    for ($j = 0; $j < $count; $j++) {
        $case = new ocase();
        $cases = $case->get_ocases('enable = 1 and price > 0');
        $user = new user($user_id);
        $case = $cases[array_rand($cases)];
        $casePrice = $case->get_final_price();
        $fast = 1;
        $items = array();
        if ($case->get_id() != '') {
            if ($case->is_available()) {
                if ($case->get_price() > 0 || ($case->get_price() == 0 && can_open_free_case($case))) {
                    $enabledItems = db()->query('select * from opencase_itemincase where case_id = "' . $case->get_id() . '" and (count_items = -1 or count_items > 0) and enabled = 1 and chance > 0 order by chance DESC');
                    $item_names = array();
                    foreach ($enabledItems as $item) {
                        $tmpItem = new item($item['item_id']);
                        $items[] = array('name' => $tmpItem->get_name(), 'chance' => $item['chance'], 'item_id' => $item['item_id'], 'withdrawable' => $item['withdrawable'], 'usable' => $item['usable'], 'image' => $tmpItem->get_image(), 'rarity' => $tmpItem->get_css_quality_class(), 'quality' => $tmpItem->get_quality(), 'price' => $tmpItem->get_price());
                    }
                    $haveItems = $items;
                    if (count($enabledItems) > 0) {
                        $sum = 0;
                        foreach ($haveItems as $key => $hItem) {
                            $sum += $hItem['chance'];
                        }

                        if (count($haveItems) > 0) {
                            $chance = rand(0, $sum - 1);
                            $i = 0;
                            $find = false;
                            $item = false;
                            forEach ($haveItems as $hItem) {
                                if ($chance >= $i && $chance < $i + (int) $hItem['chance'] && !$find) {
                                    $item = $hItem;
                                    $find = true;
                                } else {
                                    $i += (int) $hItem['chance'];
                                }
                            }
                            if ($item) {
                                $dItem = new droppedItem();
                                $itemPrice = round($item['price']);
                                $dItem->set_parametrs('', $user->get_id(), $item['item_id'], 5, $itemPrice, '', 3, $case->get_id(), $fast, 0, 0, '', $item['withdrawable'], $item['usable']);
                                $openTime = $start + $freq * $j;
                                if ($freq > 0) {
                                    $randTime = rand($openTime - 30, $openTime + 30);
                                } else {
                                    $randTime = $openTime;
                                }
                                $time = $dItem->add_droppedItem($randTime);
                                $itemID = $dItem->get_id();
                                $case->inc_open_count();
                                $openCase = new openCase();
                                $openCase->set_parametrs('', $user->get_id(), $case->get_id(), $itemID, $casePrice, '');
                                $openCase->add_openCase(true, $randTime);
                                $itemincase = new itemincase($item['item_id']);
                                $user->update();
                                update_setval('opencase_count_open_case', get_setval('opencase_count_open_case') + 1);
                                centrifugo::sendItem($dItem, $time);
                                centrifugo::sendStats();
                            } else {
                                $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                            }
                        } else {
                            $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                        }
                    } else {
                        $json['error'] = 'При открытие кейса возникла ошибка, попробуйте повторить операцию позже';
                    }
                } else {
                    $json['error'] = 'Вы не можете открыть бесплатный кейс, т.к. у Вас не выполнены все условия';
                }
            } else {
                $json['error'] = 'В данный момент, этот кейс недоступен';
            }
        } else {
            $json['error'] = 'Такого кейса не существует';
        }
    }
}
