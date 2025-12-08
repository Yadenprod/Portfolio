<?php

add_installer('disablepage', 'disablepage_plugin_install');
add_uninstaller('disablepage', 'disablepage_plugin_uninstall');

function disablepage_plugin_install() {
	add_setval('disabledsite', '0', 'Включить/выключить сайт', 'bool');
	add_setval('disablepage', 'disable.php', 'Страница отключения сайта', 'text');
	add_setval('disabletext', 'Сайт отключен для проведения технических работ.', 'Текст на странице отключения сайта', 'text');
}

function disablepage_plugin_uninstall() {
	delete_setval('disabledsite');
	delete_setval('disablepage');
	delete_setval('disabletext');
}
