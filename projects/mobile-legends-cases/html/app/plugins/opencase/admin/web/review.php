<?php

add_admin_get('/review/(([0-9]+)/)?', 'admin_review_index');
add_admin_get('/review/addform/', 'admin_review_addform');
add_admin_post('/review/add/', 'admin_review_add');
add_admin_get('/review/editform/([0-9]+)/', 'admin_review_editform');
add_admin_post('/review/edit/([0-9]+)/', 'admin_review_edit');
add_admin_get('/review/delete/([0-9]+)/', 'admin_review_delete');

function admin_review_index($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$reviewcount = db()->query_once('select count(id) from opencase_reviews');
	$pages = new Pages();
	$pages->set_num_object($reviewcount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/review/{p}/');
	$pages->set_first_url(ADMINURL . '/review/');
	$pages->set_curent_page($page);
	$reviews = review::get_reviews('', array('time_add' => 'DESC'), (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
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
									<th>Комментарий</th>
									<th>Предмет</th>
									<th>Модерация</th>
									<th>Дата</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($reviews as $review) {
		$content .= '
							<tr class = "bold">
								<td>' . $review->get_id() . '</td>
								<td><a href = "' .ADMINURL . '/opencase/user/' . $review->get_user_id() . '/">' . $review->get_user()->get_name() . '</a></td>
								<td>' . str_replace(['\\\r', '\\\n'], ['', '<br>'], $review->get_text()) . '</td>
								<td>' . ($review->get_item()->get_id() ? $review->get_item()->get_item_class()->get_name() : 'Нет') . '</td>
								<td>' . ($review->get_moderate() ? '<span class = "label label-success">Допущен</span>' : '<span class = "label label-danger">Запрещен</span>') . '</td>
								<td>' . $review->get_format_time_add() . '</td>
								<td>
									<a href="' .ADMINURL . '/review/editform/' . $review->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
								</td>
								<td>
									<a href="' .ADMINURL . '/review/delete/' . $review->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
								</td>
							</tr>
						';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<a class="btn btn-success" href="' .ADMINURL . '/review/addform/"><i class = "fa fa-plus"></i> Добавить отзыв</a>
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('review');
	set_title('Список отзывов');
	set_content($content);
	set_tpl('index.php');
}

function admin_review_addform() {
	$users = '';
	foreach (sel('users') as $user) {
		$users .= '<option value = ' . $user['id'] . '>' . $user['name'] . '</option>';
	}
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/review/add/" enctype="multipart/form-data">
				<div class="col-xs-12">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="user_id">Пользователь:</label>
								<select name = "user_id" id = "user_id" class="form-control">
									' . $users . '
								</select>
							</div>
							<div class="form-group">
								<label for="text">Комментарий:</label>
								<textarea class = "form-control" id = "text" name = "text"></textarea>
							</div>
							<div class="form-group">
								<label for="item_id">Предмет:</label>
								<select name = "item_id" id = "item_id" class="form-control">
									<option value = "0">Не выбран</option>
								</select>
							</div>
							<div class="form-group">
								<label for="moderate">Модерация:</label>
								<select name = "moderate" id = "moderate" class="form-control">
									<option value = "1">Допущен</option>
									<option value = "0">Запрещен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить отзыв</button>
						</div>
					</div>
				</div>
				</form>
			</div>
		';
	add_breadcrumb('Список отзывов', ADMINURL . '/review/', 'fa-pencil-square-o');
	set_active_admin_menu('reviewadd');
	set_title('Добавить отзыв');
	set_content($content);
	set_tpl('index.php');
}

function admin_review_add() {
	$review = new review();
	$review->set_parametrs_from_request();
	$review->add_review();
	alertS('Отзыв успешно добавлен', ADMINURL . '/review/');
}

function admin_review_editform($args) {
	$review = new review((int) $args[0]);
	$users = '';
	foreach (sel('users') as $user) {
		$users .= '<option value = "' . $user['id'] . '"' . ($user['id'] == $review->get_user_id() ? ' selected = "selected"' : '') . '>' . $user['name'] . '</option>';
	}
	$content = '
			<div class="row">
				<form method = "post" action = "' .ADMINURL . '/review/edit/' . $review->get_id() . '/" enctype="multipart/form-data">
				<div class="col-xs-12">
					<div class="box">
						<div class = "box-body">
							<div class="form-group">
								<label for="user_id">Пользователь:</label>
								<select name = "user_id" id = "user_id" class="form-control">
									' . $users . '
								</select>
							</div>
							<div class="form-group">
								<label for="text">Комментарий:</label>
								<textarea class = "form-control" id = "text" name = "text">' . str_replace(['\\\r', '\\\n'], ['', "\n"], $review->get_text()) . '</textarea>
							</div>
							<div class="form-group">
								<label for="item_id">Предмет:</label>
								<select name = "item_id" id = "item_id" class="form-control">
									<option value = "0">Не выбран</option>
								</select>
							</div>
							<div class="form-group">
								<label for="moderate">Модерация:</label>
								<select name = "moderate" id = "moderate" class="form-control">
									<option value = "1"' . ($review->get_moderate() ? ' selected = "selected"' : '') . '>Допущен</option>
									<option value = "0"' . (!$review->get_moderate() ? ' selected = "selected"' : '') . '>Запрещен</option>
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить</button>
						</div>
					</div>
				</div>
				</form>
			</div>
		';
	add_breadcrumb('Список отзывов', ADMINURL . '/review/', 'fa-pencil-square-o');
	set_active_admin_menu('review');
	set_title('Редактирование отзыва');
	set_content($content);
	set_tpl('index.php');
}

function admin_review_edit($args) {
	$review = new review((int) $args[0]);
	$review->set_parametrs_from_request();
	$review->update_review();
	alertS('Изменения сохранены', ADMINURL . '/review/editform/' . $review->get_id() . '/');
}

function admin_review_delete($args) {
	$review = new review((int) $args[0]);
	$review->delete_review();
	alertS('Отзыв успешно удален', ADMINURL . '/review/');
}
