<?php

add_admin_get('/promo/(([0-9]+)/)?', 'admin_promo_index');
add_admin_get('/promo/addform/(([0-9]+)/)?', 'admin_promo_addform');
add_admin_post('/promo/add/', 'admin_promo_add');
add_admin_get('/promo/editform/([0-9]+)/', 'admin_promo_editform');
add_admin_post('/promo/edit/([0-9]+)/', 'admin_promo_edit');
add_admin_get('/promo/delete/([0-9]+)/', 'admin_promo_delete');
add_admin_get('/promo/settings/', 'admin_promo_settings');
add_admin_post('/promo/settingssave/', 'admin_promo_settingssave');

function admin_promo_index($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$promocount = db()->query_once('select count(id) from promo_code');
	$pages = new Pages();
	$pages->set_num_object($promocount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/promo/{p}/');
	$pages->set_first_url(ADMINURL . '/promo/');
	$pages->set_curent_page($page);
	$promocodes = new promocode();
	$promocodes = $promocodes->get_promocodes('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class = "row">
			<div class = "col-xs-12">
				<div class = "box">
					<div class = "box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Промокод</th>
									<th>Бонус</th>
									<th>Использованно</th>
									<th>Всего</th>
									<th>Осталось</th>
									<th>Включен</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($promocodes as $promocode) {
		$content .= '
							<tr class = "bold">
								<td>' . $promocode->get_id() . '</td>
								<td>' . $promocode->get_code() . '</td>
								<td>' . $promocode->get_bonus_string() . '</td>
								<td>' . $promocode->get_use() . '</td>
								<td>' . $promocode->get_count() . '</td>
								<td>' . $promocode->get_left() . '</td>
								<td>' . $promocode->get_label_enable() . '</td>
								<td>
									<a href="' .ADMINURL . '/promo/editform/' . $promocode->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
								</td>
								<td>
									<a href="' .ADMINURL . '/promo/delete/' . $promocode->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
								</td>
							</tr>
						';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a class="btn btn-success" href="' .ADMINURL . '/promo/addform/"><i class = "fa fa-plus"></i> Добавить промокод</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('promo');
	set_title('Промокоды');
	set_content($content);
	set_tpl('index.php');
}

function admin_promo_addform($args) {
	if (!empty($args[1])) {
		$case_id = $args[1];
		$type = promocode::TYPE_CASE;
	} else {
		$case_id = false;
		$type = false;
	}
	$ocase = new ocase();
	$promocases = $ocase->get_ocases('type = ' . ocase::TYPE_PROMOCODE, 'id DESC');
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/promo/add/" enctype="multipart/form-data">
				<div class="col-xs-12">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="code">Промокод:</label>
								<div class="input-group">
									<input type = "text" class="form-control" name="code" id="code">
									<div class="input-group-btn">
										<a href = "#" class = "btn btn-primary" id = "generate-promo"><i class = "fa fa-gears"></i> Сгенерировать</a>
									</div>
								</div>
							</div>
							<div class="form-group">
								<label for="type">Тип промокода:</label>
								<select name = "type" id = "type" class = "form-control">
									<option value = "'.promocode::TYPE_SUM.'" ' . ($type == promocode::TYPE_SUM ? ' selected = "selected"' : '') . '>Сумма</option>
									<option value = "'.promocode::TYPE_CASE.'"' . ($type == promocode::TYPE_CASE ? ' selected = "selected"' : '') . '>Кейс</option>
									<option value = "'.promocode::TYPE_PERCENT.'"' . ($type == promocode::TYPE_PERCENT ? ' selected = "selected"' : '') . '>Процент</option>
								</select>
							</div>
							<div class="form-group"  id="caseWrapper" ' . ($type != promocode::TYPE_CASE ? 'style="display:none"' : '') . '>
								<label for="case_id">Кейс:</label>
								<select name = "case_id" id = "case_id" class="form-control">
									<option value = "">Выберите кейс</option>';
									foreach ($promocases as $case) {
										$content .= '<option value = "' . $case->get_id() .'" ' . ($case_id == $case->get_id() ? ' selected = "selected"' : '') . '>' . $case->get_id() . ') ' . $case->get_name() .'</option>';
									}
								$content .=	'</select>
							</div>
							<div class="form-group" id="valueWrapper" ' . ($type == promocode::TYPE_CASE ? 'style="display:none"' : '') . '>
								<label for="value">Бонус:</label>
								<input type = "text" class="form-control" name="value" id="value" value = "10">
							</div>
							<div class="form-group">
								<label for="count">Количество активаций:</label>
								<input type = "number" class="form-control" name="count" id="count" value = "100">
							</div>
							<div class="form-group">
								<label for="enable">Включен:</label>
								<select name = "enable" id = "enable" class="form-control">
									<option value = "1">Включен</option>
									<option value = "0">Отключен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить промокод</button>
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
			let valueRange = null;
			$("#type").on("change", function() {
				let type = $(this).val();
				let value = $("#value");
				if (valueRange) {
					valueRange.destroy();
					valueRange = null;
				}
				if (type == '.promocode::TYPE_SUM.') {
					value.val(10);
					$("#valueWrapper").show();
					$("#caseWrapper").hide();
				} else if (type == '.promocode::TYPE_CASE.') {
					value.val(0);
					$("#caseWrapper").show();
					$("#valueWrapper").hide();
				} else if (type == '.promocode::TYPE_PERCENT.') {
					value.val(10);
					$("#valueWrapper").show();
					$("#caseWrapper").hide();
					value.ionRangeSlider({
						min: 0,
						max: 100,
						type: \'single\',
						step: 1,
						postfix: " %",
						prettify: false,
						hasGrid: true
					});
					valueRange = value.data("ionRangeSlider");
				}
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
				$("#code").val(code);
			});
		});');
	add_breadcrumb('Промокоды', ADMINURL . '/promo/', 'fa-diamond');
	set_active_admin_menu('promoadd');
	set_title('Добавить промокод');
	set_content($content);
	set_tpl('index.php');
}

function admin_promo_add() {
	$promo = new promocode();
	$promo->set_parametrs_from_request();
	$promo->add_promocode();
	alertS('Промокод успешно добавлен', ADMINURL . '/promo/');
}

function admin_promo_editform($args) {
	$ocase = new ocase();
	$promocases = $ocase->get_ocases('type = ' . ocase::TYPE_PROMOCODE, 'id DESC');
	$promo = new promocode($args[0]);
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/promo/edit/' . $promo->get_id() . '/" enctype="multipart/form-data">
				<div class="col-xs-12">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="code">Промокод:</label>
								<input type = "text" class="form-control" name="code" id="code" value = "' . $promo->get_code() . '">
							</div>
							<div class="form-group">
								<label for="type">Тип промокода:</label>
								<select name = "type" id = "type" class = "form-control">
									<option value = "'.promocode::TYPE_SUM.'" '. ($promo->get_type() == promocode::TYPE_SUM ? ' selected = "selected"' : '') . '>Сумма</option>
									<option value = "'.promocode::TYPE_CASE.'" '. ($promo->get_type() == promocode::TYPE_CASE ? ' selected = "selected"' : '') . '>Кейс</option>
									<option value = "'.promocode::TYPE_PERCENT.'" '. ($promo->get_type() == promocode::TYPE_PERCENT ? ' selected = "selected"' : '') . '>Процент</option>
								</select>
							</div>
							<div class="form-group"  id="caseWrapper">
								<label for="case_id">Кейс:</label>
								<select name = "case_id" id = "case_id" class="form-control">
									<option value = "">Выберите кейс</option>';
									foreach ($promocases as $case) {
										$content .= '<option value = "' . $case->get_id() .'"' . ($promo->get_case_id() == $case->get_id() ? ' selected = "selected"' : '') . '>' . $case->get_id() . ') ' . $case->get_name() .'</option>';
									}
								$content .=	'</select>
							</div>
							<div class="form-group" id="valueWrapper">
								<label for="value">Бонус:</label>
								<input type = "text" class="form-control" name="value" id="value" value = "' . $promo->get_value() . '">
							</div>
							<div class="form-group">
								<label for="count">Количество активаций:</label>
								<input type = "number" class="form-control" name="count" id="count" value = "' . $promo->get_count() . '">
							</div>
							<div class="form-group">
								<label for="use">Использованно:</label>
								<input type = "number" class="form-control" name="use" id="use" value = "' . $promo->get_use() . '">
							</div>
							<div class="form-group">
								<label for="enable">Включен:</label>
								<select name = "enable" id = "enable" class="form-control">
									<option value = "1"' . ($promo->get_enable() ? ' selected = "selected"' : '') . '>Включен</option>
									<option value = "0"' . ($promo->get_enable() ? '' : ' selected = "selected"') . '>Отключен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
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
			let valueRange = null;
			let initType = $("#type").val();
			if (initType == '.promocode::TYPE_SUM.') {
				$("#valueWrapper").show();
				$("#caseWrapper").hide();
			} else if (initType == '.promocode::TYPE_CASE.') {
				$("#caseWrapper").show();
				$("#valueWrapper").hide();
			} else if (initType == '.promocode::TYPE_PERCENT.') {
				$("#valueWrapper").show();
				$("#caseWrapper").hide();
				$("#value").ionRangeSlider({
					min: 0,
					max: 100,
					type: \'single\',
					step: 1,
					postfix: " %",
					prettify: false,
					hasGrid: true
				});
				valueRange = $("#value").data("ionRangeSlider");				
			}
			$("#type").on("change", function() {
				let type = $(this).val();
				let value = $("#value");
				if (valueRange) {
					valueRange.destroy();
					valueRange = null;
				}
				if (type == '.promocode::TYPE_SUM.') {
					value.val(10);
					$("#valueWrapper").show();
					$("#caseWrapper").hide();
				} else if (type == '.promocode::TYPE_CASE.') {
					value.val(0);
					$("#caseWrapper").show();
					$("#valueWrapper").hide();
				} else if (type == '.promocode::TYPE_PERCENT.') {
					value.val(10);
					$("#valueWrapper").show();
					$("#caseWrapper").hide();
					value.ionRangeSlider({
						min: 0,
						max: 100,
						type: \'single\',
						step: 1,
						postfix: " %",
						prettify: false,
						hasGrid: true
					});
					valueRange = value.data("ionRangeSlider");
				}
			});
		});');
	add_breadcrumb('Промокоды', ADMINURL . '/promo/', 'fa-diamond');
	set_active_admin_menu('promo');
	set_title('Редактирование промокода');
	set_content($content);
	set_tpl('index.php');
}

