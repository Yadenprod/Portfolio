<?php

function mobilelegends_admin() {
    $content = '
        <div class="row">
            <div class="col-xs-12">
                <div class="box">
                    <div class="box-header">
                        <h3 class="box-title">Управление Mobile Legends</h3>
                    </div>
                    <div class="box-body">
                        <p>Здесь вы можете управлять предметами и кейсами Mobile Legends Bang Bang.</p>
                        <ul>
                            <li><a href="' . ADMINURL . '/mobilelegends/cases/">Управление кейсами</a></li>
                            <li><a href="' . ADMINURL . '/mobilelegends/items/">Управление предметами</a></li>
                            <li><a href="' . ADMINURL . '/mobilelegends/settings/">Настройки интеграции</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    ';
    
    set_title('Mobile Legends');
    set_content($content);
    set_active_admin_menu('Mobile Legends');
}

function mobilelegends_cases_admin() {
    $content = '
        <div class="row">
            <div class="col-xs-12">
                <div class="box">
                    <div class="box-header">
                        <h3 class="box-title">Управление кейсами Mobile Legends</h3>
                        <div class="box-tools">
                            <a href="' . ADMINURL . '/mobilelegends/cases/add/" class="btn btn-primary btn-sm"><i class="fa fa-plus"></i> Добавить кейс</a>
                        </div>
                    </div>
                    <div class="box-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Название</th>
                                    <th>Цена</th>
                                    <th>Активен</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody id="cases-list">
                                <!-- Список кейсов будет загружен через AJAX -->
                                <tr>
                                    <td colspan="5" class="text-center">Загрузка данных...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <script>
            $(document).ready(function() {
                // Здесь будет AJAX для загрузки кейсов
                // ...
            });
        </script>
    ';
    
    set_title('Кейсы Mobile Legends');
    set_content($content);
    set_active_admin_menu('ML Кейсы');
}

function mobilelegends_items_admin() {
    $content = '
        <div class="row">
            <div class="col-xs-12">
                <div class="box">
                    <div class="box-header">
                        <h3 class="box-title">Управление предметами Mobile Legends</h3>
                        <div class="box-tools">
                            <a href="' . ADMINURL . '/mobilelegends/items/add/" class="btn btn-primary btn-sm"><i class="fa fa-plus"></i> Добавить предмет</a>
                        </div>
                    </div>
                    <div class="box-body">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Изображение</th>
                                    <th>Название</th>
                                    <th>Тип</th>
                                    <th>Редкость</th>
                                    <th>Цена</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody id="items-list">
                                <!-- Список предметов будет загружен через AJAX -->
                                <tr>
                                    <td colspan="7" class="text-center">Загрузка данных...</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        <script>
            $(document).ready(function() {
                // Здесь будет AJAX для загрузки предметов
                // ...
            });
        </script>
    ';
    
    set_title('Предметы Mobile Legends');
    set_content($content);
    set_active_admin_menu('ML Предметы');
}

function mobilelegends_settings_admin() {
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        // Сохранение настроек
        update_setval('ml_currency_rate', $_POST['ml_currency_rate']);
        update_setval('ml_min_withdraw', $_POST['ml_min_withdraw']);
        update_setval('ml_api_key', $_POST['ml_api_key']);
        update_setval('ml_api_url', $_POST['ml_api_url']);
        
        add_msg('Настройки успешно сохранены', 'success');
        redirect(ADMINURL . '/mobilelegends/settings/');
    }
    
    $content = '
        <div class="row">
            <div class="col-xs-12">
                <div class="box">
                    <form method="post">
                        <div class="box-header">
                            <h3 class="box-title">Настройки интеграции с Mobile Legends</h3>
                        </div>
                        <div class="box-body">
                            <div class="form-group">
                                <label for="ml_currency_rate">Курс обмена внутренней валюты на алмазы:</label>
                                <input type="text" name="ml_currency_rate" id="ml_currency_rate" class="form-control" value="' . get_setval('ml_currency_rate') . '">
                            </div>
                            <div class="form-group">
                                <label for="ml_min_withdraw">Минимальная сумма для вывода алмазов:</label>
                                <input type="text" name="ml_min_withdraw" id="ml_min_withdraw" class="form-control" value="' . get_setval('ml_min_withdraw') . '">
                            </div>
                            <div class="form-group">
                                <label for="ml_api_key">API ключ для интеграции с Mobile Legends:</label>
                                <input type="text" name="ml_api_key" id="ml_api_key" class="form-control" value="' . get_setval('ml_api_key') . '">
                            </div>
                            <div class="form-group">
                                <label for="ml_api_url">API URL для интеграции с Mobile Legends:</label>
                                <input type="text" name="ml_api_url" id="ml_api_url" class="form-control" value="' . get_setval('ml_api_url') . '">
                            </div>
                        </div>
                        <div class="box-footer">
                            <button type="submit" class="btn btn-primary">Сохранить</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    ';
    
    set_title('Настройки Mobile Legends');
    set_content($content);
    set_active_admin_menu('ML Настройки');
} 