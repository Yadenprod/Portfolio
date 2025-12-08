<?php

add_admin_get('/opencase/case/(([0-9]+)/)?', 'admin_opencase_case');
add_admin_get('/opencase/caseaddform/(([0-9]+)/)?', 'admin_opencase_caseaddform');
add_admin_post('/opencase/caseadd/', 'admin_opencase_caseadd');
add_admin_get('/opencase/caseeditform/([0-9]+)/', 'admin_opencase_caseeditform');
add_admin_post('/opencase/caseedit/([0-9]+)/', 'admin_opencase_caseedit');
add_admin_get('/opencase/casedelimage/([0-9]+)/', 'admin_opencase_casedelimage');
add_admin_get('/opencase/casedelitemimage/([0-9]+)/', 'admin_opencase_casedelitemimage');
add_admin_get('/opencase/casedelete/([0-9]+)/', 'admin_opencase_casedelete');
add_admin_get('/opencase/caseitems/(([0-9]+)/)?', 'admin_opencase_caseitems');
add_admin_get('/opencase/additemincaseform/([0-9]+)/([0-9]+)/', 'admin_opencase_additemincaseform');
add_admin_post('/opencase/additemincase/([0-9]+)/([0-9]+)/', 'admin_opencase_additemincase');
add_admin_get('/opencase/edititemincaseform/([0-9]+)/', 'admin_opencase_edititemincaseform');
add_admin_post('/opencase/edititemincase/([0-9]+)/', 'admin_opencase_edititemincase');
add_admin_get('/opencase/deleteitemincase/([0-9]+)/', 'admin_opencase_deleteitemincase');
add_admin_get('/opencase/category/', 'admin_opencase_category');
add_admin_get('/opencase/categoryaddform/', 'admin_opencase_categoryaddform');
add_admin_post('/opencase/categoryadd/', 'admin_opencase_categoryadd');
add_admin_get('/opencase/categoryeditform/([0-9]+)/', 'admin_opencase_categoryeditform');
add_admin_post('/opencase/categoryedit/([0-9]+)/', 'admin_opencase_categoryedit');
add_admin_get('/opencase/categoryup/([0-9]+)/', 'admin_opencase_categoryup');
add_admin_get('/opencase/categorydown/([0-9]+)/', 'admin_opencase_categorydown');
add_admin_get('/opencase/categorydelete/([0-9]+)/', 'admin_opencase_categorydelete');
add_admin_get('/opencase/caseposition/', 'admin_opencase_caseposition');
add_admin_get('/opencase/cases/items/chance/calc/', 'admin_opencase_calc_all_cases_items_chance');
add_admin_get('/opencase/cases/items/chance/reset/', 'admin_opencase_reset_all_cases_items_chance');
add_admin_get('/opencase/case/([0-9]+)/items/chance/calc/', 'admin_opencase_calc_case_items_chance');
add_admin_get('/opencase/case/([0-9]+)/items/chance/reset/', 'admin_opencase_reset_case_items_chance');

