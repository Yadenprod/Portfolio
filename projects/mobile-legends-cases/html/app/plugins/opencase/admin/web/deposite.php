<?php

add_admin_navbar('admin_navbar_opencase_deposite');
add_admin_get('/opencase/deposite/(([0-9]+)/)?', 'admin_opencase_deposite');

function admin_navbar_opencase_deposite() {
	$deposite = new deposite();
	$alldeposites = $deposite->get_deposites('', 'id DESC', 8);
	$content = '';
	foreach ($alldeposites as $value) {
		$content .= '
				<li>
					<a href="' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">
					  <div class="pull-left">
						<img src="' . $value->get_user_class()->get_data('image') . '" class="img-circle" alt="' . $value->get_user_class()->get_name() . '" width = "160px">
					  </div>
					  <h4>
						' . mb_substr($value->get_user_class()->get_name(), 0, 18) . '
						<small><i class="fa fa-clock-o"></i> ' . $value->get_format_time_add('H:i:s') . '</small>
					  </h4>
					  <p>Депозит "' . $value->get_from_text() . '", сумма ' . $value->get_sum() . ' руб</p>
					</a>
				</li>';
	}
	$content .= '<li class = "lastupdate" hidden>' . (isset($alldeposites[0]) ? $alldeposites[0]->get_format_time_add('H:i:s') : '') . '</li>';
	$content = '
              <li class="header">Последние депозиты</li>
              <li>
                <ul class="menu">
				' . $content . '
                </ul>
              </li>
              <li class="footer"><a href="' .ADMINURL . '/opencase/deposite/">Просмотреть все депозиты</a></li>
            ';
	return array(
		'position' => 1,
		'key' => 'nvabar-deposite',
		'icon' => 'fa-money',
		'content' => $content
	);
}

function admin_opencase_deposite($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$depositecount = db()->query_once('select count(id) from opencase_deposite');
	$pages = new Pages();
	$pages->set_num_object($depositecount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/deposite/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/deposite/');
	$pages->set_curent_page($page);
	$deposite = new deposite();
	$alldeposites = $deposite->get_deposites('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Пользователь</th>
									<th>Сумма</th>
									<th>Платежная система</th>
									<th>Статус</th>
									<th>Время</th>
								</tr>
							</thead>
								
							<tbody>
						';
	foreach ($alldeposites as $value) {
		$content .= '
								<tr>
									<td>' . $value->get_id() . '</td>
									<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>
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
					<div class = "box-footer">
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('opencasedepoite');
	set_title('Депозиты');
	set_content($content);
	set_tpl('index.php');
}
