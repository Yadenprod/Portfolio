<?php

add_admin_get('/mode/upgrade/(([0-9]+)/)?', 'admin_opencase_mode_upgrade');

function admin_opencase_mode_upgrade($args) {
	$page = isset($args[1]) ? $args[1] : 1;
	$pages = new Pages();
	$pages->set_num_object(upgrade::getUpgradesCount());
	$pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
	$pages->set_format_url(ADMINURL . '/mode/upgrade/{p}/');
	$pages->set_first_url(ADMINURL . '/mode/upgrade/');
	$pages->set_curent_page($page);
	$content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<div class="box-body">
						<table class = "table table-bordered table-striped" id="FAQElements">
							<thead>
								<tr>
									<th>ID</th>
									<th>Пользователь</th>
									<th>Исходный предмет</th>
									<th>Целевой предмет</th>
									<th>Доп баланс</th>
									<th>Профит</th>
									<th>Время</th>
									<th>Статус</th>
								</tr>
							</thead>								
							<tbody>
					';
	$allUpgrades = upgrade::getUpgrades('', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));
	foreach ($allUpgrades as $value) {
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
											<td><a href = "' .ADMINURL . '/opencase/user/' . $value->getUserId() . '/">' . $value->getUser()->get_name() . '</a></td>
											<td>' . $value->getSource()->get_item_class()->get_name() . '</td>
											<td>' . $value->getTarget()->get_name() . '</td>
											<td>' . $value->getAdditionalBalance() . '</td>
											<td><span class = "label ' . $labelClass . '">' . $value->getProfit() . ' руб</span></td>
											<td>' . $value->getFormatCreatedAt() . '</td>
											<td>' . $value->getLabelStatus() . '</td>
										</tr>
									';
	}
	$content .= '
							</tbody>
						</table>
					</div>
					<div class = "box-footer">
						<ul class="pagination pagination-sm no-margin pull-right">' .  $pages->get_html_pages() . '</ul>
					</div>
				</div>
			</div>
		</div>
		';
	set_active_admin_menu('upgrademode');
	set_title('Режим Апгрейд');
	set_content($content);
	set_tpl('index.php');
}