function admin_opencase_case($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$casecount = db()->query_once('select count(id) from opencase_case');
	$pages = new Pages();
	$pages->set_num_object($casecount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/case/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/case/');
	$pages->set_curent_page($page);
	$ocase = new ocase();
	$allcases = $ocase->get_ocases('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Название</th>
									<th>Изображение</th>
									<th>Цена</th>
									<th>Скидка %</th>
									<th>Категория</th>
									<th>Включен</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allcases as $value) {
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td>' . $value->get_name() . '</td>
					<td><img src = "' . $value->get_src_image() . '" width = "40px"></td>
					<td>' . $value->get_sum_label() . '</td>
					<td>' . $value->get_sale() . '</td>
					<td>' . $value->get_category_class()->get_name() . '</td>
					<td>' . $value->get_label_enable() . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/caseitems/' . $value->get_id() . '/" title="Управление содержимым"><i class = "fa fa-suitcase"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/caseeditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/casedelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/caseaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить кейс</a>
						<a href="' .ADMINURL . '/opencase/cases/items/chance/calc/" class="btn btn-primary"><i class="fa fa-calculator"></i> Рассчитать шансы предметов</a>
						<a href="' .ADMINURL . '/opencase/cases/items/chance/reset/" class="btn btn-primary"><i class="fa fa-repeat"></i> Сбросить шансы предметов</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	add_script(get_admin_template_folder() . '/plugins/deleteConfirm/deleteConfirm.js', 10, 'footer');
	set_active_admin_menu('case');
	set_title('Упрвление кейсами');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_caseaddform($args) {
	$category_id = !empty($args[1]) ? (int) $args[1] : false;
	$category = new caseCategory();
	$case = new ocase();
	$maxid = db()->query_once('select max(id) from opencase_case');
	$maxid = $maxid['max(id)'] ? $maxid['max(id)'] : 0;
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/opencase/caseadd/" enctype="multipart/form-data">
				<div class="col-lg-9">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="name">Название кейса:</label>
								<input type = "text" class="form-control" name="name" id="name">
							</div>
							<div class="form-group">
								<label for="description">Описание:</label>
								<textarea class = "form-control" name = "description" id = "description"></textarea>
							</div>
							<div class="form-group">
								<label for="type">Тип:</label>
								<select name = "type" id = "type" class="form-control">
									<option value = "' . ocase::TYPE_DEFAULT . '">Обычный</option>
									<option value = "' . ocase::TYPE_PROMOCODE . '">По промокоду</option>
									<option value = "' . ocase::TYPE_DEPOSITE . '">По депозиту</option>
								</select>
							</div>
							<div class="form-group" id="priceWrapper">
								<label for="price">Цена:</label>
								<input type = "number" class="form-control" name="price" id="price">
							</div>
							<div class="form-group" id="promoWrapper" style="display:none">
								<label for="promocode">Промокод:</label>
								<div class="input-group">
									<input type = "text" class="form-control" name="promocode" id="promocode">
									<div class="input-group-btn">
										<a href = "#" class = "btn btn-primary" id = "generate-promo"><i class = "fa fa-gears"></i> Сгенерировать</a>
									</div>
								</div>
								<label for="promocount">Количество активаций:</label>
								<input type = "number" class="form-control" name="promocount" id="promocount" value = "100">
							</div>
							<div class="form-group">
								<label for="sale">Скида:</label>
								<input type = "number" class="form-control" name="sale" id="sale" value = "0">
							</div>
							<div class="form-group">
								<label for="category">Категория:</label>
								<select name = "category" id = "category" class="form-control">';
	foreach ($category->get_caseCategorys() as $cat) {
		$content .= '<option value = "' . $cat->get_id() . '"' . ($cat->get_id() == $category_id ? ' selected = "selected"' : '') . '>' . $cat->get_name() . '</option>';
	}
	$content .= '</select>
							</div>
							<div class="form-group">
								<label for="rarity">Редкость:</label>
								<select name = "rarity" id = "rarity" class="form-control">';
	foreach ($case->get_rarity_array() as $key => $label) {
		$content .= '<option value = "' . $key . '">' . $label . '</option>';
	}
	$content .= '</select>
							</div>
							<div class="form-group">
								<label for="enable">Включен:</label>
								<select name = "enable" id = "enable" class="form-control">
									<option value = "1">Включен</option>
									<option value = "0">Отключен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="label">Ярлык:</label>
								<input type = "text" class="form-control" name="label" id="label" value = "">
							</div>
							<div class="form-group">
								<label for="chance">Изменение шанса:</label>
								<input type = "number" class="form-control" name="chance" id="chance" value = "100">
							</div>
							<div class="form-group">
								<label for="key">Уникальный ключ:</label>
								<input type = "text" class="form-control" name="key" id="key" value = "case' . ($maxid + 1) . '">
							</div>
							<div class="form-group">
									<label for="max_open_count">Максимальное количество открытий</label>
									<input type = "text" class="form-control" name="max_open_count" id="max_open_count" value = "-1">
							</div>
							<div class="form-group" id="depositSumWrap" style="display:none">
									<label for="dep_for_open">Минимальная сумма депозита для открытия</label>
									<input type = "text" class="form-control" name="dep_for_open" id="dep_for_open" value = "0">
							</div>
							<div class="form-group" id="depositCountWrap" style="display:none">
								<label for="dep_open_count">Количество бесплатных открытий</label>
								<input type = "text" class="form-control" name="dep_open_count" id="dep_open_count" value = "1">
							</div>
							<div class="form-group">
								<label for="time_limit">Включен до</label>
								<input type = "text" class="form-control datepicker" name="time_limit" id="time_limit" value = "">
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить кейс</button>
						</div>
					</div>
				</div>
				<div class = "col-lg-3">
					<div class="box">
						<div class = "box-header with-border">
							Изображение кейса
						</div>
						<div class = "box-body">
							<input type = "file" name="upload_image" id="upload_image">
						</div>
					</div>
					<!--div class="box">
						<div class = "box-header with-border">
							Изображение предмета
						</div>
						<div class = "box-body">
							<input type = "file" name="upload_item_image" id="upload_item_image">
						</div>
					</div-->
				</div>
				</form>
			</div>
		';
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
	add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
	add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 300,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
			$("#sale").ionRangeSlider({
			  min: 0,
			  max: 100,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
	add_jscript(' $(function () {
			$("#generate-promo").click(function() {
				var alpha = \'QWERTYUIOPASDFGHJKLZXCVBNM0123456789\';
				var code = \'\';
				for (var i = 0; i < 8; i++) {
					code += alpha[Math.floor(Math.random() * alpha.length)];
				}
				code += \'-\';
				for (var i = 0; i < 4; i++) {
					code += alpha[Math.floor(Math.random() * alpha.length)];
				}
				code += \'-\';
				for (var i = 0; i < 4; i++) {
					code += alpha[Math.floor(Math.random() * alpha.length)];
				}
				code += \'-\';
				for (var i = 0; i < 4; i++) {
					code += alpha[Math.floor(Math.random() * alpha.length)];
				}
				$("#promocode").val(code);
				return false;
			});
		});');
	add_jscript(' $(function () {
			$("#type").on("change", function() {
				let type = $(this).val();
				if (type == ' . ocase::TYPE_PROMOCODE . ') {
					$("#price").val(0);
					$("#promoWrapper").show();
					$("#priceWrapper").hide();
					$("#depositSumWrap").show();
					$("#depositCountWrap").hide();
					$("#dep_open_count").val(1);
				} else if (type == ' . ocase::TYPE_DEFAULT . ') {
					$("#promoWrapper").hide();
					$("#priceWrapper").show();
					$("#depositSumWrap").hide();
					$("#dep_for_open").val(0);
					$("#depositCountWrap").hide();
					$("#dep_open_count").val(1);
				} else if (type == ' . ocase::TYPE_DEPOSITE . ') {
					$("#price").val(0);
					$("#promoWrapper").hide();
					$("#priceWrapper").hide();
					$("#depositSumWrap").show();
					$("#depositCountWrap").show();
				}
			});
			$.datetimepicker.setLocale("ru");
			$(".datepicker").datetimepicker({format:"d.m.Y H:i"});
		});');
	add_breadcrumb('Управление кейсами', ADMINURL . '/opencase/case/', 'fa-suitcase');
	set_active_admin_menu('caseadd');
	set_title('Добавить кейс');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_caseadd() {
	$case = new ocase();
	if (empty($_REQUEST['price'])) {
		$_REQUEST['price'] = 0;
	}
	$warning = '';
	if ($_REQUEST['type'] == ocase::TYPE_DEFAULT && $_REQUEST['price'] <= 0 && $_REQUEST['enable']) {
		$_REQUEST['enable'] = 0;
		$warning = "Не установлена цена, поэтому кейс отключен";
	}
	$case->set_parametrs_from_request();
	$img = '';
	if ($_FILES['upload_image'] != '')
		$img = upload_file('upload_image');
	if ($img)
		$case->set_image($img);
	$item_img = '';
	if ($_FILES['upload_item_image'] != '')
		$item_img = upload_file('upload_item_image');
	if ($item_img)
		$case->set_item_image($item_img);
	$case->set_position($case->get_position_max() + 1);
	$case->add_ocase();
	if ($case->get_type() == ocase::TYPE_PROMOCODE && !empty($_REQUEST['promocode']) && !empty($_REQUEST['promocount'])) {
		$case_id = db()->get_last_id();
		$promocode = new promocode();
		$promocode->set_code($_REQUEST['promocode']);
		$promocode->set_count($_REQUEST['promocount']);
		$promocode->set_type(promocode::TYPE_CASE);
		$promocode->set_case_id($case_id);
		$promocode->set_enable(1);
		$promocode->add_promocode();
	}
	if (!empty($warning)) {
		alertW('Кейс успешно добавлен. ' . $warning, ADMINURL . '/opencase/case/');
	} else {
		alertS('Кейс успешно добавлен', ADMINURL . '/opencase/case/');
	}
}

function admin_opencase_caseeditform($args) {
	$case = new ocase($args[0]);
	$category = new caseCategory($case->get_category());
	$images = '';
	$image_button = '';
	$item_images = '';
	$item_image_button = '';
	if ($case->get_image() == '') {
		$images = '<input type = "file" name="upload_image" id="upload_image">';
		$image_button = '<button class="btn btn-success" type="submit"><i class = "fa fa-upload"></i> Загрузить</button>';
	} else {
		$images = '<img src = "/uploads/' . $case->get_image() . '" alt = "Изображение" class = "img-responsive" style = "margin: 0 auto; padding: 0 10%;">';
		$image_button = '<a href = "' .ADMINURL . '/opencase/casedelimage/' . $case->get_id() . '/" class = "btn btn-danger"><i class = "fa fa-trash"></i> Удалить изображение</a>';
	}
	if ($case->get_item_image() == '') {
		$item_images = '<input type = "file" name="upload_item_image" id="upload_item_image">';
		$item_image_button = '<button class="btn btn-success" type="submit"><i class = "fa fa-upload"></i> Загрузить</button>';
	} else {
		$item_images = '<img src = "/uploads/' . $case->get_item_image() . '" alt = "Изображение" class = "img-responsive" style = "margin: 0 auto; padding: 0 10%;">';
		$item_image_button = '<a href = "' .ADMINURL . '/opencase/casedelitemimage/' . $case->get_id() . '/" class = "btn btn-danger"><i class = "fa fa-trash"></i> Удалить изображение</a>';
	}
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/opencase/caseedit/' . $case->get_id() . '/" enctype="multipart/form-data">
					<div class = "col-lg-9">
						<div class="box">
							<div class = "box-body">
								<div class="form-group">
									<label for="name">Название кейса:</label>
									<input type = "text" class="form-control" name="name" id="name" value = "' . $case->get_name() . '">
								</div>
								
								<div class="form-group">
									<label for="description">Описание:</label>
									<textarea class = "form-control" name = "description" id = "description">' . $case->get_description() . '</textarea>
								</div>
								<div class="form-group">
									<label for="type">Тип:</label>
									<select name = "type" id = "type" class="form-control">
										<option value = "' . ocase::TYPE_DEFAULT . '" ' . ($case->get_type() == ocase::TYPE_DEFAULT ? ' selected = "selected"' : '') . '>Обычный</option>
										<option value = "' . ocase::TYPE_PROMOCODE . '"' . ($case->get_type() == ocase::TYPE_PROMOCODE ? ' selected = "selected"' : '') . '>По промокоду</option>
										<option value = "' . ocase::TYPE_DEPOSITE . '"' . ($case->get_type() == ocase::TYPE_DEPOSITE ? ' selected = "selected"' : '') . '>По депозиту</option>
									</select>
								</div>
								<div class="form-group" id="priceWrapper">
									<label for="price">Цена:</label>
									<input type = "number" class="form-control" name="price" id="price" value = "' . $case->get_price() . '">
								</div>';
	if ($case->get_type() == ocase::TYPE_PROMOCODE) {
		$codes = db()->query('SELECT * FROM promo_code WHERE case_id = ' . $case->get_id());
		$content .= '<div class="form-group" id="promoWrapper">
										<label for="promocode">Промокоды:</label>
										<table class="table table-bordered table-striped">';
		foreach ($codes as $code) {
			$content .= '<tr><td>
													<a href="' .ADMINURL . '/promo/editform/' . $code['id'] . '/">' . $code['code'] . '</a>
												</td></tr>';
		}
		$content .= '<tr><td>
												<a href="' .ADMINURL . '/promo/addform/' . $case->get_id() . '/">Добавить промокод</a>
											</td></tr>
										</table>
									</div>';
	}
	$content .= '<div class="form-group">
									<label for="sale">Скида:</label>
									<input type = "number" class="form-control" name="sale" id="sale" value = "' . $case->get_sale() . '">
								</div>
								<div class="form-group">
									<label for="category">Категория:</label>
									<select name = "category" id = "category" class="form-control">';
	foreach ($category->get_caseCategorys() as $cat) {
		$content .= '<option value = "' . $cat->get_id() . '"' . ($cat->get_id() == $category->get_id() ? ' selected = "selected"' : '') . '>' . $cat->get_name() . '</option>';
	}
	$content .= '</select>
								</div>
								<div class="form-group">
									<label for="rarity">Редкость:</label>
									<select name = "rarity" id = "rarity" class="form-control">';
	foreach ($case->get_rarity_array() as $key => $label) {
		$content .= '<option value = "' . $key . '"' . ($case->get_rarity() == $key ? ' selected = "selected"' : '') . '>' . $label . '</option>';
	}
	$content .= '</select>
								</div>
								<div class="form-group">
									<label for="enable">Включен:</label>
									<select name = "enable" id = "enable" class="form-control">
										<option value = "1"' . ($case->get_enable() ? ' selected = "selected"' : '') . '>Включен</option>
										<option value = "0"' . ($case->get_enable() ? '' : ' selected = "selected"') . '>Отключен</option>
									</select>
								</div>
								<div class="form-group">
									<label for="label">Ярлык:</label>
									<input type = "text" class="form-control" name="label" id="label" value = "' . $case->get_label() . '">
								</div>
								<div class="form-group">
									<label for="chance">Изменение шанса:</label>
									<input type = "number" class="form-control" name="chance" id="chance" value = "' . $case->get_chance() . '">
								</div>
								<div class="form-group">
									<label for="key">Уникальный ключ:</label>
									<input type = "text" class="form-control" name="key" id="key" value = "' . $case->get_key() . '">
								</div>
								<div class="form-group">
									<label for="max_open_count">Максимальное количество открытий</label>
									<input type = "text" class="form-control" name="max_open_count" id="max_open_count" value = "' . $case->get_max_open_count() . '">
								</div>
								<div class="form-group" id="depositSumWrap">
									<label for="dep_for_open">Минимальная сумма депозита для открытия</label>
									<input type = "text" class="form-control" name="dep_for_open" id="dep_for_open" value = "' . $case->get_dep_for_open() . '">
								</div>
								<div class="form-group" id="depositCountWrap">
									<label for="dep_open_count">Количество бесплатных открытий</label>
									<input type = "text" class="form-control" name="dep_open_count" id="dep_open_count" value = "' . $case->get_dep_open_count() . '">
								</div>
								<div class="form-group">
									<label for="time_limit">Включен до</label>
									<input type = "text" class="form-control datepicker" name="time_limit" id="time_limit" value = "' . (empty($case->get_time_limit()) ? '' :  date('d.m.Y H:i', $case->get_time_limit())) . '">
								</div>
							</div>
							<div class = "box-footer">
								<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
								<a href = "' .ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/" class = "btn btn-primary"><i class = "fa fa-suitcase"></i> Управление содержимым</a>
							</div>
						</div>
					</div>
					<div class = "col-lg-3">
						<div class="box">
							<div class = "box-header with-border">
								Изображение кейса
							</div>
							<div class = "box-body">
								' . $images . '
							</div>
							<div class = "box-footer">
								' . $image_button . '
							</div>
						</div>
						<!--div class="box">
							<div class = "box-header with-border">
								Изображение предмета
							</div>
							<div class = "box-body">
								' . $item_images . '
							</div>
							<div class = "box-footer">
								' . $item_image_button . '
							</div>
						</div-->
					</div>
				</form>
			</div>
		';
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
	add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
	add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 300,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
			$("#sale").ionRangeSlider({
			  min: 0,
			  max: 100,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
	add_jscript(' $(function () {
			function onCaseTypeChange(type) {
				if (type == ' . ocase::TYPE_PROMOCODE . ') {
					$("#price").val(0);
					$("#promoWrapper").show();
					$("#priceWrapper").hide();
					$("#depositSumWrap").show();
					$("#depositCountWrap").hide();
					$("#dep_open_count").val(1);
				} else if (type == ' . ocase::TYPE_DEFAULT . ') {
					$("#promoWrapper").hide();
					$("#priceWrapper").show();
					$("#depositSumWrap").hide();
					$("#dep_for_open").val(0);
					$("#depositCountWrap").hide();
					$("#dep_open_count").val(1);
				} else if (type == ' . ocase::TYPE_DEPOSITE . ') {
					$("#price").val(0);
					$("#promoWrapper").hide();
					$("#priceWrapper").hide();
					$("#depositSumWrap").show();
					$("#depositCountWrap").show();
				}
			}
			onCaseTypeChange(' . $case->get_type() . ');
			$("#type").on("change", function() {
				let type = $(this).val();
				onCaseTypeChange(type);
			});
			$.datetimepicker.setLocale("ru");
			$(".datepicker").datetimepicker({format:"d.m.Y H:i"});
		});');
	add_breadcrumb('Управление кейсами', ADMINURL . '/opencase/case/', 'fa-suitcase');
	set_active_admin_menu('case');
	set_title('Редактирование кейса');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_caseedit($args) {
	if (empty($_REQUEST['price'])) {
		$_REQUEST['price'] = 0;
	}
	$warning = '';
	if ($_REQUEST['type'] == ocase::TYPE_DEFAULT && $_REQUEST['price'] <= 0 && $_REQUEST['enable']) {
		$_REQUEST['enable'] = 0;
		$warning = "Не установлена цена, поэтому кейс отключен";
	}
	$case = new ocase($args[0]);
	$case->set_parametrs_from_request();
	$img = '';
	if (isset($_FILES['upload_image']) && $_FILES['upload_image'] != '')
		$img = upload_file('upload_image');
	if ($img)
		$case->set_image($img);
	$item_img = '';
	if (isset($_FILES['upload_item_image']) && $_FILES['upload_item_image'] != '')
		$item_img = upload_file('upload_item_image');
	if ($item_img)
		$case->set_item_image($item_img);
	$case->update_ocase();
	if (!empty($warning)) {
		alertW('Изменения успешно сохранены. ' . $warning, ADMINURL . '/opencase/caseeditform/' . $case->get_id() . '/');
	} else {
		alertS('Изменения успешно сохранены', ADMINURL . '/opencase/caseeditform/' . $case->get_id() . '/');
	}
}

function admin_opencase_casedelimage($args) {
	$case = new ocase($args[0]);
	unlink('uploads/' . $case->get_image());
	$case->set_image('');
	$case->update_ocase();
	alertS('Миниатюра успешно удалена', ADMINURL . '/opencase/caseeditform/' . $case->get_id() . '/');
}

function admin_opencase_casedelitemimage($args) {
	$case = new ocase($args[0]);
	unlink('uploads/' . $case->get_item_image());
	$case->set_item_image('');
	$case->update_ocase();
	alertS('Миниатюра успешно удалена', ADMINURL . '/opencase/caseeditform/' . $case->get_id() . '/');
}

function admin_opencase_casedelete($args) {
	$case = new ocase($args[0]);
	$case->delete_ocase();
	alertS('Кейс успешно удален', ADMINURL . '/opencase/case/');
}

function admin_opencase_caseitems($args) {
	$case = new ocase($args[0]);
	$count_items = db()->query_once('select count(id) from opencase_itemincase where case_id = "' . $case->get_id() . '"');
	$count_items = $count_items['count(id)'];
	$content = '
			<div class = "row">
				<div class = "col-md-12">
					<div class = "box">
						<div class = "box-body">
							<div class = "row">
								<div class = "col-md-3">
									<img src = "/uploads/' . $case->get_image() . '" alt = "Изображение" class = "img-responsive" style = "margin: 0 auto; padding: 10px 10%;">
								</div>
								<div class = "col-md-9">
									<div class = "table-responsive">
										<div class = "box-body">
											<table class = "table table-striped">
												<tr>
												  <th>Название</th> <td>' . $case->get_name() . '</td>
												</tr>
												<tr>
												  <th>Цена</th> <td>' . $case->get_sum_label() . '</td>
												</tr>
												<tr>
												  <th>Категория</th> <td>' . $case->get_category_class()->get_name() . '</td>
												</tr>
												<tr>
												  <th>Включен</th> <td>' . $case->get_label_enable() . '</td>
												</tr>
												<tr>
												  <th>Описание</th> <td>' . $case->get_description() . '</td>
												</tr>
												<tr>
												  <th>Ярлык</th> <td>' . $case->get_label() . '</td>
												</tr>
												<tr>
												  <th>Количество предметов</th> <td>' . $count_items . '</td>
												</tr>
											</table>
										</div>
									</div>
								</div>	
							</div>	
						</div>	
						<div class = "box-footer">
							<a href = "' .ADMINURL . '/opencase/caseeditform/' . $case->get_id() . '/" class = "btn btn-success"><i class = "fa fa-pencil"></i> Редактировать кейс</a>
							<a href="' .ADMINURL . '/opencase/case/' . $case->get_id() . '/items/chance/calc/" class="btn btn-primary"><i class="fa fa-calculator"></i> Рассчитать шансы предметов</a>
							<a href="' .ADMINURL . '/opencase/case/' . $case->get_id() . '/items/chance/reset/" class="btn btn-primary"><i class="fa fa-repeat"></i> Сбросить шансы предметов</a>
						</div>
					</div>
				</div>';
				$itemincase = new itemincase();
				$allitems = $itemincase->get_itemincases('case_id = "' . $case->get_id() . '"', 'position ASC, id ASC');
				$allWithdrawable = false;
				$allUsable = false;
				if (is_array($allitems)) {
					foreach ($allitems as $item) {
						if (!$allWithdrawable && $item->get_withdrawable()) {
							$allWithdrawable = true;
						}
						if (!$allUsable && $item->get_usable()) {
							$allUsable = true;
						}
					}
				}
				$content .= '<div class = "col-md-12">
					<div class = "box">
						<div class = "box-header with-border">
							Предметы в кейсе
						</div>
						<div class = "box-body">
							<table class = "table table-bordered table-striped" id = "caseItems">
								<thead>
									<tr>
										<th>ID</th>
										<th>Изображение</th>
										<th>Название</th>
										<th>Количество</th>
										<th>В наличии</th>
										<th>Цена</th>
										<th>Шанс</th>
										<th>Вывод<a href="#" class="change-all-withdrawable" style="margin-left: 10px"><i class = "fa ' . ($allWithdrawable ? 'fa-toggle-on' : 'fa-toggle-off') . '"></i></a></th>
										<th>Использование<a href="#" class="change-all-usable" style="margin-left: 10px"><i class = "fa ' . ($allUsable ? 'fa-toggle-on' : 'fa-toggle-off') . '"></i></a></th>
										<th>Включен</th>
										<th width = "30px"></th>
										<th width = "30px"></th>
									</tr>
								</thead>
								<tbody>';
	if (is_array($allitems)) {
		foreach ($allitems as $item) {
			$content .= '
											<tr id = "item_' . $item->get_id() . '">
												<td>' . $item->get_id() . '</td>
												<td><img src = "' . $item->get_item_class()->get_steam_image('40f', '30f') . '" alt = "' . $item->get_item_class()->get_name() . '"></td>
												<td>' . $item->get_item_class()->get_name() . '</td>
												<td>' . $item->get_text_count_items() . '</td>
												<td>' . $item->get_item_class()->get_count_on_bot() . '</td>
												<td>' . $item->get_item_class()->get_price() . '</td>
												<td>' . $item->get_chance() . '</td>
												<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/' . $item->get_id() . '/" class="change-withdrawable" data-id="'.$item->get_id().'"><i class = "fa ' . ($item->get_withdrawable() ? 'fa-toggle-on' : 'fa-toggle-off') . '"></i></a></td>
												<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/' . $item->get_id() . '/" class="change-usable" data-id="'.$item->get_id().'"><i class = "fa ' . ($item->get_usable() ? 'fa-toggle-on' : 'fa-toggle-off') . '"></i></a></td>
												<td>' . $item->get_label_enabled() . '</td>
												<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/' . $item->get_id() . '/"><i class = "fa fa-pencil"></i></a></td>
												<td><a href = "' .ADMINURL . '/opencase/deleteitemincase/' . $item->get_id() . '/"><i class = "fa fa-trash"></i></td>
											</tr>
										';
		}
	}

	$content .= '
								</tbody>
							</table>
						</div>
					</div>
				</div>
			
		';
	$item = new item();
	$where = '1 = 0';
	$name = !empty($_POST['name']) ? $_POST['name'] : '';
	if (!empty($name)) {
		$where = 'name like "%' . db()->nomysqlinj(trim($name)) . '%"';
	}
	$allitems = $item->get_items($where, 'id DESC');
	$content .= '
			<div class="col-xs-12">
				<div class="box">
					<div class = "box-header with-border">
						<form action = "' .ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/" method = "POST" id = "itemsSearchForm">
							<div class = "row">
								<div class = "col-md-11">
									<input type = "text" name = "name" value = "' . $name . '" placeholder = "Название предмета" class = "form-control">
								</div>
								<div class = "col-md-1">
									<button type = "submit" class = "btn btn-primary pull-right"><i class = "fa fa-search"></i> Поиск</button>
								</div>
							</div>
						</form>
					</div>
					<div class="box-body">
						<table class = "table table-bordered table-striped" id = "itemsSearchTable">
							<thead>
								<tr>
									<th>ID</th>
									<th>Название</th>
									<th>Изображение</th>
									<th>В наличии</th>
									<th>Цена</th>
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
					<td>' . $value->get_count_on_bot() . '</td>
					<td>' . $value->get_price() . '</td>
					<td>	
						<a href="' .ADMINURL . '/opencase/additemincaseform/' . $case->get_id() . '/' . $value->get_id() . '/" title="Добавить предмет" id = "itemsSearchAdd" data-id = "' . $value->get_id() . '"><i class = "fa fa-plus"></i></a>
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
		add_jscript('
			$(document).on("click", ".change-withdrawable", function() {
				let clickedLins = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/itemsincase/changewithdrawable/"  + clickedLins.data("id") + "/",
					dataType: "json",
					type: "POST",
					success: function(data) { 
						if (!data.success) {
							console.error("Ошибка загрузки данных");
							return;
						}
						let toggleIcon = clickedLins.find("i.fa");
						if (toggleIcon.length > 0) {
							if (data.withdrawable) {
								toggleIcon.removeClass("fa-toggle-off").addClass("fa-toggle-on");
							} else {
								toggleIcon.removeClass("fa-toggle-on").addClass("fa-toggle-off");
							}
						}
						if ($(".change-withdrawable i.fa.fa-toggle-on").length > 0) {
							$(".change-all-withdrawable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
						} else {
							$(".change-all-withdrawable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
						}
					},
					error: function() {
						console.error("Ошибка загрузки данных");
					}
				});
				return false;	
			});
			
			$(document).on("click", ".change-all-withdrawable", function() {
				let clickedLins = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/itemsincase/changewithdrawable/all/'.$case->get_id().'/",
					dataType: "json",
					type: "POST",
					success: function(data) { 
						if (!data.success) {
							console.error("Ошибка загрузки данных");
							return;
						}
						let toggleIcon = clickedLins.find("i.fa");
						if (toggleIcon.length > 0) {
							if (data.withdrawable) {
								toggleIcon.removeClass("fa-toggle-off").addClass("fa-toggle-on");
							} else {
								toggleIcon.removeClass("fa-toggle-on").addClass("fa-toggle-off");
							}
						}
						if (data.withdrawable) {
							$(".change-withdrawable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
						} else {
							$(".change-withdrawable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
						}
					},
					error: function() {
						console.error("Ошибка загрузки данных");
					}
				});
				return false;	
			});
			

			
			$(document).on("click", ".change-usable", function() {
				let clickedLins = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/itemsincase/changeusable/"  + clickedLins.data("id") + "/",
					dataType: "json",
					type: "POST",
					success: function(data) { 
						if (!data.success) {
							console.error("Ошибка загрузки данных");
							return;
						}
						let toggleIcon = clickedLins.find("i.fa");
						if (toggleIcon.length > 0) {
							if (data.usable) {
								toggleIcon.removeClass("fa-toggle-off").addClass("fa-toggle-on");
							} else {
								toggleIcon.removeClass("fa-toggle-on").addClass("fa-toggle-off");
							}
						}
						if ($(".change-usable i.fa.fa-toggle-on").length > 0) {
							$(".change-all-usable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
						} else {
							$(".change-all-usable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
						}
					},
					error: function() {
						console.error("Ошибка загрузки данных");
					}
				});
				return false;	
			});
			
			$(document).on("click", ".change-all-usable", function() {
				let clickedLins = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/itemsincase/changeusable/all/'.$case->get_id().'/",
					dataType: "json",
					type: "POST",
					success: function(data) { 
						if (!data.success) {
							console.error("Ошибка загрузки данных");
							return;
						}
						let toggleIcon = clickedLins.find("i.fa");
						if (toggleIcon.length > 0) {
							if (data.usable) {
								toggleIcon.removeClass("fa-toggle-off").addClass("fa-toggle-on");
							} else {
								toggleIcon.removeClass("fa-toggle-on").addClass("fa-toggle-off");
							}
						}
						if (data.usable) {
							$(".change-usable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
						} else {
							$(".change-usable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
						}
					},
					error: function() {
						console.error("Ошибка загрузки данных");
					}
				});
				return false;	
			});
		');
	add_jscript('$("#caseItems tbody").sortable({
			update: function(event, ui) {
				var order = $(this).sortable("toArray");
				var data = [];
				for (var i = 0; i < order.length; i++) {
					data.push(order[i].replace("item_", "") + ":" + i);
				}
				data = data.join(";");
				var sortElem = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/updateitempos/",
					data: "positions=" + data,
					dataType: "json",
					type: "POST",
					success: function(data){ 
						if (data.success) {
							
						} else {
							sortElem.sortable("cancel");
						}
					},
					error: function() {
						sortElem.sortable("cancel");
					}
				});
			}
		}); ');
	add_jscript('$("#itemsSearchForm").on("submit", function() { 
			$.ajax({
				url: "' .ADMINURL . '/api/opencase/searchitemsincase/",
				data: "name=" + $("#itemsSearchForm input[name=name]").val() + "&case=' . $case->get_id() . '",
				dataType: "json",
				type: "POST",
				success: function(data) { 
					if (!data.success) {
						console.error("Ошибка загрузки данных");
						return;
					}
					var html = "";
					data.items.forEach(function(item) {
						html += \'\
							<tr>\
								<td>\' + item.id + \'</td>\
								<td>\' + item.name + \'</td>\
								<td><img src = "\' + item.image + \'"></td>\
								<td>\' + item.count + \'</td>\
								<td>\' + item.price + \' руб</td>\
								<td>\
									<a href="' .ADMINURL . '/opencase/additemincaseform/\' + item.case + \'/\' + item.id + \'/" title="Добавить предмет" id = "itemsSearchAdd" data-id = "\' + item.id + \'"><i class = "fa fa-plus"></i></a>\
								</td>\
							</tr>\
						\';
					});
					$("#itemsSearchTable tbody").html(html);
				},
				error: function() {
					console.error("Ошибка загрузки данных");
				}
			});
			return false;
		});');
	add_jscript('$(document).on("click", "#itemsSearchAdd", function() {
			$.ajax({
				url: "' .ADMINURL . '/api/opencase/searchitemsincaseadd/",
				data: "id=" + $(this).data("id") + "&case=' . $case->get_id() . '",
				dataType: "json",
				type: "POST",
				success: function(data) { 
					if (!data.success) {
						console.error("Ошибка загрузки данных");
						return;
					}
					var html = \'\
						<tr id = "item_\' + data.item.id + \'">\
							<td>\' + data.item.id + \'</td>\
							<td><img src = "\' + data.item.image + \'" alt = "\' + data.item.name + \'"></td>\
							<td>\' + data.item.name + \'</td>\
							<td>\' + data.item.count + \'</td>\
							<td>\' + data.item.count_on_bot + \'</td>\
							<td>\' + data.item.price + \' руб</td>\
							<td>\' + data.item.chance + \'</td>\
							<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/\' + data.item.id + \'/" class="change-withdrawable" data-id="\'+ data.item.id +\'"><i class = "fa \' + (data.item.withdrawable ? \'fa-toggle-on\' : \'fa-toggle-off\') + \'"></i></a></td>\
							<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/\' + data.item.id + \'/" class="change-usable" data-id="\'+ data.item.id +\'"><i class = "fa \' + (data.item.usable ? \'fa-toggle-on\' : \'fa-toggle-off\') + \'"></i></a></td>\
							<td>\' + data.item.label + \'</td>\
							<td><a href = "' .ADMINURL . '/opencase/edititemincaseform/\' + data.item.id + \'/"><i class = "fa fa-pencil"></i></a></td>\
							<td><a href = "' .ADMINURL . '/opencase/deleteitemincase/\' + data.item.id + \'/"><i class = "fa fa-trash"></i></td>\
						</tr>\
					\';
					$("#caseItems tbody").append(html);
					if ($(".change-withdrawable i.fa.fa-toggle-on").length > 0) {
						$(".change-all-withdrawable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
					} else {
						$(".change-all-withdrawable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
					}
					if ($(".change-usable i.fa.fa-toggle-on").length > 0) {
						$(".change-all-usable i.fa").removeClass("fa-toggle-off").addClass("fa-toggle-on");
					} else {
						$(".change-all-usable i.fa").removeClass("fa-toggle-on").addClass("fa-toggle-off");
					}
				},
				error: function() {
					console.error("Ошибка загрузки данных");
				}
			});
			return false;	
		})');
	add_breadcrumb('Управление кейсами', ADMINURL . '/opencase/case/', 'fa-suitcase');
	set_active_admin_menu('case');
	set_title('Управление содержимым кейса');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_additemincaseform($args) {
	$case = new ocase($args[0]);
	$item = new item($args[1]);
	$content = '
		<div class="row">
			<form method = "post" action = "' .ADMINURL . '/opencase/additemincase/' . $case->get_id() . '/' . $item->get_id() . '/" enctype="multipart/form-data">
				<div class="col-lg-10">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="count_items">Количество предметов:</label>
								<input type = "text" class="form-control" name="count_items" id="count_items" value = "-1">
							</div>
							<div class="form-group">
								<label for="chance">Шанс выпадения: </label>
								<input type = "text" class="form-control" name="chance" id="chance" value = "100">
							</div>
							<div class="form-group">
								<label for="enabled">Включен:</label>
								<select name = "enabled" id = "enabled" class = "form-control">
									<option value = "1">Включен</option>
									<option value = "0">Отключен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить предмет</button>
							<a href = "' .ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/" class = "btn btn-primary"><i class = "fa fa-suitcase"></i> Вернуться к кейсу</a>
						</div>
					</div>
				</div>
				<div class = "col-lg-2">
					<div class="box">
						<div class = "box-header with-border">
							Предмет
						</div>
						<div class = "box-body box-profile">
							<img class="profile-user-img img-responsive img-circle" src="' . $item->get_steam_image('128f', '128f') . '">
							<h3 class="profile-username text-center">' . $item->get_name() . '</h3>
							<p class="text-muted text-center" style = "color : rgb(' . $item->get_quality_color() . ')">' . $item->get_text_quality() . '</p>
						</div>
					</div>
				</div>
			</form>
		</div>
		';
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
	add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
	add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 300,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
	add_breadcrumb('Управление кейсами', ADMINURL . '/opencase/case/', 'fa-suitcase');
	add_breadcrumb('Кейс "' . $case->get_name() . '"', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/', 'fa-suitcase');
	set_active_admin_menu('case');
	set_title('Добавление предмета');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_additemincase($args) {
	$case = new ocase($args[0]);
	$item = new item($args[1]);
	$count = db()->query_once('select count(id) from opencase_itemincase where case_id = "' . $case->get_id() . '" and item_id = "' . $item->get_id() . '"');
	$count = $count['count(id)'];
	if ($count == 0) {
		$itemincase = new itemincase();
		$itemincase->set_case_id($case->get_id());
		$itemincase->set_item_id($item->get_id());
		$itemincase->set_parametrs_from_request();
		$itemincase->set_position($itemincase->get_position_max($case->get_id()) + 1);
		$itemincase->add_itemincase();
		alertS('Предмет успешно добавлен в кейс', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/');
	} else {
		alertE('Этот предмет уже добавлен в кейс', ADMINURL . '/opencase/additemincaseform/' . $case->get_id() . '/' . $item->get_id() . '/');
	}
}

function admin_opencase_edititemincaseform($args) {
	$itemincase = new itemincase($args[0]);
	$case = new ocase($itemincase->get_case_id());
	$item = new item($itemincase->get_item_id());
	$content = '
		<div class="row">
			<form method = "post" action = "' .ADMINURL . '/opencase/edititemincase/' . $itemincase->get_id() . '/" enctype="multipart/form-data">
				<div class="col-lg-10">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="count_items">Количество предметов:</label>
								<input type = "text" class="form-control" name="count_items" id="count_items" value = "' . $itemincase->get_count_items() . '">
							</div>
							<div class="form-group">
								<label for="chance">Шанс выпадения: </label>
								<input type = "text" class="form-control" name="chance" id="chance" value = "' . $itemincase->get_chance() . '">
							</div>
							<div class="form-group">
								<label for="withdrawable">Вывод:</label>
								<select name = "withdrawable" id = "withdrawable" class = "form-control">
									<option value = "1"' . ($itemincase->get_withdrawable() ? ' selected = "selected"' : '') . '>Включен</option>
									<option value = "0"' . ($itemincase->get_withdrawable() ? '' : ' selected = "selected"') . '>Отключен</option>
								</select>
							</div>
							<div class="form-group">
								<label for="usable">Использование:</label>
								<select name = "usable" id = "usable" class = "form-control">
									<option value = "1"' . ($itemincase->get_usable() ? ' selected = "selected"' : '') . '>Включено</option>
									<option value = "0"' . ($itemincase->get_usable() ? '' : ' selected = "selected"') . '>Отключено</option>
								</select>
							</div>
							<div class="form-group">
								<label for="enabled">Включен:</label>
								<select name = "enabled" id = "enabled" class = "form-control">
									<option value = "1"' . ($itemincase->get_enabled() ? ' selected = "selected"' : '') . '>Включен</option>
									<option value = "0"' . ($itemincase->get_enabled() ? '' : ' selected = "selected"') . '>Отключен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
							<a href = "' .ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/" class = "btn btn-primary"><i class = "fa fa-suitcase"></i> Вернуться к кейсу</a>
						</div>
					</div>
				</div>
				<div class = "col-lg-2">
					<div class="box">
						<div class = "box-header with-border">
							Предмет
						</div>
						<div class = "box-body box-profile">
							<img class="profile-user-img img-responsive img-circle" src="' . $item->get_steam_image('128f', '128f') . '">
							<h3 class="profile-username text-center">' . $item->get_name() . '</h3>
							<p class="text-muted text-center" style = "color : rgb(' . $item->get_quality_color() . ')">' . $item->get_text_quality() . '</p>
						</div>
					</div>
				</div>
			</form>
		</div>
		';
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
	add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
	add_jscript(' $(function () {
			$("#chance").ionRangeSlider({
			  min: 0,
			  max: 300,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
		});');
	add_breadcrumb('Управление кейсами', ADMINURL . '/opencase/case/', 'fa-suitcase');
	add_breadcrumb('Кейс "' . $case->get_name() . '"', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/', 'fa-suitcase');
	set_active_admin_menu('case');
	set_title('Редактирование предмета');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_edititemincase($args) {
	$itemincase = new itemincase($args[0]);
	$itemincase->set_parametrs_from_request();
	$itemincase->update_itemincase();
	alertS('Изменения успешно сохранены', ADMINURL . '/opencase/edititemincaseform/' . $itemincase->get_id() . '/');
}

function admin_opencase_deleteitemincase($args) {
	$itemincase = new itemincase($args[0]);
	$case = new ocase($itemincase->get_case_id());
	$itemincase->delete_itemincase();
	alertS('Предмет успешно удален', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/');
}

function admin_opencase_category() {
	$category = new caseCategory();
	$allcategory = $category->get_caseCategorys('', 'pos ASC');
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped" id = "caseCategory">
							<thead>
								<tr>
									<th>ID</th>
									<th>Название</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($allcategory as $value) {
		$content .= '
				<tr id = "category_' . $value->get_id() . '">
					<td>' . $value->get_id() . '</td>
					<td>' . $value->get_name() . '</td>
					<td>
						<a href="' .ADMINURL . '/opencase/categoryeditform/' . $value->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>
						<a href="' .ADMINURL . '/opencase/categorydelete/' . $value->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/opencase/categoryaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить категорию</a>
					</div>
				</div>
			</div>
		</div>
		';
	add_jscript('$("#caseCategory tbody").sortable({
			update: function(event, ui) {
				var order = $(this).sortable("toArray");
				var data = [];
				for (var i = 0; i < order.length; i++) {
					data.push(order[i].replace("category_", "") + ":" + i);
				}
				data = data.join(";");
				var sortElem = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/opencase/updatecatpos/",
					data: "positions=" + data,
					dataType: "json",
					type: "POST",
					success: function(data){ 
						if (data.success) {
							
						} else {
							sortElem.sortable("cancel");
						}
					},
					error: function() {
						sortElem.sortable("cancel");
					}
				});
			}
		}); ');
	set_active_admin_menu('casecategory');
	set_title('Упрвление категориями кейсов');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_categoryaddform() {
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/categoryadd/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя категории: </label>
								<input type = "text" class="form-control" name="name" id="name">
							</div>
							<div class="form-group">
								<label for="disable">Отображение категории: </label>
								<select name = "disable" id = "disable" class="form-control">
									<option value = "0">Включено</option>
									<option value = "1">Выключено</option>
								</select>
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить категорию</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('casecategory');
	add_breadcrumb('Упрвление категориями кейсов', ADMINURL . '/opencase/category/', 'fa-th-list');
	set_title('Добавление категории');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_categoryadd() {
	$category = new caseCategory();
	$category->set_parametrs_from_request();
	$max_pos = db()->query_once('select max(pos) from opencase_category');
	$category->set_pos(($max_pos['max(pos)'] + 1));
	$category->add_caseCategory();
	alertS('Категория успешно добавленна', ADMINURL . '/opencase/category/');
}

function admin_opencase_categoryeditform($args) {
	$category = new caseCategory($args[0]);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/opencase/categoryedit/' . $category->get_id() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя категории: </label>
								<input type = "text" class="form-control" name="name" id="name" value = "' . $category->get_name() . '">
							</div>
							<div class="form-group">
								<label for="disable">Отображение категории: </label>
								<select name = "disable" id = "disable" class="form-control">
									<option value = "0"' . ($category->get_disable() ? '' : ' selected = "selected"') . '>Включено</option>
									<option value = "1"' . ($category->get_disable() ? ' selected = "selected"' : '') . '>Выключено</option>
								</select>
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('casecategory');
	add_breadcrumb('Упрвление категориями кейсов', ADMINURL . '/opencase/category/', 'fa-th-list');
	set_title('Редактирование категории');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_categoryedit($args) {
	$category = new caseCategory($args[0]);
	$category->set_parametrs_from_request();
	$category->update_caseCategory();
	alertS('Изменения успешно сохранены', ADMINURL . '/opencase/categoryeditform/' . $category->get_id() . '/');
}

function admin_opencase_categoryup($args) {
	$category = new caseCategory($args[0]);
	$min_pos = db()->query_once('select min(pos) from opencase_category');
	if ($category->get_pos() > $min_pos['min(pos)']) {
		$prevcategory = db()->query_once('select id from opencase_category where pos < "' . $category->get_pos() . '" order by pos DESC LIMIT 1');
		$prevcategory = new caseCategory($prevcategory['id']);
		$tmppos = $category->get_pos();
		$category->set_pos($prevcategory->get_pos());
		$prevcategory->set_pos($tmppos);
		$category->update_caseCategory();
		$prevcategory->update_caseCategory();
		redirect_srv_msg('', ADMINURL . '/opencase/category/');
	} else {
		alertW('Категория уже имеет самую высокую позицию', ADMINURL . '/opencase/category/');
	}
}

function admin_opencase_categorydown($args) {
	$category = new caseCategory($args[0]);
	$max_pos = db()->query_once('select max(pos) from opencase_category');
	if ($category->get_pos() < $max_pos['max(pos)']) {
		$prevcategory = db()->query_once('select id from opencase_category where pos > "' . $category->get_pos() . '" order by pos ASC LIMIT 1');
		$prevcategory = new caseCategory($prevcategory['id']);
		$tmppos = $category->get_pos();
		$category->set_pos($prevcategory->get_pos());
		$prevcategory->set_pos($tmppos);
		$category->update_caseCategory();
		$prevcategory->update_caseCategory();
		redirect_srv_msg('', ADMINURL . '/opencase/category/');
	} else {
		alertW('Категория уже имеет самую низкую позицию', ADMINURL . '/opencase/category/');
	}
}

function admin_opencase_categorydelete($args) {
	$category = new caseCategory($args[0]);
	$category->delete_caseCategory();
	alertS('Категория успешно удаленна', ADMINURL . '/opencase/category/');
}

function admin_opencase_caseposition() {
	$content = '
		<style>
			.casePosition{text-align: center; height: 140px;cursor:pointer;line-height:140px;}
			.casePosition img{height:90%; width: auto;}
			.sortable-category .box .box-header{cursor: pointer;}
			.case-add-icon{display:block;width:80%;height:100%;background:#f4f4f4;text-align: center;line-height:140px;font-size:30px;margin:0 auto;border-radius:3px;border: 1px solid #ddd;}
		</style>
		<div class="row">
			<div class="col-xs-12 sortable-category">';
	forEach (get_case_category() as $caseCategory) {
		$content .= '
				<div class="box" id = "catefory_' . $caseCategory->get_id() . '">
					<div class = "box-header with-border">
						' . $caseCategory->get_name() . ' <a href="' .ADMINURL . '/opencase/categoryeditform/' . $caseCategory->get_id() . '/" title="Редактировать" class = "pull-right"><i class="fa fa-pencil"></i></a>
					</div>
					<div class="box-body">
						<div class="row">
			';
		$case = new ocase();
		$cases = $case->get_ocases('category = ' . $caseCategory->get_id(), 'position ASC, id ASC');
		forEach ($cases as $case) {
			$content .= '
						<div class="col-lg-2 col-md-3 col-xs-6 casePosition" id = "case_' . $case->get_id() . '">
							<img src = "' . $case->get_src_image() . '" alt = "' . $case->get_name() . '">
						</div>
				';
		}
		$content .= '
						<div class="col-lg-2 col-md-3 col-xs-6">
							<a href = "' .ADMINURL . '/opencase/caseaddform/' . $caseCategory->get_id() . '/" class = "btn-default case-add-icon"><i class = "fa fa-plus"></i></a>
						</div>
						</div>
					</div>
					<div class = "box-footer">
					
					</div>
				</div>
			';
	}
	$content .= '
			</div>
			<div class="col-xs-12">
				<a href = "' .ADMINURL . '/opencase/categoryaddform/" class = "btn btn-default btn-block"><i class = "fa fa-plus"></i> Добавить категорию</a>
			</div>
		</div>
		';
	
		add_jscript('
			$(".box-body .row").sortable({
			items: "> .casePosition",
			update: function (event, ui) {
				var order = $(this).sortable("toArray");
				var data = [];
				for (var i = 0; i < order.length; i++) {
					data.push(order[i].replace("case_", "") + ":" + i);
				}
				data = data.join(";");
				var sortElem = $(this);
				$.ajax({
					url: "' . ADMINURL . '/api/opencase/updatecasepos/",
					data: "positions=" + data,
					dataType: "json",
					type: "POST",
					success: function (data) {
						if (!data.success) {
							sortElem.sortable("cancel");
						}
					},
					error: function () {
						sortElem.sortable("cancel");
					}
				});
			}
		});

		$(".sortable-category").sortable({
			handle: ".box-header",
			update: function (event, ui) {
				var order = $(this).sortable("toArray");
				var data = [];
				for (var i = 0; i < order.length; i++) {
					data.push(order[i].replace("catefory_", "") + ":" + i);
				}
				data = data.join(";");
				var sortElem = $(this);
				$.ajax({
					url: "' . ADMINURL . '/api/opencase/updatecatpos/",
					data: "positions=" + data,
					dataType: "json",
					type: "POST",
					success: function (data) {
						if (!data.success) {
							sortElem.sortable("cancel");
						}
					},
					error: function () {
						sortElem.sortable("cancel");
					}
				})
			}
		});
	');
	set_active_admin_menu('caseposition');
	set_title('Управление позициями');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_calc_all_cases_items_chance() {
	$ocase = new ocase();
	$cases= $ocase->get_ocases();
	foreach ($cases as $case) {
		$case->recalc_items_chances();
	}
	ch()->flush();
	alertS('Шансы предметов в кейсах перерасчитаты в зависимости от цен', ADMINURL . '/opencase/case/');
}

function admin_opencase_reset_all_cases_items_chance() {
	db()->query_once('UPDATE `opencase_itemincase` SET `chance` = 100;');
	ch()->flush();
	alertS('Шансы предметов в кейсах сброшены на начальные', ADMINURL . '/opencase/case/');
}

function admin_opencase_calc_case_items_chance($args) {
	$case = new ocase($args[0]);
	if ($case->get_id() != '') {
		$case->recalc_items_chances();
		ch()->flush();
		alertS('Шансы предметов в кейсе перерасчитаты в зависимости от цен', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/');
	}
	alertE('Keйс не найден', ADMINURL . '/opencase/case/');
}

function admin_opencase_reset_case_items_chance($args) {
	$case = new ocase($args[0]);
	if ($case->get_id() != '') {
		db()->query_once('UPDATE `opencase_itemincase` SET `chance` = 100 WHERE `case_id` = "' . $case->get_id() . '";');
		ch()->flush();
		alertS('Шансы предметов в кейсе сброшены на начальные', ADMINURL . '/opencase/caseitems/' . $case->get_id() . '/');
	}
	alertE('Keйс не найден', ADMINURL . '/opencase/case/');
}
