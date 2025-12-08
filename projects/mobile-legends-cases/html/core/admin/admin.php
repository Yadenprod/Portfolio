<?php
$admin_menu = array(
    array(
        'key' => 'constrol',
        'name' => 'Управление',
        'position' => 1,
        'icon' => 'fa-dashboard',
        'menu' => array(
            array(
                'key' => 'dashboard',
                'icon' => 'fa-dashboard',
                'url' => ADMINURL . '/dashboard/',
                'text' => 'Панель управления'
            ),
            array(
                'key' => 'vivod',
                'icon' => 'fa-vivod',
                'url' => ADMINURL . '/vivod/',
                'text' => 'Запросы на вывод'
            ),
            array(
                'key' => 'vivodhistory',
                'icon' => 'fa-historyvivod',
                'url' => ADMINURL . '/vivod/history',
                'text' => 'Выведенные предметы'
            ),
            array(
                'icon' => 'fa-sign-in',
                'url' => '/',
                'text' => 'Перейти на сайт'
            ),
            array(
                'key' => 'page',
                'icon' => 'fa-file-text',
                'url' => ADMINURL . '/page/',
                'text' => 'Страницы'
            ),
            array(
                'key' => 'pageaddform',
                'icon' => 'fa-plus',
                'url' => ADMINURL . '/page/addform/',
                'text' => 'Добавить страницу'
            ),
            array(
                'key' => 'update',
                'icon' => 'fa-refresh',
                'url' => ADMINURL . '/update/',
                'text' => 'Обновление системы'
            ),
            array(
                'key' => 'settings',
                'icon' => 'fa-wrench',
                'url' => ADMINURL . '/settings/',
                'text' => 'Настройки'
            )
        )
    ),
    array(
        'key' => 'adminsmain',
        'name' => 'Администраторы',
        'position' => 15,
        'icon' => 'fa-user-secret',
        'menu' => array(
            array(
                'key' => 'admins',
                'icon' => 'fa-users',
                'url' => ADMINURL . '/admins/',
                'text' => 'Администраторы'
            ),
            array(
                'key' => 'adminsaddform',
                'icon' => 'fa-plus',
                'url' => ADMINURL . '/admins/addform/',
                'text' => 'Добавить администратора'
            )
        )
    ),
    array(
        'key' => 'pluginsmain',
        'name' => 'Плагины',
        'position' => 14,
        'icon' => 'fa-plug',
        'menu' => array(
            array(
                'key' => 'plugins',
                'icon' => 'fa-plug',
                'url' => ADMINURL . '/plugins/',
                'text' => 'Плагины'
            )
        )
    ),
    array(
        'key' => 'mediamanagermain',
        'name' => 'Медиа файлы',
        'position' => 13,
        'icon' => 'fa-image',
        'menu' => array(
            array(
                'key' => 'mediamanager',
                'icon' => 'fa-file-image-o',
                'url' => ADMINURL . '/mediamanager/',
                'text' => 'Менеджер медиа файлов'
            ),
            array(
                'key' => 'addmediafile',
                'icon' => 'fa-upload',
                'url' => ADMINURL . '/mediamanager/addform/',
                'text' => 'Загрузить файл'
            )
        )
    )
);

set_menu('admin', $admin_menu);

global $admin_dashboard;
$admin_dashboard = array();

global $admin_navbar;
$admin_navbar = array();

add_app(ADMINURL . '/', 'index');
add_app(ADMINURL . '/login/', 'login');
add_admin_app('/dashboard/', 'dashboard');
add_admin_app('/vivod/', 'vivod');
add_admin_app('/vivod/history', 'vivod_history');
add_admin_app('/page/', 'page_list');
add_admin_app('/page/addform/', 'page_addform');
add_admin_app('/page/editform/([a-z0-9]+)/', 'page_editform');
add_admin_app('/page/add/', 'page_add');
add_admin_app('/page/edit/([a-z0-9]+)/', 'page_edit');
add_admin_app('/page/delete/([a-z0-9]+)/', 'page_delete');
add_admin_app('/update/', 'update_system');
add_admin_app('/update/start/', 'update_start');
add_admin_app('/settings/', 'settings_page');
add_admin_app('/settings/edit/', 'settings_edit');
add_admin_app('/admins/', 'admin_list');
add_admin_app('/admins/addform/', 'admin_addform');
add_admin_app('/admins/editform/([0-9]+)/', 'admin_editform');
add_admin_app('/admins/add/', 'admin_add');
add_admin_app('/admins/edit/([0-9]+)/', 'admin_edit');
add_admin_app('/admins/delete/([0-9]+)/', 'admin_delete');
add_admin_app('/admins/editmenu/([0-9]+)/', 'admin_editmenu');
add_admin_app('/plugins/', 'plugins_list');
add_admin_app('/plugins/switch/([0-9]+)/', 'plugin_switch');
add_admin_app('/plugins/delete/([0-9]+)/', 'plugin_delete');
add_admin_app('/mediamanager/(([0-9]+)/)?', 'media_list');
add_admin_app('/mediamanager/editform/([a-z0-9]+)/', 'media_editform');
add_admin_app('/mediamanager/addform/', 'media_addform');
add_admin_app('/mediamanager/edit/([a-z0-9]+)/', 'media_edit');
add_admin_app('/mediamanager/add/', 'media_add');
add_admin_app('/mediamanager/delete/([a-z0-9]+)/', 'media_delete');
add_admin_app('/logout/', 'logout');


