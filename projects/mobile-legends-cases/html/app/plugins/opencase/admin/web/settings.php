<?php

add_admin_get('/opencase/settings/', 'admin_opencase_settings');
add_admin_post('/opencase/settingssave/', 'admin_opencase_settingssave');

function admin_opencase_settings() {
	$content = '
			<div class = "row">
				<div class = "col-xs-12">
					<div class="nav-tabs-custom">
						<ul class="nav nav-tabs">
							<li class="active"><a href="#settings" data-toggle="tab">Настройки</a></li>
							<li><a href="#ref" data-toggle="tab">Реферальная система</a></li>
							<li><a href="#reg-bonus" data-toggle="tab">Бонус при регистрации</a></li>
							<li><a href="#qiwi" data-toggle="tab">Qiwi</a></li>
							<li><a href="#interkassa" data-toggle="tab">Interkassa</a></li>
							<li><a href="#freekassa" data-toggle="tab">Freekassa</a></li>
							<li><a href="#unitpay" data-toggle="tab">Unitpay</a></li>
						</ul>
						<div class="tab-content">
							<div class="active tab-pane" id="settings">
								<form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
									<div class = "form-group">
										<label for="opencase_chance">Окупаемость пользователей:</label>
										<input type = "text" class="form-control" name="opencase_chance" id="opencase_chance" value = "' . get_setval('opencase_chance') . '">
									</div>
									<div class = "form-group">
										<label for="opencase_gameid">Игра с которой работает OpenCase:</label>
										<select name = "opencase_gameid" id = "opencase_gameid" class = "form-control">
											<option value = "730"' . (get_setval('opencase_gameid') == 730 ? ' selected = "selected"' : '') . '>Counter Strike : Global Offensive</option>
											<option value = "570"' . (get_setval('opencase_gameid') == 570 ? ' selected = "selected"' : '') . '>Dota 2</option>
											<option value = "252490"' . (get_setval('opencase_gameid') == 252490 ? ' selected = "selected"' : '') . '>Rust</option>
										</select>
									</div>
									<div class = "form-group">
										<label for="opencase_userprofit">Доступный профит для пользователей:</label>
										<input type = "text" class="form-control" name="opencase_userprofit" id="opencase_userprofit" value = "' . get_setval('opencase_userprofit') . '">
									</div>
									
									<div class = "form-group">
										<label for="opencase_drop_only_have">Выпадение предметов которые есть на боте:</label>
										<select name = "opencase_drop_only_have" id = "opencase_drop_only_have" class = "form-control">
											<option value = "0"' . (get_setval('opencase_drop_only_have') == 0 ? ' selected = "selected"' : '') . '>Отключено</option>
											<option value = "1"' . (get_setval('opencase_drop_only_have') == 1 ? ' selected = "selected"' : '') . '>Включено</option>
										</select>
									</div>
									<div class = "form-group">
										<label for="opencase_freeopen">Бесплатное открытие 6ого кейса:</label>
										<select name = "opencase_freeopen" id = "opencase_freeopen" class = "form-control">
											<option value = "0"' . (get_setval('opencase_freeopen') == 0 ? ' selected = "selected"' : '') . '>Отключено</option>
											<option value = "1"' . (get_setval('opencase_freeopen') == 1 ? ' selected = "selected"' : '') . '>Включено</option>
										</select>
									</div>
									<div class = "form-group">
										<label for="opencase_deposit_check_day">Количество дней за которые считаются депозиты для открытия бесплатных кейсов:</label>
										<input type = "text" class="form-control" name="opencase_deposit_check_day" id="opencase_deposit_check_day" value = "' . get_setval('opencase_deposit_check_day') . '">
                                    </div>
                                    <div class = "form-group">
										<label for="steamauth_loginDomen">Домен для авторизации:</label>
										<input type = "text" class="form-control" name="steamauth_loginDomen" id="steamauth_loginDomen" value = "' . get_setval('steamauth_loginDomen') . '">
									</div>
                                    <div class = "form-group">
										<label for="steamauth_apiKey">Ключ Steam Web Api для логина на сайте:</label>
										<input type = "text" class="form-control" name="steamauth_apiKey" id="steamauth_apiKey" value = "' . get_setval('steamauth_apiKey') . '">
									</div>
                                    <div class = "form-group">
										<label for="api_scretkey">Секретный ключ для API:</label>
										<input type = "text" class="form-control" name="api_scretkey" id="api_scretkey" value = "' . get_setval('api_scretkey') . '">
									</div>
									<div class = "form-group">
										<label for="opencase_withdraw_type">Тип вывода предметов:</label>
										<select name = "opencase_withdraw_type" id = "opencase_withdraw_type" class = "form-control">
											<option value = "' . WITHDRAW_TYPE_ONLY_BOT . '"' . (get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_ONLY_BOT ? ' selected = "selected"' : '') . '>Только с ботов</option>
											<option value = "' . WITHDRAW_TYPE_ONLY_MARKET . '"' . (get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_ONLY_MARKET ? ' selected = "selected"' : '') . '>Только с market.csgo.com</option>
											<option value = "' . WITHDRAW_TYPE_BOT_AND_MARKET . '"' . (get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_BOT_AND_MARKET ? ' selected = "selected"' : '') . '>С ботов и с market.csgo.com, если нет на ботах</option>
											<option value = "' . WITHDRAW_TYPE_ONLY_ADMIN_VIVOD . '"' . (get_setval('opencase_withdraw_type') == WITHDRAW_TYPE_ONLY_ADMIN_VIVOD ? ' selected = "selected"' : '') . '>Только в ручную администратором</option>
										</select>
									</div>
									<div class = "form-group">
										<label for="opencase_auto_sell">Автопродажа предметов через время:</label>
										<select name = "opencase_auto_sell" id = "opencase_auto_sell" class = "form-control">
											<option value = "0"' . (get_setval('opencase_auto_sell') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('opencase_auto_sell') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
									</div>
									<div class = "form-group">
										<label for="opencase_auto_sell_time">Время, через которое предметы будут автоматически проданы(в минутах):</label>
										<input type = "text" class="form-control" name="opencase_auto_sell_time" id="opencase_auto_sell_time" value = "' . get_setval('opencase_auto_sell_time') . '">
									</div>
									<div class="form-group">
										<label for="opencase_global_sale">Дополнительная скидка на все кейсы:</label>
										<input type = "number" class="form-control" name="opencase_global_sale" id="opencase_global_sale" value = "' . get_setval('opencase_global_sale') . '">
									</div>
									<div class = "form-group">
										<label for="opencase_price_parser_key">Источник цен для предметов:</label>
										<select name = "opencase_price_parser_key" id = "opencase_price_parser_key" class = "form-control">';
											foreach (item::$price_keys_array as $key => $val) {
												$content .= '<option value = "'.$key.'"' . (get_setval('opencase_price_parser_key') == $key ? ' selected = "selected"' : '') . '>'.$val.'</option>';
											}
										$content .= '</select>
									</div>
									<div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
								</form>
                            </div>
							<div class="tab-pane" id="reg-bonus">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
									<div class = "form-group">
										<label for="opencase_regbalance">Бонус при регистрации:</label>
										<input type = "text" class="form-control" name="opencase_regbalance" id="opencase_regbalance" value = "' . get_setval('opencase_regbalance') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="reg_bonus_referral_test_csgo">Проверка на наличие CS:GO на аккаунте:</label>
                                        <select name = "reg_bonus_referral_test_csgo" id = "reg_bonus_referral_test_csgo" class = "form-control">
											<option value = "0"' . (get_setval('reg_bonus_referral_test_csgo') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('reg_bonus_referral_test_csgo') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="reg_bonus_referral_min_lvl">Минимальный уровень Steam для получения реферального вознаграждения:</label>
                                        <input type = "text" class="form-control" name="reg_bonus_referral_min_lvl" id="reg_bonus_referral_min_lvl" value = "' . get_setval('reg_bonus_referral_min_lvl') . '">
                                    </div>
									<div class = "form-group">
                                        <label for="reg_bonus_referral_test_vacban">Проверка на наличие VACBANA на аккаунте:</label>
                                        <select name = "reg_bonus_referral_test_vacban" id = "reg_bonus_referral_test_vacban" class = "form-control">
											<option value = "0"' . (get_setval('reg_bonus_referral_test_vacban') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('reg_bonus_referral_test_vacban') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="reg_bonus_referral_test_time_create">Проверка на дату регистрации аккаунта:</label>
                                        <select name = "reg_bonus_referral_test_time_create" id = "reg_bonus_referral_test_time_create" class = "form-control">
											<option value = "0"' . (get_setval('reg_bonus_referral_test_time_create') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('reg_bonus_referral_test_time_create') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="reg_bonus_referral_mintime_from_create">Минимальное количества дней с момента регистрации в стиме, для получения реферального вознаграждения:</label>
                                        <input type = "text" class="form-control" name="reg_bonus_referral_mintime_from_create" id="reg_bonus_referral_mintime_from_create" value = "' . get_setval('reg_bonus_referral_mintime_from_create') . '">
                                    </div>
									<div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
							<div class="tab-pane" id="ref">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
									<div class = "form-group">
                                        <label for="ref_referral_rewards">Вознаграждение нового пользователя, пришедшего по реферальной ссылке:</label>
                                        <input type = "text" class="form-control" name="ref_referral_rewards" id="ref_referral_rewards" value = "' . get_setval('ref_referral_rewards') . '">
                                    </div>									
									<div class = "form-group">
                                        <label for="ref_referrer_rewards">Вознаграждение реферера за привлечение нового пользователя:</label>
                                        <input type = "text" class="form-control" name="ref_referrer_rewards" id="ref_referrer_rewards" value = "' . get_setval('ref_referrer_rewards') . '">
                                    </div>
									<div class = "form-group">
                                        <label for="ref_referrer_rewards_from_deposite">Вознаграждение реферера при депозите реферала (%):</label>
                                        <input type = "text" class="form-control" name="ref_referrer_rewards_from_deposite" id="ref_referrer_rewards_from_deposite" value = "' . get_setval('ref_referrer_rewards_from_deposite') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="ref_referral_test_csgo">Проверка на наличие CS:GO на аккаунте:</label>
                                        <select name = "ref_referral_test_csgo" id = "ref_referral_test_csgo" class = "form-control">
											<option value = "0"' . (get_setval('ref_referral_test_csgo') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('ref_referral_test_csgo') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="ref_referral_min_lvl">Минимальный уровень Steam для получения реферального вознаграждения:</label>
                                        <input type = "text" class="form-control" name="ref_referral_min_lvl" id="ref_referral_min_lvl" value = "' . get_setval('ref_referral_min_lvl') . '">
                                    </div>
									<div class = "form-group">
                                        <label for="ref_referral_test_vacban">Проверка на наличие VACBANA на аккаунте:</label>
                                        <select name = "ref_referral_test_vacban" id = "ref_referral_test_vacban" class = "form-control">
											<option value = "0"' . (get_setval('ref_referral_test_vacban') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('ref_referral_test_vacban') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="ref_referral_test_time_create">Проверка на дату регистрации аккаунта:</label>
                                        <select name = "ref_referral_test_time_create" id = "ref_referral_test_time_create" class = "form-control">
											<option value = "0"' . (get_setval('ref_referral_test_time_create') == 0 ? ' selected = "selected"' : '') . '>Отключена</option>
											<option value = "1"' . (get_setval('ref_referral_test_time_create') == 1 ? ' selected = "selected"' : '') . '>Включена</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="ref_referral_mintime_from_create">Минимальное количества дней с момента регистрации в стиме, для получения реферального вознаграждения:</label>
                                        <input type = "text" class="form-control" name="ref_referral_mintime_from_create" id="ref_referral_mintime_from_create" value = "' . get_setval('ref_referral_mintime_from_create') . '">
                                    </div>
									<div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
							<div class="tab-pane" id="qiwi">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
                                    <div class = "form-group">
                                        <label for="deposite_qiwi_enable">Включить способ оплаты:</label>
                                        <select name = "deposite_qiwi_enable" id = "deposite_qiwi_enable" class = "form-control">
											<option value = "0"' . (get_setval('deposite_qiwi_enable') == 0 ? ' selected = "selected"' : '') . '>Отключен</option>
											<option value = "1"' . (get_setval('deposite_qiwi_enable') == 1 ? ' selected = "selected"' : '') . '>Включен</option>
										</select>
                                    </div>
									<div class = "form-group">
                                        <label for="deposite_qiwi_merchant_id">Номер qiwi кошелька:</label>
                                        <input type = "text" class="form-control" name="deposite_qiwi_merchant_id" id="deposite_qiwi_merchant_id" value = "' . get_setval('deposite_qiwi_merchant_id') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_qiwi_secret">Секретный ключ:</label>
                                        <input type = "text" class="form-control" name="deposite_qiwi_secret" id="deposite_qiwi_secret" value = "' . get_setval('deposite_qiwi_secret') . '">
                                    </div>
									<div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
                            <div class="tab-pane" id="interkassa">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
                                    <div class = "form-group">
                                        <label for="deposite_interkassa_enable">Включить способ оплаты:</label>
                                        <select name = "deposite_interkassa_enable" id = "deposite_interkassa_enable" class = "form-control">
											<option value = "0"' . (get_setval('deposite_interkassa_enable') == 0 ? ' selected = "selected"' : '') . '>Отключен</option>
											<option value = "1"' . (get_setval('deposite_interkassa_enable') == 1 ? ' selected = "selected"' : '') . '>Включен</option>
										</select>
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_interkassa_merchant_id">ID магазина:</label>
                                        <input type = "text" class="form-control" name="deposite_interkassa_merchant_id" id="deposite_interkassa_merchant_id" value = "' . get_setval('deposite_interkassa_merchant_id') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_interkassa_secret">Секретный ключ:</label>
                                        <input type = "text" class="form-control" name="deposite_interkassa_secret" id="deposite_interkassa_secret" value = "' . get_setval('deposite_interkassa_secret') . '">
                                    </div>
                                    <div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
                            <div class="tab-pane" id="freekassa">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
                                     <div class = "form-group">
                                        <label for="deposite_freekassa_enable">Включить способ оплаты:</label>
                                        <select name = "deposite_freekassa_enable" id = "deposite_freekassa_enable" class = "form-control">
											<option value = "0"' . (get_setval('deposite_freekassa_enable') == 0 ? ' selected = "selected"' : '') . '>Отключен</option>
											<option value = "1"' . (get_setval('deposite_freekassa_enable') == 1 ? ' selected = "selected"' : '') . '>Включен</option>
										</select>
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_freekassa_merchant_id">ID магазина:</label>
                                        <input type = "text" class="form-control" name="deposite_freekassa_merchant_id" id="deposite_freekassa_merchant_id" value = "' . get_setval('deposite_freekassa_merchant_id') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_freekassa_secret_1">Секретный ключ №1:</label>
                                        <input type = "text" class="form-control" name="deposite_freekassa_secret_1" id="deposite_freekassa_secret_1" value = "' . get_setval('deposite_freekassa_secret_1') . '">
                                    </div>
                                     <div class = "form-group">
                                        <label for="deposite_freekassa_secret_2">Секретный ключ №2:</label>
                                        <input type = "text" class="form-control" name="deposite_freekassa_secret_2" id="deposite_freekassa_secret_2" value = "' . get_setval('deposite_freekassa_secret_2') . '">
                                    </div>
                                    <div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
                            <div class="tab-pane" id="unitpay">
                                <form action = "' .ADMINURL . '/opencase/settingssave/" method = "POST">
                                     <div class = "form-group">
                                        <label for="deposite_unitpay_enable">Включить способ оплаты:</label>
                                        <select name = "deposite_unitpay_enable" id = "deposite_unitpay_enable" class = "form-control">
											<option value = "0"' . (get_setval('deposite_unitpay_enable') == 0 ? ' selected = "selected"' : '') . '>Отключен</option>
											<option value = "1"' . (get_setval('deposite_unitpay_enable') == 1 ? ' selected = "selected"' : '') . '>Включен</option>
										</select>
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_unitpay_merchant_id">ID магазина:</label>
                                        <input type = "text" class="form-control" name="deposite_unitpay_merchant_id" id="deposite_unitpay_merchant_id" value = "' . get_setval('deposite_unitpay_merchant_id') . '">
                                    </div>
                                    <div class = "form-group">
                                        <label for="deposite_unitpay_secret">Секретный ключ:</label>
                                        <input type = "text" class="form-control" name="deposite_unitpay_secret" id="deposite_unitpay_secret" value = "' . get_setval('deposite_unitpay_secret') . '">
                                    </div>
                                    <div class = "form-group">
										<button type = "submit" class = "btn btn-success"><i class = "fa fa-save"></i> Сохранить</button>
									</div>
                                </form>
                            </div>
						</div>
					</div>
				</div>
			</div>
		';
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.css', 10);
	add_css(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.skinNice.css', 11);
	add_script(get_admin_template_folder() . '/plugins/ionslider/ion.rangeSlider.min.js', 10, 'footer');
	add_jscript(' $(function () {
			$("#opencase_chance").ionRangeSlider({
			  min: 0,
			  max: 300,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
			
			$("#opencase_global_sale").ionRangeSlider({
			  min: 0,
			  max: 100,
			  type: \'single\',
			  step: 1,
			  postfix: " %",
			  prettify: false,
			  hasGrid: true
			});
			
		});');
	set_active_admin_menu('opencasesettings');
	set_title('Настройки OpenCase');
	set_content($content);
	set_tpl('index.php');
}

function admin_opencase_settingssave() {
	$saveAsRust = false;
	$needChangeWithdrowType = false;
	$additionalInfo = '';
	foreach ($_POST as $key => $val) {
		if ($key == 'opencase_gameid' && $val == 252490) {
			$saveAsRust = true;
		}
		if ($key == 'opencase_withdraw_type' && $val != WITHDRAW_TYPE_ONLY_BOT) {
			$needChangeWithdrowType = true;
		}
		$needItemUpdate = false;
		if ($key == 'opencase_price_parser_key' && $val != get_setval('opencase_price_parser_key')) {
			$needItemUpdate = true;
		}
		update_setval($key, $val);
		if ($needItemUpdate) {
			$item = new item();
			$error = '';
			$success = $item->update_items_list($error);
			if ($success) {
				$additionalInfo = 'Предметы успешно обновлены согласно новому источнику.';
			}
		}
	}
	if ($saveAsRust && $needChangeWithdrowType) {
		update_setval('opencase_withdraw_type', WITHDRAW_TYPE_ONLY_BOT);
		alertW('Изменения успешно сохранены. ' . $additionalInfo . ' Тип вывода предметов перекдючен на "Только с ботов", так как только он доступен для выбранной игры.', ADMINURL . '/opencase/settings/');
	} else {
		alertS('Изменения успешно сохранены. ' . $additionalInfo, ADMINURL . '/opencase/settings/');
	}
}
