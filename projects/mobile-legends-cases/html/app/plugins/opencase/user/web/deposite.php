<?php

add_app('/deposite/success/', 'deposite_success');
add_app('/deposite/fail/', 'deposite_fail');
add_app('/deposite/waiting/', 'deposite_waiting');

function deposite_success() {
	set_content('Оплата успешно произведена');
	set_title('Оплата успешно произведена');
	set_title_page('Оплата успешно произведена');
	set_tpl('page.php');
}

function deposite_fail() {
	set_content('Неудачная попытка оплаты');
	set_title('Неудачная попытка оплаты');
	set_title_page('Неудачная попытка оплаты');
	set_tpl('page.php');
}

function deposite_waiting() {
	set_content('Ожидание процесса подтверждения платежа со стороны платежной системы');
	set_title('Ожидание подтверждения');
	set_title_page('Ожидание подтверждения');
	set_tpl('page.php');
}