function index()
{
    if (!is_admin()) {
        clear_cookie('admin_token');
        $content = '<form method = "post" action = "' . ADMINURL . '/login/">Имя пользователя:<br> <input type = "text" name = "name" value = ""><br> Пароль: <br><input type = "password" name = "password" value = ""><br><input type = "submit" value = "Вход"></form>';
        set_title('Панель администрирования');
        set_content($content);
        set_tpl('login.php');
    } else {
        redirect(ADMINURL . '/dashboard/');
    }
}

function login()
{
    if (!empty($_POST['name']) && !empty($_POST['password'])) {
        $admin = new admin();
        if ($admin->login($_POST['name'], $_POST['password'])) {
            set_cookie('admin_token', md5('ADMIN' . $admin->get_id() . ':' . $admin->get_name() . ':' . $admin->get_password() . ':' . iptoken('ADMIN')));
            redirect(ADMINURL . '/dashboard/');
        } else {
            alertE('Неверное имя или пароль', ADMINURL . '/');
        }
    } else {
        alertE('Не все поля заполнены', ADMINURL . '/');
    }
}

function dashboard()
{
    $content = get_admin_dashboard();
    add_content($content);
    set_active_admin_menu('dashboard');
    set_title('Панель управления');
    set_tpl('index.php');
}

function vivod($args) {
    $page = isset($args[1]) ? $args[1] : 1;
    $dropcount = db()->query_once('SELECT count(id) FROM opencase_droppeditems where status = 1 or status = 5');
    $pages = new Pages();
    $pages->set_num_object($dropcount['count(id)']);
    $pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
    $pages->set_format_url(ADMINURL . '/opencase/withdraw/{p}/');
    $pages->set_first_url(ADMINURL . '/opencase/withdraw/');
    $pages->set_curent_page($page);
    $dItem = new droppedItem();
    $alldItems = $dItem->get_droppedItems('status = 1 or status = 5', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));

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
										<th>UserID|ZoneID</th>
										<th>Предмет</th>
										<th>Цена</th>
										<th>Статус</th>
										<th>Время</th>
										<th>Подтверждение</th>
									</tr>
								</thead>
									
								<tbody>
						';
    foreach ($alldItems as $value) {
        $content .= '
					<tr>
						<td>' . $value->get_id() . '</td>
						<td><a href = "' .ADMINURL . '/opencase/user/' . $value->get_user_id() . '/">' . $value->get_user_class()->get_name() . '</a></td>
						<td><a href = "https://www.kachishop.com/ru/mobile-legends?type=contact_us&from=account' . '/" target="_blank">' .$value->get_user_class()->get_data('trade_link') . '</a></td>
						<td>' . $value->get_item_name_alt() . '</td>
						<td>' . $value->get_price() . ' руб</td>
						<td>' . $value->get_label_status() . '</td>
						<td>' . $value->get_format_time_drop() . '</td>
						<td class="btn btn-success btn-sm" onclick="chi('.$value->get_id().')">Отправить</td>
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
    set_active_admin_menu('vivod');
    set_title('Запросы на вывод');
    // вызов php-скрипта и перезагрузка страницы, чтобы табличка обновилась
    add_jscript("
    function chi(n) {
    $.ajax({
        type: 'POST',
        url: 'https://m-legends-drop.ru/api/opencase/withdraw/admin/'+n+'/',
        data: {},
        async: true,
        dataType: 'json',
        success: function (response) {
            //console.log('Страницу перезагружаем через 1 секунду');
            setTimeout(function(){location.reload(true);},500);
        }
    });
    }
    ");
    set_content($content);
    set_tpl('index.php');
}

function vivod_history()
{
    $page = isset($args[1]) ? $args[1] : 1;
    $dropcount = db()->query_once('SELECT count(id) FROM opencase_droppeditems where status = 2');
    $pages = new Pages();
    $pages->set_num_object($dropcount['count(id)']);
    $pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
    $pages->set_format_url(ADMINURL . '/opencase/withdraw/{p}/');
    $pages->set_first_url(ADMINURL . '/opencase/withdraw/');
    $pages->set_curent_page($page);
    $dItem = new droppedItem();
    $alldItems = $dItem->get_droppedItems('status = 2', 'id DESC', (($page - 1) * get_setval('admin_in_page')) . ',' . get_setval('admin_in_page'));

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
									<th>UserID|ZoneID</th>
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
					<td>' .$value->get_user_class()->get_data('trade_link') . '</td>
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
    set_active_admin_menu('vivodhistory');
    set_title('Выведенные предметы');
    set_content($content);
    set_tpl('index.php');
}

function page_list()
{
    $webpages = webpage::get_webpages();
    $tbody = '';
    foreach ($webpages as $webpage) {
        $tbody .= '
				<tr>
					<td>' . $webpage->get_namepage() . '</td>
					<td><a href = "' . $webpage->get_url() . '" target = "_blank">' . $webpage->get_url() . '</td>
					<td>
						<a href="' . ADMINURL . '/page/editform/' . $webpage->get_namepage() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>
						<a href="' . ADMINURL . '/page/delete/' . $webpage->get_namepage() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
    }
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="box">
						<div class="box-body">
					 
							<table id = "pageList" class = "table table-bordered table-striped">
								<thead>
									<tr>
										<th>Имя страницы</th>
										<th>Адрес страницы</th>
										<th width = "20px"></th>
										<th width = "20px"></th>
									</tr>
								</thead>
								<tbody>
									' . $tbody . '
								</tbody>
							</table>
						</div>
					<div class="box-footer">
						<a href="' . ADMINURL . '/page/addform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить страницу</a>
					</div>
				</div>
			</div>
		';
    set_active_admin_menu('page');
    set_title('Страницы');
    set_content($content);
    set_tpl('index.php');
}

function page_addform()
{
    $webpage = new webpage();
    $tamplates_select = '';
    foreach (get_files($webpage->get_folder(), '\.php') as $key => $file) {
        if (!strstr($file, 'footer') && !strstr($file, 'header') && !strstr($file, 'sidebar')) {
            $tamplates_select .= '<option value = "' . $file . '">' . $file . '</option>';
        }
    }
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<form method = "post" action = "' . ADMINURL . '/page/add/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя страницы: <span class="red">*</span></label>
								<input type = "text" class="form-control" name="namepage" id="name">
							</div>
							<div class="form-group">
								<label for="url">URL страницы: <span class="red">*</span></label>
								<input type = "text" class="form-control" name="url" id="url">
							</div>
							<div class="form-group">
								<label for="title">Заголовок:</label>
								<input type = "text" class="form-control" name="title" id="title">
							</div>
							<div class="form-group">
								<label for="title_page">Заголовок страницы:</label>
								<input type = "text" class="form-control" name="title_page" id="title_page">
							</div>
							<div class="form-group">
								<label for="content">Содержимое страницы:</label>
								<textarea class = "form-control" name = "content" id = "content"></textarea>
							</div>
							<div class="form-group">
								<label for="meta_des">Мета описание:</label>
								<textarea class="form-control" name="meta_des" id="meta_des"></textarea>
								<b>Количество символов: <span id = "meta_des_count_char">0</span></b>
							</div>
							<div class="form-group">
								<label for="meta_key">Мета ключевые слова:</label>
								<input type = "text" class="form-control" name="meta_key" id="meta_key">
							</div>
							<div class="form-group">
								<label for="tpl">Шаблон:</label>
								<select class="form-control" name="tpl" id="tpl">
									' . $tamplates_select . '
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить страницу</button>
						</div>
					</form>
				</div>
			</div>
		</div>';
    add_jscript('$(function () {
			$("#content").wysihtml5();
		  });');
    add_jscript('$(\'#meta_des\').keyup(function() {
			$(\'#meta_des_count_char\').html($(this).val().length);
		});');
    add_breadcrumb('Страницы', ADMINURL . '/page/', 'fa-file-text');
    set_active_admin_menu('pageaddform');
    set_title('Добавление страницы');
    set_content($content);
    set_tpl('index.php');
}

