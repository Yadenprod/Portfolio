<?php

add_app('/upgrade/', 'mode_upgrade_index');

function mode_upgrade_index() {
	set_content('');
	set_title('Апгрейд');
	set_title_page('Апгрейд');
	set_tpl('upgrade.php');
}
