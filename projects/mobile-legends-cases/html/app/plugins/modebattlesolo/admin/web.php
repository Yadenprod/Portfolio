<?php

add_admin_get('/mode/battle/(([0-9]+)/)?', 'admin_opencase_mode_battle');
add_admin_get('/mode/battle/cases/', 'admin_opencase_mode_battle_cases');
add_admin_get('/mode/battle/cases/add/', 'admin_opencase_mode_battle_cases_addform');
add_admin_post('/mode/battle/cases/add/', 'admin_opencase_mode_battle_cases_add');
add_admin_get('/mode/battle/cases/delete/([0-9]+)/', 'admin_opencase_mode_battle_cases_delete');
add_admin_post('/api/updatecaseinabettlepos/', 'admin_updatecaseinabettlepos');

function admin_opencase_mode_battle($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$pages = new Pages();
	$pages->set_num_object(battle::getBattlesCount());
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/mode/battle/{p}/');
	$pages->set_first_url(ADMINURL . '/mode/battle/');
	$pages->set_curent_page($page);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class="table table-bordered table-striped" id="FAQElements">
							<thead>
								<tr>
									<th>ID</th>
									<th>Создатель</th>
									<th>Участник</th>
									<th>Цена</th>
									<th>Профит</th>
									<th>Время</th>
									<th>Статус</th>
								</tr>
							</thead>								
							<tbody>
					';
	$allBattles = battle::getBattles('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	foreach ($allBattles as $value) {
		if ($value->getProfit() > 0) {
			$labelClass = 'label-success';
		} else if ($value->getProfit() < 0) {
			$labelClass = 'label-danger';
		} else {
			$labelClass = 'label-warning';
		}
		$content .= '
										<tr>
											<td>' . $value->getId() . '</td>
											<td><a href="' . ADMINURL . '/opencase/user/' . $value->getCreatorId() . '/">' . $value->getCreator()->get_name() . '</a>' . $value->getWonLabelByUserId($value->getCreatorId()) . '</td>';
		if (is_null($participant = $value->getParticipant())) {
			$content .= '<td>-</td>';
		} else {
			$content .= '<td><a href="' . ADMINURL . '/opencase/user/' . $participant->get_id() . '/">' . $participant->get_name() . '</a>' . $value->getWonLabelByUserId($participant->get_id()) . '</td>';
		}
		$content .= '
											<td>' . $value->getPrice() . '</td>
											<td><span class="label ' . $labelClass . '">' . $value->getProfit() . ' руб</span></td>
											<td>' . $value->getFormatFinishedAt() . '</td>
											<td>' . $value->getLabelStatus() . '</td>
										</tr>
									';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class="box-footer">
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('battlemode');
	set_title('Режим Батл');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_mode_battle_cases($args) {
	$battleCases = caseInBattle::getAllBattleCases();
	$content = '
			<div class="row">
				<div class="col-md-12">
					<div class="box">
						<div class="box-header">
							<a href="' . ADMINURL . '/mode/battle/cases/add/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить кейс</a>
						</div>
						<div class="box-body">
							<table class="table table-bordered table-striped" id="battleCases">
								<thead>
									<tr>
										<th>ID Кейса</th>
										<th>Изображение</th>
										<th>Название</th>
										<th width="30px"></th>
									</tr>
								</thead>
								<tbody>';
	foreach ($battleCases as $value) {
		$content .= '
									<tr id="item_' . $value->getCaseId() . '">
										<td>' . $value->getCaseId() . '</td>
										<td><img src="/uploads/' . $value->getCaseClass()->get_image() . '" style="width: 40px;"></td>
										<td><a href="' . ADMINURL . '/opencase/caseitems/' . $value->getCaseId() . '/">' . $value->getCaseClass()->get_name() . '</a></td>
										<td><a href="' . ADMINURL . '/mode/battle/cases/delete/' . $value->getCaseId() . '/" title="Удалить"><i class="fa fa-trash"></i></a></td>
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
	add_jscript('$("#battleCases tbody").sortable({
			update: function(event, ui) {
				var order=$(this).sortable("toArray");
				var data=[];
				for (var i=0; i < order.length; i++) {
					data.push(order[i].replace("item_", "") + ":" + i);
				}
				data=data.join(";");
				var sortElem=$(this);
				$.ajax({
					url: "' . ADMINURL . '/api/updatecaseinabettlepos/",
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
	add_script(get_admin_template_folder() . '/plugins/deleteConfirm/deleteConfirm.js', 10, 'footer');
	set_active_admin_menu('battlemodecases');
	set_title('Режим Батл');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_mode_battle_cases_delete($args) {
	$battleCase = new caseInBattle($args[0]);
	$battleCase->delete();
	alertS('Кейс больше не доступен для батла', ADMINURL . '/mode/battle/cases/');
}

function admin_updatecaseinabettlepos() {
	$json = array('success' => false);
	if (isset($_POST['positions'])) {
		$position = explode(';', db()->nomysqlinj($_POST['positions']));
		if (is_array($position) && count($position) > 0) {
			foreach ($position as $pos) {
				$data = explode(':', $pos);
				$battleCase = new caseInBattle($data[0]);
				$battleCase->setPosition($data[1]);
				$battleCase->save();
			}
			$json['success'] = true;
		} else {
			$json['error'] = 'Неверные данные';
		}
	} else {
		$json['error'] = 'Не указаны данные для обновления';
	}
	echo_json($json);
}

function admin_opencase_mode_battle_cases_addform() {
	$availCases = caseInBattle::getAvailForAddCases();
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method="post" action="' . ADMINURL . '/mode/battle/cases/add/">
						<div class="box-body">
							<div class="form-group">
								<label for="enabled">Кейс: </label>
								<select name="case" class="form-control">';
	foreach ($availCases as $case) {
		$content .= '
									<option value="' . $case->get_id() . '">' . $case->get_id() . ') ' . $case->get_name() . '</option>
				';
	}
	$content .= '
								</select>
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class="fa fa-plus"></i> Добавить кейс</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('battlemodecases');
	set_title('Режим Батл');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_mode_battle_cases_add() {
	if (!empty($_POST['case'])) {
		$battleCase = new caseInBattle();
		$battleCase->setCaseId(db()->nomysqlinj($_REQUEST['case']));
		$battleCase->setPosition(caseInBattle::getMaxPosition());
		$battleCase->save();
		alertS('Кейс успешно добавлен', ADMINURL . '/mode/battle/cases/');
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/mode/battle/cases/');
	}
}
