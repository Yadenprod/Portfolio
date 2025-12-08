<?php

add_admin_navbar('admin_navbar_opencase_withdraw');
add_admin_get('/opencase/withdraw/(([0-9]+)/)?', 'admin_opencase_withdraw');

function admin_navbar_opencase_withdraw() {
	$dItems = new droppedItem();
	$dItems = $dItems->get_droppedItems('status = 1 or status = 2 or status = 5', 'id DESC', 8);
	$content = '';
	foreach ($dItems as $value) {
		$content .= '
				<li>
					<a href="' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">
					  <div class="pull-left">
						<img src="' . $value->get_user_class()->get_data('image') . '" class="img-circle" alt="' . $value->get_user_class()->get_name() . '" width = "160px">
					  </div>
					  <h4>
						' . mb_substr($value->get_user_class()->get_name(), 0, 18) . '
						<small><i class="fa fa-clock-o"></i> ' . $value->get_format_time_drop('H:i:s') . '</small>
					  </h4>
					  <p>' . $value->get_item_name_alt() . '</p>
					</a>
				</li>';
	}
	$content .= '<li class = "lastupdate" hidden>' . (isset($dItems[0]) ? $dItems[0]->get_format_time_drop('H:i:s') : '') . '</li>';
	$content = '
              <li class="header">Последние выводы</li>
              <li>               
                <ul class="menu">
				' . $content . '
                </ul>
              </li>
              <li class="footer"><a href="' .ADMINURL . '/opencase/withdraw/">Просмотреть все выводы</a></li>
            ';
	return array(
		'position' => 2,
		'key' => 'nvabar-withdraw',
		'icon' => 'fa-ticket',
		'content' => $content
	);
}

function admin_opencase_withdraw($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$dropcount = db()->query_once('select count(id) from opencase_droppeditems where status = 1 or status = 2 or status = 5');
	$pages = new Pages();
	$pages->set_num_object($dropcount['count(id)']);
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/opencase/withdraw/{p}/');
	$pages->set_first_url(ADMINURL . '/opencase/withdraw/');
	$pages->set_curent_page($page);
	$dItem = new droppedItem();
	$alldItems = $dItem->get_droppedItems('status = 1 or status = 2 or status = 5', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
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
									<th>Предмет</th>
									<th>Цена</th>
									<th>Статус</th>
									<th>Время</th>
								</tr>
							</thead>
								
							<tbody>
					';
	foreach ($alldItems as $value) {
		$content .= '
				<tr>
					<td>' . $value->get_id() . '</td>
					<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>
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
					<div class = "box-footer">
						<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('opencasewithdraw');
	set_title('Выводы предметов');
	set_content($content);
	set_tpl('index.php');
}