function admin_promo_edit($args) {
	$promo = new promocode($args[0]);
	$promo->set_parametrs_from_request();
	$promo->update_promocode();
	alertS('Изменения успешно сохранены', ADMINURL . '/promo/editform/' . $promo->get_id() . '/');
}

function admin_promo_delete($args) {
	$promo = new promocode($args[0]);
	$promo->delete_promocode();
	alertS('Промокод успешно удален', ADMINURL . '/promo/');
}

function admin_promo_settings() {
	$promos = new promocode();
	$promos = $promos->get_promocodes('`type` = '.promocode::TYPE_PERCENT.' and `enable` = 1 and `use` < `count`');
	$options = '';
	foreach ($promos as $promo) {
		$options .= '<option value = "' . $promo->get_id() . '"' . ($promo->get_id() == get_setval('promo_active_code') ? ' selected = "selected"' : '') . '>' . $promo->get_code() . ' (' . $promo->get_left() . ')</option>';
	}
	$content = '
			<div class = "row">
				<div class = "col-xs-12">
					<div class="nav-tabs-custom">
						<ul class="nav nav-tabs">
							<li class="active"><a href="#settings" data-toggle="tab">Настройки</a></li>
						</ul>
						<div class="tab-content">
							<div class="active tab-pane" id="settings">
								<form action = "' .ADMINURL . '/promo/settingssave/" method = "POST">
									<div class = "form-group">
										<label for="promo_active_code">Активный промокод:</label>
										<select name="promo_active_code" id="promo_active_code" class="form-control">
										' . $options . '
										</select>
									</div>
									<div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
								</form>
							</div>
						</div>
					</div>
				</div>
			</div>
		';
	set_active_admin_menu('promosettings');
	set_title('Настройки промокодов');
	set_content($content);
	set_tpl('index.php');
}

function admin_promo_settingssave() {
	update_setval('promo_active_code', $_POST['promo_active_code']);
	alertS('Изменения успешно сохранены', ADMINURL . '/promo/settings/');
}