function page_editform($args)
{
    $webpage = new webpage($args[0]);
    if ($webpage->get_namepage() == '')
        wserror();
    $tamplates_select = '';
    foreach (get_files($webpage->get_folder(), '\.php') as $key => $file) {
        if (!strstr($file, 'footer') && !strstr($file, 'header') && !strstr($file, 'sidebar')) {
            $tamplates_select .= '<option value = "' . $file . '"' . ($webpage->get_tpl() == $file ? ' selected = "selected"' : '') . '>' . $file . '</option>';
        }
    }
    $content = '
		<div class="row">
			<div class="col-xs-12">
				<div class="box">
					<form method = "post" action = "' . ADMINURL . '/page/edit/' . $webpage->get_namepage() . '/">
						<div class="box-body">
							<div class="form-group">
								<label for="name">Имя страницы: <span class="red">*</span></label>
								<input type = "text" class="form-control" name="namepage" id="name" value = "' . $webpage->get_namepage() . '">
							</div>
							<div class="form-group">
								<label for="url">URL страницы: <span class="red">*</span></label>
								<input type = "text" class="form-control" name="url" id="url" value = "' . $webpage->get_url() . '">
							</div>
							<div class="form-group">
								<label for="title">Заголовок:</label>
								<input type = "text" class="form-control" name="title" id="title" value = "' . $webpage->get_title() . '">
							</div>
							<div class="form-group">
								<label for="title_page">Заголовок страницы:</label>
								<input type = "text" class="form-control" name="title_page" id="title_page" value = "' . $webpage->get_title_page() . '">
							</div>
							<div class="form-group">
								<label for="content">Содержимое страницы:</label>
								<textarea class = "form-control" name = "content" id = "content">' . $webpage->get_content() . '</textarea>
							</div>
							<div class="form-group">
								<label for="meta_des">Мета описание:</label>
								<textarea class="form-control" name="meta_des" id="meta_des">' . $webpage->get_meta_des() . '</textarea>
								<b>Количество символов: <span id = "meta_des_count_char">' . mb_strlen(htmlspecialchars($webpage->get_meta_des()), "UTF-8") . '</span></b>
							</div>
							<div class="form-group">
								<label for="meta_key">Мета ключевые слова:</label>
								<input type = "text" class="form-control" name="meta_key" id="meta_key" value = "' . $webpage->get_meta_key() . '">
							</div>
							<div class="form-group">
								<label for="tpl">Шаблон: *</label>
								<select class="form-control" name="tpl" id="tpl">
									' . $tamplates_select . '
								</select>
							</div>
						</div>
						<div class = "box-footer">
							<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
							<a href = "' . $webpage->get_url() . '" class="btn btn-info" target = "_blank"><i class = "fa fa-eye"></i> Просмотреть</a>
						</div>
					</form>
				</div>
			</div>
		</div>';
    add_jscript('$(function () {
			$("#content").wysihtml5();
		  });');
    add_jscript('$(\'#meta_des\').keyup(function() {
			$(\'#meta_des_count_char\').html($(this).val().length);
		});');
    add_breadcrumb('Страницы', ADMINURL . '/page/', 'fa-file-text');
    set_active_admin_menu('page');
    set_title('Редактирование страницы');
    set_content($content);
    set_tpl('index.php');
}

