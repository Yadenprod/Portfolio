<?php

add_admin_get('/disablepage/', 'admin_disablepage_index');
add_admin_post('/disablepage/update/', 'admin_disablepage_update');

if (get_setval('disabledsite') && !is_admin_uri() && !is_admin()) {
	set_content('');
	set_title(get_setval('disabletext'));
	set_title_page(get_setval('disabletext'));
	set_tpl(get_setval('disablepage'));
	wp()->render();
	wsexit();
}

function admin_disablepage_index() {
	$dir = current_template_folder();
	$skip = array('.', '..');
	$files = scandir($dir);
	$tamplates = '';
	foreach ($files as $key => $file) {
		if (!in_array($file, $skip))
			if (strstr($file, '.php') && !strstr($file, 'footer') && !strstr($file, 'header') && !strstr($file, 'sidebar')) {
				$tamplates .= '<option value = "' . $file . '" ' . (get_setval('disablepage') == $file ? 'selected = "selected"' : '') . '>' . $file . '</option>';
			}
	}
	$content = '
				<div class="row">
					<div class="col-xs-12">
						<div class="box">
							<form method = "post" action = "' .ADMINURL . '/disablepage/update/" enctype="multipart/form-data">
								<div class="box-body">
									<div class="form-group">
										<label for="disabled">Отключить сайт:</label>
										<select name = "disabled" id = "disabled" class = "form-control">
											<option value = "0">Нет</option>
											<option value = "1" ' . (get_setval('disabledsite') ? 'selected = "selected"' : '') . '>Да</option>
										</select>
									</div>
									<div class="form-group">
										<label for="disablepage">Страница при отключение сайта:</label>
										<select name = "disablepage" id = "disablepage" class = "form-control">
											' . $tamplates . '
										</select>
									</div>
									<div class="form-group">
										<label for="disabletext">Текст на странице отключения сайта:</label>
										<input type = "text" class="form-control" name="disabletext" id="disabletext" value = "' . get_setval('disabletext') . '">
									</div>
								</div>
								<div class = "box-footer">
									<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить</button>
								</div>
							</form>
						</div>
					</div>
				</div>
		';
	set_active_admin_menu('disablesite');
	set_title('Настройки отключения сайта');
	set_content($content);
	set_tpl('index.php');
}

function admin_disablepage_update() {
	update_setval('disabledsite', $_POST['disabled']);
	update_setval('disablepage', $_POST['disablepage']);
	update_setval('disabletext', $_POST['disabletext']);
	redirect_srv_msg('<div class="n_ok"><p>Настройки успешно сохранены.</p></div>', ADMINURL . '/disablepage/');
}
