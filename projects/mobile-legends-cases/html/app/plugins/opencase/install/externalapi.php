<?php

add_installer('opencase', 'opencase_externalapi_install');
add_uninstaller('opencase', 'opencase_externalapi_uninstall');

function opencase_externalapi_install() {
	add_setval('api_scretkey', 'd6dd71c6b4afff8e9b58e2fc5472be81', 'Секретный ключ для работы с api', 'text');
}

function opencase_externalapi_uninstall() {
	delete_setval('api_scretkey');
}