function page_add()
{
    if ($_POST['namepage'] != '' && $_POST['tpl'] != '') {
        $webpage = new webpage();
        $webpage->set_from_array($_POST);
        $webpage->add();
        alertS('Страница успешно добавленна', ADMINURL . '/page/');
    } else {
        alertE('Не все обязательные поля заполнены', ADMINURL . '/page/addform/');
    }
}

function page_edit($args)
{
    if ($_POST['namepage'] != '' && $_POST['tpl'] != '') {
        $webpage = new webpage($args[0]);
        if ($webpage->get_namepage() == '')
            wserror();
        $webpage->set_from_array($_POST);
        $webpage->update($args[0]);
        alertS('Изменения успешно сохранены', ADMINURL . '/page/editform/' . $webpage->get_namepage() . '/');
    } else {
        alertE('Не все обязательные поля заполнены', ADMINURL . '/page/editform/' . $args[0] . '/');
    }
}

function page_delete($args)
{
    $webpage = new webpage($args[0]);
    if ($webpage->get_namepage() == '')
        wserror();
    $webpage->delete();
    alertS('Страница успешно удаленна', ADMINURL . '/page/');
}

function update_system()
{
    $lastVer = checklastv();
    $changeLog = checkchanglog();
    $content = '
		<div class="row">
			<div class="col-md-7">
			  <div class="box">
					<div class = "box-header with-border">
						<h3 class="box-title">Что нового:</h3>
					</div>
					<div class="box-body">
							' . ($changeLog ? $changeLog : 'Не удалось соедениться с сервером обновлений') . '
					</div>
				</div>
			</div>
			<div class="col-md-5">
			  <div class="box">
					<div class = "box-header with-border">
						<h3 class="box-title">Обновление системы:</h3>
					</div>
					<div class="box-body">
						<table class="table">
							<tr>
								<th width = "50%">Ваша версия системы:</th>
								<td>' . get_setval('cms_version') . '</td>
							</tr>
							<tr>
								<th width = "50%">Доступная верисия системы:</th>
								<td>' . ($lastVer ? $lastVer : 'Не удалось соедениться с сервером обновлений') . '</td>
							</tr>
						</table>
					</div>
					<div class = "box-footer">'
        . ($lastVer != get_setval('cms_version') ? '<a href = "' . ADMINURL . '/update/start/" class = "btn btn-primary' . (!$lastVer ? ' disabled' : '') . '"><i class = "fa fa-refresh"></i> Обновить</a>' : 'Обновлений не требуется') .
        '</div>
				</div>
			</div>
		</div>
		';
    set_title('Обновление системы');
    set_active_admin_menu('update');
    set_content($content);
    set_tpl('index.php');
}

function update_start()
{
    if (get_setval('cms_version') == checklastv())
        alertS('Обновление не требуется. У Вас последняя версия.', ADMINURL . '/sysupdate/');
}

function settings_page()
{
    $template_select = '';
    foreach (get_files(TPLFOLDER . '/') as $file) {
        if (is_dir(TPLFOLDER . '/' . $file))
            $template_select .= '<option value="' . $file . '"' . ($file == get_setval('current_template_folder') ? 'selected = "selected"' : '') . '>' . $file . '</option>';
    }
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="box">
						<form method = "post" action = "' . ADMINURL . '/settings/edit/">
							<div class="box-body">
								<div class="form-group">
									<label for="siteurl">Адрес сайта: </label>
									<input type = "text" class="form-control" name="site_url" id="siteurl" value = "' . get_setval('site_url') . '">
								</div>
								<div class="form-group">
									<label for="siteurl">Имя сайта: </label>
									<input type = "text" class="form-control" name="site_name" id="site_name" value = "' . get_setval('site_name') . '">
								</div>
								<div class="form-group">
									<label for="siteurl">Почта администратора сайта: </label>
									<input type = "text" class="form-control" name="admin_email" id="admin_email" value = "' . get_setval('admin_email') . '">
								</div>
								<div class="form-group">
									<label for="template">Шаблон сайта:</label>
									<select name="current_template_folder" id = "template" class = "form-control">
										' . $template_select . '
									</select>
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
    set_title('Настройки');
    set_content($content);
    set_tpl('index.php');
    set_active_admin_menu('settings');
}

function settings_edit()
{
    foreach ($_POST as $key => $value) {
        get_settings()->update_value($key, $value);
    }
    alertS('Настройки успешно сохранены', ADMINURL . '/settings/');
}

function admin_list()
{
    $admin = new admin();
    $admins = admin::get_admins();
    $tbody = '';
    foreach ($admins as $admin) {
        $tbody .= '
				<tr>
					<td>' . $admin->get_id() . '</td>
					<td>' . $admin->get_name() . '</td>
					<td>' . $admin->get_email() . '</td>
					<td>	
						<a href="' . ADMINURL . '/admins/editform/' . $admin->get_id() . '/" title="Редактировать"><i class = "fa fa-pencil"></i></a>
					</td>
					<td>
						<a href="' . ADMINURL . '/admins/delete/' . $admin->get_id() . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
					</td>
				</tr>
			';
    }
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="box">
						<div class="box-body">
						<table class = "table table-bordered table-striped">
							<thead>
								<tr>
									<th>ID</th>
									<th>Имя администратора</th>
									<th>Email администратора</th>
									<th width = "30px"></th>
									<th width = "30px"></th>
								</tr>
							</thead>	
							<tbody>
								' . $tbody . '
							</tbody>
							</table>
						</div>
						<div class = "box-footer">
							<a href="' . ADMINURL . '/admins/addform/" class="btn btn-success"><i class="fa fa-plus"></i> Добавить администратора</a>
						</div>
					</div>
				</div>
			</div>
		';
    set_active_admin_menu('admins');
    set_title('Администраторы');
    set_content($content);
    set_tpl('index.php');
}

