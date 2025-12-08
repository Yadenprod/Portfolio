<?php

add_admin_get('/opencase/items/(([0-9]+)/)?', 'admin_opencase_items');
add_admin_app('/opencase/itemsearch/', 'admin_opencase_itemsearch');
add_admin_get('/opencase/itemaddform/', 'admin_opencase_itemaddform');
add_admin_post('/opencase/itemadd/', 'admin_opencase_itemadd');
add_admin_get('/opencase/itemeditform/([0-9]+)/', 'admin_opencase_itemeditform');
add_admin_post('/opencase/itemedit/([0-9]+)/', 'admin_opencase_itemedit');
add_admin_get('/opencase/itemdelete/([0-9]+)/', 'admin_opencase_itemdelete');
add_admin_get('/opencase/itemupload/', 'admin_opencase_itemupload');

function admin_opencase_items($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$itemcount = db()->query_once('select count(id) from opencase_items');
	$pages = new Pages();
	$pages->set_num_object($itemcount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/items/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/items/');
	$pages->set_curent_page($page);
	$item = new item();
	$allitems = $item->get_items('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$quality = '<option value = "-1">Выберите качество</option>';
	foreach ($item->get_quality_array() as $key => $value) {
		$quality .= '<option value = "' . $key . '">' . $value . '</option>';
	}
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/itemsearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-5">
									<input type = "text" name = "name" value = "" placeholder = "Название предмета" class = "form-control">
								</div>
								<div class = "col-md-5">
									<select id = "quality" name = "quality" class = "form-control">
										' . $quality . '
									</select>
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
									<th>Название</th>
									<th>Изображение</th>
									<th>Цена</th>
									<th>В наличии</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allitems as $value) {
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td>' . $value->get_name() . '</td>
					<td><img src = "' . $value->get_steam_image('40f', '30f') . '"></td>
					<td>' . $value->get_price() . ' руб.</td>
					<td>' . $value->get_count_on_bot() . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/itemeditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/itemdelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/itemaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить предмет</a>
						<a href="' .ADMINURL . '/opencase/itemupload/" class="btn btn-primary"><i class="fa fa-upload"></i> Загрузить предметы</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/deleteConfirm/deleteConfirm.js', 10, 'footer');
	set_active_admin_menu('items');
	set_title('Упрвление предметами');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_itemsearch() {
	$item = new item();
	$where = '';
	if (isset($_POST['name']) && $_POST['name'] != '') {
		$where .= 'name like "%' . db()->nomysqlinj(trim($_POST['name'])) . '%"';
	}
	if (isset($_POST['quality']) && $_POST['quality'] != '-1') {
		$where .= (strlen($where) > 0 ? ' and ' : '') . 'quality = "' . db()->nomysqlinj($_POST['quality']) . '"';
	}
	if (strlen($where) == 0) {
		$where = '1 = 0';
	}
	$allitems = $item->get_items($where, 'id DESC');
	$quality = '<option value = "-1">Выберите качество</option>';
	foreach ($item->get_quality_array() as $key => $value) {
		$quality .= '<option value = "' . $key . '"' . (isset($_POST['quality']) && $key == $_POST['quality'] ? ' selected = "selected"' : '') . '>' . $value . '</option>';
	}
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/itemsearch/" method = "POST">
							<div class = "row">
								<div class = "col-md-5">
									<input type = "text" name = "name" value = "' . (isset($_POST['name']) ? $_POST['name'] : '') . '" placeholder = "Название предмета" class = "form-control">
								</div>
								<div class = "col-md-5">
									<select id = "quality" name = "quality" class = "form-control">
										' . $quality . '
									</select>
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
									<th>Название</th>
									<th>Изображение</th>
									<th>Цена</th>
									<th>В наличии</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allitems as $value) {
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td>' . $value->get_name() . '</td>
					<td><img src = "' . $value->get_steam_image('40f', '30f') . '"></td>
					<td>' . $value->get_price() . ' руб.</td>
					<td>' . $value->get_count_on_bot() . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/itemeditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/itemdelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/itemaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить предмет</a>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('itemsearch');
	set_title('Поиск предметов');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_itemaddform() {
	$item = new item();
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/itemadd/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Название предмета: </label>
								<input type = "text" class="form-control" name="name" id="name">
							</div>
							<div class="form-group">
								<label for="image">Изображение предмета: </label>
								<input type = "text" class="form-control" name="image" id="image">
							</div>
							<div class="form-group">
								<label for="price">Цена: </label>
								<input type = "text" class="form-control" name="price" id="price">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить предмет</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('itemadd');
	add_breadcrumb('Упрвление предметами', ADMINURL . '/opencase/items/', 'fa-gavel');
	set_title('Добавление предмета');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_itemadd() {
	if ($_POST['name'] != '' && $_POST['image'] != '') {
		$item = new item();
		$item->set_parametrs_from_request();
		$item->add_item();
		alertS('Предмет успешно добавлен', ADMINURL . '/opencase/items/');
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/opencase/itemaddform/');
	}
}

function admin_opencase_itemeditform($args) {
	$item = new item($args[0]);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/itemedit/' . $item->get_id() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Название предмета: </label>
								<input type = "text" class="form-control" name="name" id="name" value = "' . $item->get_name() . '">
							</div>
							<div class="form-group">
								<label for="image">Изображение предмета: </label>
								<input type = "text" class="form-control" name="image" id="image" value = "' . $item->get_image() . '">
							</div>
							<div class="form-group">
								<label for="price">Цена: </label>
								<input type = "text" class="form-control" name="price" id="price" value = "' . $item->get_price() . '">
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('items');
	add_breadcrumb('Упрвление предметами', ADMINURL . '/opencase/items/', 'fa-gavel');
	set_title('Редактирование предмета');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_itemedit($args) {
	$item = new item($args[0]);
	if ($_POST['name'] != '' && $_POST['image'] != '') {
		$item->set_parametrs_from_request();
		$item->update_item();
		alertS('Изменения успешно сохранены', ADMINURL . '/opencase/itemeditform/' . $item->get_id() . '/');
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/opencase/itemeditform/' . $item->get_id() . '/');
	}
}

function admin_opencase_itemdelete($args) {
	$item = new item($args[0]);
	$item->delete_item();
	alertS('Предмет успешно удален', ADMINURL . '/opencase/items/');
}

function admin_opencase_itemupload() {
	$item = new item();
	$error = '';
	$success = $item->update_items_list($error);
	if ($success) {
		alertS('Предметы успешно обновлены.', ADMINURL . '/opencase/items/');
	} else {
		alertE($error, ADMINURL . '/opencase/items/');
	}
}
