<?php

add_admin_get('/faq/(([0-9]+)/)?', 'admin_faq');
add_admin_get('/faqaddform/', 'admin_faqaddform');
add_admin_post('/faqadd/', 'admin_faqadd');
add_admin_get('/faqeditform/([0-9]+)/', 'admin_faqeditform');
add_admin_post('/faqedit/([0-9]+)/', 'admin_faqedit');
add_admin_get('/faqdelete/([0-9]+)/', 'admin_faqdelete');

function admin_faq($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$pages = new Pages();
	$pages->set_num_object(FAQElement::getTotalCount());
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/faq/{p}/');
	$pages->set_first_url(ADMINURL . '/faq/');
	$pages->set_curent_page($page);
	$faqRows = FAQElement::getQuestions($page, get_setval('admin_in_page'));
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped" id="FAQElements">
							<thead>
								<tr>
									<th>ID</th>
									<th>Вопрос</th>
									<th>Ответ</th>
									<th>Включен</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($faqRows as $row) {
		$content .= '
				<tr id = "item_' . $row['id'] . '">
					<td>' . $row['id'] . '</td>
					<td>' . $row['question'] . '</td>
					<td>' . $row['answer'] . '</td>
					<td>' . ($row['enabled'] ? '<span class = "label label-success">Включен</span>' : '<span class = "label label-danger">Отключен</span>') . '</td>
					<td>	
						<a href="' .ADMINURL . '/faqeditform/' . $row['id'] . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>	
						<a href="' .ADMINURL . '/faqdelete/' . $row['id'] . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a href="' .ADMINURL . '/faqaddform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить вопрос</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	add_jscript('$("#FAQElements tbody").sortable({
			update: function(event, ui) {
				var order = $(this).sortable("toArray");
				var data = [];
				for (var i = 0; i < order.length; i++) {
					data.push(order[i].replace("item_", "") + ":" + i);
				}
				data = data.join(";");
				var sortElem = $(this);
				$.ajax({
					url: "' .ADMINURL . '/api/updatefaqpos/",
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
	set_active_admin_menu('faq');
	set_title('Упрвление FAQ');
	set_content($content);
	set_tpl('index.php');
}

function admin_faqaddform() {
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/faqadd/">
						<div class="box-body">
							<div class="form-group">
								<label for="question">Вопрос:</label>
								<textarea class = "form-control" name = "question" id = "question"></textarea>
							</div>
							<div class="form-group">
								<label for="answer">Ответ:</label>
								<textarea class = "form-control" name = "answer" id = "answer"></textarea>
							</div>
							<div class="form-group">
								<label for="enabled">Включен: </label>
								<select id = "enabled" name = "enabled" class = "form-control">
									<option value = "1">Включен</option>
									<option value = "0">Отключен</option>
								</select>
							</div>
						</div>
						<div class="box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить вопрос</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
	set_active_admin_menu('faqadd');
	add_breadcrumb('Упрвление FAQ', ADMINURL . '/faq/', 'fa-cog');
	set_title('Добавление вопроса');
	set_content($content);
	set_tpl('index.php');
}

function admin_faqadd() {
	if (!empty($_POST['question']) && !empty($_POST['answer'])) {
		$question = new FAQElement();
		$question->fromRequest();
		$question->save();
		alertS('Вопрос успешно добавлен', ADMINURL . '/faq/');
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/faqaddform/');
	}
}

function admin_faqeditform($args) {
	$question = new FAQElement($args[0]);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">	
					<form method = "post" action = "' .ADMINURL . '/faqedit/' . $question->getId() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="question">Вопрос:</label>
								<textarea class = "form-control" name = "question" id = "question">' . $question->getQuestion() . '</textarea>
							</div>
							<div class="form-group">
								<label for="answer">Ответ:</label>
								<textarea class = "form-control" name = "answer" id = "answer">' . $question->getAnswer() . '</textarea>
							</div>
							<div class="form-group">
								<label for="enabled">Включен: </label>
								<select id = "enabled" name = "enabled" class = "form-control">
									<option value = "1"' . ($question->getEnabled() ? ' selected = "selected"' : '') . '>Включен</option>
									<option value = "0"' . ($question->getEnabled() ? '' : ' selected = "selected"') . '>Отключен</option>
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
	set_active_admin_menu('faq');
	add_breadcrumb('Упрвление FAQ', ADMINURL . '/faq/', 'fa-cog');
	set_title('Редактирование вопроса');
	set_content($content);
	set_tpl('index.php');
}

function admin_faqedit($args) {
	if (!empty($_POST['question']) && !empty($_POST['answer'])) {
		$question = new FAQElement($args[0]);
		$question->fromRequest();
		$question->save();
		alertS('Вопрос успешно обновлен', ADMINURL . '/faq/');
	} else {
		alertE('Не все поля заполнены', ADMINURL . '/faqaddform/');
	}
}

function admin_faqdelete($args) {
	$question = new FAQElement($args[0]);
	$question->delete();
	alertS('Вопрос успешно удален', ADMINURL . '/faq/');
}