function admin_addform()
{
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="nav-tabs-custom">
						<ul class="nav nav-tabs">
							<li class="active"><a href="#settings" data-toggle="tab">Настройки</a></li>
						</ul>
						<div class="tab-content">
							<div class="active tab-pane" id="settings">
								<form method = "post" action = "' . ADMINURL . '/admins/add/">
									<div class="form-group">
										<label for="name">Имя администратора: <span class="red">*</span></label>
										<input type = "text" class="form-control" name="name" id="name">
									</div>
									<div class="form-group">
										<label for="password">Пароль: <span class="red">*</span></label>
										<input type = "password" class="form-control" name="password" id="password">
									</div>
									<div class="form-group">
										<label for="email">Email:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="email" id="email">
											<div class="input-group-addon">
												<i class="fa fa-send"></i>
											</div>
										</div>
									</div>
									<div class="form-group">
										<label for="phone">Телефон:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="phone" id="phone">
											<div class="input-group-addon">
												<i class="fa fa-phone"></i>
											</div>
										</div>
									</div>
									<div class="form-group">
										<label for="ips">IP с которых разрешен вход:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="ips" id="ips">
											<div class="input-group-addon">
												<i class="fa fa-laptop"></i>
											</div>
										</div>
									</div>
									<button class="btn btn-success" type="submit"><i class = "fa fa-plus"></i> Добавить администратора</button>
								</form>	
							</div>
						</div>
					</div>
				</div>
			</div>
		';
    add_script(get_admin_template_folder() . '/plugins/input-mask/jquery.inputmask.js', 10, 'footer');
    add_jscript('$(function () {
			$("#phone").inputmask("(999) 999-9999");
		});');
    add_breadcrumb('Администраторы', ADMINURL . '/admins/', 'fa-users');
    set_active_admin_menu('adminsaddform');
    set_title('Добавление администратора');
    set_content($content);
    set_tpl('index.php');
}

function admin_editform($args)
{
    $admin = new admin($args[0]);
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="nav-tabs-custom">
						<ul class="nav nav-tabs">
							<li class="active"><a href="#settings" data-toggle="tab">Настройки</a></li>
						</ul>
						<div class="tab-content">
							<div class="active tab-pane" id="settings">
								<form method = "post" action = "' . ADMINURL . '/admins/edit/' . $admin->get_id() . '/">
									<div class="form-group">
										<label for="name">Имя администратора: <span class="red">*</span></label>
										<input type = "text" class="form-control" name="name" id="name" value = "' . $admin->get_name() . '">
									</div>
									<div class="form-group">
										<label for="password">Пароль: <span class="red">*</span></label>
										<input type = "password" class="form-control" name="password" id="password">
									</div>
									<div class="form-group">
										<label for="email">Email:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="email" id="email" value = "' . $admin->get_email() . '">
											<div class="input-group-addon">
												<i class="fa fa-send"></i>
											</div>
										</div>
									</div>
									<div class="form-group">
										<label for="phone">Телефон:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="phone" id="phone" value = "' . $admin->get_phone() . '">
											<div class="input-group-addon">
												<i class="fa fa-phone"></i>
											</div>
										</div>
									</div>
									<div class="form-group">
										<label for="ips">IP с которых разрешен вход:</label>
										<div class="input-group">
											<input type = "text" class="form-control" name="ips" id="ips" value = "' . $admin->get_ips() . '">
											<div class="input-group-addon">
												<i class="fa fa-laptop"></i>
											</div>
										</div>
									</div>
									<button class="btn btn-success" type="submit"><i class = "fa fa-save"></i> Сохранить изменения</button>
								</form>	
							</div>	
						</div>
					</div>
				</div>
			</div>
		';
    add_script(get_admin_template_folder() . '/plugins/input-mask/jquery.inputmask.js', 10, 'footer');
    add_jscript('$(function () {
			$("#phone").inputmask("(999) 999-9999");
		});');
    add_breadcrumb('Администраторы', ADMINURL . '/admins/', 'fa-users');
    set_active_admin_menu('admins');
    set_title('Редактирование администратора');
    set_content($content);
    set_tpl('index.php');
}

function admin_add()
{
    if (!empty($_REQUEST['name']) && !empty($_REQUEST['password'])) {
        $admin = new admin();
        $admin->set_name($_POST['name']);
        $admin->set_password(admin::hash_password($_POST['password']));
        $admin->set_email($_POST['email']);
        $admin->set_phone($_POST['phone']);
        $admin->set_ips($_POST['ips']);
        $admin->add();
        alertS('Администратор успешно добавлен', ADMINURL . '/admins/');
    } else {
        alertE('Не все поля заполнены', ADMINURL . '/admins/addform/');
    }
}

function admin_edit($args)
{
    $admin = new admin($args[0]);
    if (!$admin->get_id())
        wserror();
    if (!empty($_REQUEST['name'])) {
        $admin->set_name($_POST['name']);
        if (!empty($_POST['password']))
            $admin->set_password(admin::hash_password($_POST['password']));
        $admin->set_email($_POST['email']);
        $admin->set_phone($_POST['phone']);
        $admin->set_ips($_POST['ips']);
        $admin->update();
        if (admin()->get_id() != $admin->get_id() && empty($_POST['password']))
            alertS('Изменения успешно сохранены', ADMINURL . '/admins/editform/' . $admin->get_id() . '/');
        else
            redirect_srv_msg('', ADMINURL . '/logout/');
    } else {
        alertE('Не все поля заполнены', ADMINURL . '/admins/editform/' . $admin->get_id() . '/');
    }
}

function admin_delete($args)
{
    $admin = new admin($args[0]);
    if (!$admin->get_id())
        wserror();
    $admin->delete();
    if (admin()->get_id() != $admin->get_id())
        alertS('Администратор успешно удален', ADMINURL . '/admins/');
    else
        redirect_srv_msg('', ADMINURL . '/logout/');
}

function plugins_list()
{
    $allplugins = get_plugins_list();
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="box">
						<div class="box-body">
							<table class = "table table-bordered table-striped">
								<thead>
									<tr>
										<th>Название</th>
										<th>Описание</th>
										<th >Автор</th>
										<th>Версия</th>
										<th width = "20px"></th>
										<th width = "20px"></th>
										<th width = "20px"></th>
									</tr>
								</thead>
									
								<tbody>
			';
    foreach ($allplugins as $value) {
        if (!empty($value['error'])) {
            $iconswitch = 'fa-exclamation-circle';
            $textswitch = $value['error'];
        } elseif ($value['enable']) {
            $iconswitch = 'fa-toggle-on';
            $textswitch = 'Деактивировать';
        } else {
            $iconswitch = 'fa-toggle-off';
            $textswitch = 'Активировать';
        }
        $name = false;
        $description = false;
        $author = false;
        $version = false;
        $settings = false;
        $file = file_get_contents(PLUGINFOLDER . '/' . $value['name']);
        $pluginsettings = explode('*/', $file);
        $pluginsettings = explode('/*', $pluginsettings[0]);
        if (count($pluginsettings) > 1) {
            $pluginsettings = $pluginsettings[1];
            if ($pluginsettings) {
                $pluginsettings = explode(chr(10), $pluginsettings);
                foreach ($pluginsettings as $key => $pvalue) {
                    $sets = explode(':', $pvalue);
                    if (count($sets) > 1) {
                        $sets[0] = trim($sets[0]);
                        $sets[1] = trim($sets[1]);
                        if ($sets[0] == 'Name')
                            $name = $sets[1];
                        if ($sets[0] == 'Description')
                            $description = $sets[1];
                        if ($sets[0] == 'Author')
                            $author = $sets[1];
                        if ($sets[0] == 'Version')
                            $version = $sets[1];
                        if ($sets[0] == 'Settings')
                            $settings = $sets[1];
                    }
                }
            }
        }
        if (!$name) $name = $value['name'];
        if (!$description) $description = 'Неизвестно';
        if (!$author) $author = 'Неизвестно';
        if (!$version) $version = 'Неизвестно';
        $content .= '
					<tr>
						<td>' . $name . '</td>
						<td>' . $description . '</td>
						<td>' . $author . '</td>
						<td>' . $version . '</td>
						<td>	
							' . ($settings && $value['enable'] ? '<a href="' . ADMINURL . $settings . '" title="Настройки"><i class = "fa fa-wrench"></i></a>' : '') . '
						</td>
						<td>';
        if (!empty($value['error'])) {
            $content .= '<div title="' . $textswitch . '"><i class = "fa ' . $iconswitch . '"></i></div>';
        } else {
            $content .= '<a href="' . ADMINURL . '/plugins/switch/' . $value['id'] . '/" title="' . $textswitch . '"><i class = "fa ' . $iconswitch . '"></i></a>';
        }
        $content .= '
						</td>
						<td>	
							<a href="' . ADMINURL . '/plugins/delete/' . $value['id'] . '/" title="Удалить"><i class = "fa fa-trash"></i></a>
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
    set_active_admin_menu('plugins');
    set_title('Плагины');
    set_content($content);
    set_tpl('index.php');
}

function plugin_switch($args)
{
    $plugin = selo('plugins', array('id' => $args[0]));
    $name = $plugin['name'];
    $plugin_data = get_plugin_data($name);
    if (!empty($plugin_data['error'])) {
        alertE('Ошибка в плагине ' . str_replace('.php', '', $name) . '. ' . $plugin_data['error'], ADMINURL . '/plugins/');
    }
    try {
        require_once PLUGINFOLDER . '/' . $name;
    } catch (\Exception $ex) {
        alertE('Ошибка в плагине ' . str_replace('.php', '', $name) . '. ' . $ex->getMessage(), ADMINURL . '/plugins/');
    }
    $name = str_replace('.php', '', $name);
    if ($plugin['enable'] == 0) {
        foreach (pm()->installers as $installer) {
            if ($installer['plugin'] == $name) {
                $func = $installer['func'];
                if (function_exists($func)) $func();
            }
        }
    } else {
        foreach (pm()->uninstallers as $uninstaller) {
            if ($uninstaller['plugin'] == $name) {
                $func = $uninstaller['func'];
                if (function_exists($func)) $func();
            }
        }
    }
    $name = '';
    $file = file_get_contents(PLUGINFOLDER . '/' . $plugin['name']);
    $pluginsettings = explode('*/', $file);
    $pluginsettings = explode('/*', $pluginsettings[0]);
    if (count($pluginsettings) > 1) {
        $pluginsettings = $pluginsettings[1];
        if ($pluginsettings) {
            $pluginsettings = explode(chr(10), $pluginsettings);
            foreach ($pluginsettings as $key => $pvalue) {
                $sets = explode(':', $pvalue);
                if (count($sets) > 1) {
                    $sets[0] = trim($sets[0]);
                    $sets[1] = trim($sets[1]);
                    if ($sets[0] == 'Name')
                        $name = $sets[1];
                }
            }
        }
    }
    if (!$name) $name = $plugin['name'];
    qryo('update plugins set enable = not(enable) where id = "' . nosqlinj($args[0]) . '"');
    if ($plugin['enable']) $textenable = 'деактивирован'; else $textenable = 'активирован';
    alertS('Плагин ' . $name . ' ' . $textenable . '', ADMINURL . '/plugins/');
}

function plugin_delete($args)
{
    $plugin = selo('plugins', array('id' => $args[0]));
    del('plugins', array('id' => $args[0]));
    $name = '';
    $file = file_get_contents(PLUGINFOLDER . '/' . $plugin['name']);
    $pluginsettings = explode('*/', $file);
    $pluginsettings = explode('/*', $pluginsettings[0]);
    if (count($pluginsettings) > 1) {
        $pluginsettings = $pluginsettings[1];
        if ($pluginsettings) {
            $pluginsettings = explode(chr(10), $pluginsettings);
            foreach ($pluginsettings as $key => $pvalue) {
                $sets = explode(':', $pvalue);
                if (count($sets) > 1) {
                    $sets[0] = trim($sets[0]);
                    $sets[1] = trim($sets[1]);
                    if ($sets[0] == 'Name')
                        $name = $sets[1];
                }
            }
        }
    }
    if (!$name) $name = $plugin['name'];
    eval('if (function_exists("' . str_replace('.php', '', $plugin['name']) . '_uninstall")) ' . str_replace('.php', '', $plugin['name']) . '_uninstall();');
    unlink(PLUGINFOLDER . '/' . $plugin['name']);
    alertS('Плагин ' . $name . ' успешно удален', ADMINURL . '/plugins/');
}

function media_list($args)
{
    $page = isset($args[1]) ? $args[1] : 1;
    $mediacount = qryo('select count(id) from `media`');
    $pages = new Pages();
    $pages->set_num_object($mediacount['count(id)']);
    $pages->set_object_in_page(get_settings()->get_setting_value('admin_in_page'));
    $pages->set_format_url(ADMINURL . '/mediamanager/{p}/');
    $pages->set_first_url(ADMINURL . '/mediamanager/');
    $pages->set_curent_page($page);
    $medias = Media::get_medias(false, array('id' => 'DESC'), array((($page - 1) * get_setval('admin_in_page')), get_setval('admin_in_page')));
    $content = '
			<div class="row">
				<div class="col-xs-12">
					<div class="box">
						<div class="box-body">
							<table class = "table table-bordered table-striped">
								<thead>
									<tr>
										<th width = "5%">ID</th>
										<th>Preview</th>
										<th>Имя</th>
										<th>Описание</th>
										<th>Дата добавления</th>
										<th width = "20px"></th>
										<th width = "20px"></th>
									</tr>
								</thead>
								<tbody>
					';
    foreach ($medias as $media) {
        $content .= '
				<tr>
					<td>' . $media->get_id() . '</td>
					<td>' . $media->get_image(30) . '</td>
					<td>' . $media->get_name() . '</td>
					<td>' . $media->get_description() . '</td>
					<td>' . $media->get_format_time() . '</td>
					<td><a href="' . ADMINURL . '/mediamanager/editform/' . $media->get_id() . '/" title="Изменить настройки"><i class = "fa fa-pencil"></i></a></td>
					<td><a href="' . ADMINURL . '/mediamanager/delete/' . $media->get_id() . '/" title="Удалить медиа файл"><i class = "fa fa-trash"></i></a></td>
				</tr>
			';
    }
    $content .= '
								</tbody>
							</table>
						</div>
						<div class = "box-footer">
							<a href="' . ADMINURL . '/mediamanager/addform/" class="btn btn-success"><i class="fa fa-upload"></i> Загрузить файл</a>
							<ul class="pagination pagination-sm no-margin pull-right">' . $pages->get_html_pages() . '</ul>
						</div>
					</div>
				</div>
			</div>
		';
    set_content($content);
    set_active_admin_menu('mediamanager');
    set_title('Менеджер медиа файлов');
    set_tpl('index.php');
}

function media_addform()
{
    $content = '
			<div class="row">
				<form method = "post" action = "' . ADMINURL . '/mediamanager/add/" enctype="multipart/form-data">
					<div class="col-lg-12">
						<div class="box">
							<div class = "box-body">
								<div class="form-group">
									<label for="file">Загружаймый файл</label>
									<input type="file" name = "file" id="file">
								</div>
								<div class="form-group">
									<label for="file">Описание файла</label>
									<input type = "text" class="form-control" name="description" id="description">
								</div>
								<div class="form-group">
									<label for="description">Размеры изображения:</label>
									<div class = "row">
										<div class = "col-xs-3">
											<div class="checkbox">
												<label><input type="checkbox" name = "size[]" value = "735x300" checked> 735x300</label>
											</div>
										</div>
										<div class = "col-xs-3">
											<div class="checkbox">
												<label><input type="checkbox" name = "size[]" value = "545x200" checked> 545x200</label>
											</div>
										</div>
										<div class = "col-xs-3">
											<div class="checkbox">
												<label><input type="checkbox" name = "size[]" value = "400x400" checked> 400x400</label>
											</div>
										</div>
										<div class = "col-xs-3">
											<div class="checkbox">
												<label><input type="checkbox" name = "size[]" value = "150x100" checked> 150x100</label>
											</div>
										</div>
										<div class = "col-xs-3">
											<div class="checkbox">
												<label><input type="checkbox" name = "size[]" value = "30x30" checked> 30x30</label>
											</div>
										</div>
									</div>
								</div>
								<div class="form-group">
									<label for="size">Свой размер</label>
									<input type="text" class = "form-control" name = "size[]" value = "" id = "size">
								</div>
							</div>
							<div class = "box-footer">
								<button class="btn btn-success" type="submit"><i class = "fa fa-upload"></i> Загрузить</button>
							</div>
						</div>
					</div>
				</form>
			</div>
		';
    set_content($content);
    add_breadcrumb('Менеджер медиа файлов', ADMINURL . '/mediamanager/', 'fa-file-image-o');
    set_active_admin_menu('addmediafile');
    set_title('Загрузить файл');
    set_tpl('index.php');
}

function media_add()
{
    $media = new Media();
    $filename = upload($_FILES['file']);
    if (!$filename) {
        alertE('Ошибка при загрузке файла', ADMINURL . '/mediamanager/addform/');
        return false;
    }
    $media->set_name($filename);
    $media->set_description($_POST['description']);
    $data = array();
    if ($_POST['size'] && is_array($_POST['size'])) {
        foreach ($_POST['size'] as $sizes) {
            foreach (explode(';', $sizes) as $size) {
                if (!in_array($size, $data)) {
                    $size = explode('x', $size);
                    if (is_array($size) && count($size) == 2) {
                        $result = image_resize('uploads/' . $filename, $size[0], $size[1], true);
                        if ($result) {
                            array_push($data, $size[0] . 'x' . $size[1]);
                        }
                    }
                }
            }
        }
    }
    if ($data) {
        usort($data, 'media_sort');
        $media->set_data(implode(';', $data));
    }
    $media->add();
    alertS('Файл успешно загружен', ADMINURL . '/mediamanager/');
}

function media_editform($args)
{
    $media = new Media($args[0]);
    $sizes = explode(';', $media->get_data());
    $content = '
			<div class="row">
				<form method = "post" action = "' . ADMINURL . '/mediamanager/edit/' . $media->get_id() . '/" enctype="multipart/form-data">
					<div class="col-xs-3">
						<div class="box">
							<div class = "box-header with-border">
								Загуженный файл
							</div>
							<div class = "box-body">
								<p><img src = "/uploads/' . $media->get_name() . '" alt = "' . $media->get_description() . '" class = "img-responsive"></p>
								<p><a href = "/uploads/' . $media->get_name() . '" id = "copyMediaUrl"><i class = "fa fa-copy"></i> ' . $media->get_name() . '</a></p>
							</div>
						</div>
					</div>
					<div class="col-xs-9">
						<div class="box">
							<div class = "box-body">
								<div class="form-group">
									<label for="file">Описание файла</label>
									<input type = "text" class="form-control" name="description" id="description" value = "' . $media->get_description() . '">
								</div>
								<div class="form-group">
									<label for="description">Доступные размеры:</label>
									<div class = "row">';
    foreach ($sizes as $size) {
        $size = explode('x', $size);
        $content .= '
										<div class = "col-xs-3">
											<p><a href = "/uploads/' . $media->get_name($size[0], $size[1]) . '" id = "copyMediaUrl"><i class = "fa fa-copy"></i> ' . $size[0] . 'x' . $size[1] . '</a></p>
										</div>';
    }
    $content .= '
									</div>
								</div>
								<div class="form-group">
									<label for="size">Свой размер</label>
									<input type="text" class = "form-control" name = "size[]" value = "" id = "size">
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
    add_jscript('$(document).on(\'click\', \'#copyMediaUrl\', function() {
			$(\'body\').append(\'<textarea id = "forCopy">\' + $(this).attr(\'href\') + \'</textarea>\');
			var ta = document.getElementById(\'forCopy\');
			ta.focus();
			ta.select();
			try { 
				document.execCommand(\'copy\'); 
			} catch(err) {
				return true;
			}
			window.getSelection().removeAllRanges();
			$(\'#forCopy\').remove();
			return false;
		});');
    set_content($content);
    add_breadcrumb('Менеджер медиа файлов', ADMINURL . '/mediamanager/', 'fa-file-image-o');
    set_active_admin_menu('mediamanager');
    set_title('Просмотр файла');
    set_tpl('index.php');
}

function media_edit($args)
{
    $media = new Media($args[0]);
    if (!$media->get_id())
        wserror();
    $media->set_description($_POST['description']);
    $data = explode(';', $media->get_data());
    if ($_POST['size'] && is_array($_POST['size'])) {
        foreach ($_POST['size'] as $sizes) {
            foreach (explode(';', $sizes) as $size) {
                if (!in_array($size, $data)) {
                    $size = explode('x', $size);
                    if (is_array($size) && count($size) == 2) {
                        $result = image_resize('uploads/' . $media->get_name(), $size[0], $size[1], true);
                        if ($result) {
                            array_push($data, $size[0] . 'x' . $size[1]);
                        }
                    }
                }
            }
        }
    }
    if ($data) {
        usort($data, 'media_sort');
        $media->set_data(implode(';', $data));
    }
    $media->update();
    alertS('Изменения успешно сохранены', ADMINURL . '/mediamanager/editform/' . $media->get_id() . '/');
}

function media_delete($args)
{
    $media = new Media($args[0]);
    if (!$media->get_id())
        wserror();
    foreach (explode(';', $media->get_data()) as $size) {
        $size = explode('x', $size);
        unlink('uploads/' . $media->get_name($size[0], $size[1]));
    }
    unlink('uploads/' . $media->get_name());
    $media->delete();
    alertS('Файлы успешно удалены', ADMINURL . '/mediamanager/');
}

function logout()
{
    clear_cookie('admin_token');
    redirect(ADMINURL . '/');
}

?>