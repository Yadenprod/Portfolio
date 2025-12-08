<?php

/*
  Name : MobileLegends
  Description : Плагин для интеграции с Mobile Legends Bang Bang
  Author : AI Assistant
  Version : 1.0
 */

include_plugin_files('mobilelegends/class');
include_plugin_files('mobilelegends/modules');
include_plugin_files('mobilelegends/admin/api');
include_plugin_files('mobilelegends/admin/menu');
include_plugin_files('mobilelegends/admin/web');
include_plugin_files('mobilelegends/user/api');
include_plugin_files('mobilelegends/user/web');
include_plugin_files('mobilelegends/install');

function mobilelegends_install() {
    // Подключаем SQL-файл с таблицами для Mobile Legends
    $lines = file(CMSFOLDER . 'mobile_legends_tables.sql');
    $templine = '';
    foreach ($lines as $line) {
        if (substr($line, 0, 2) == '--' || $line == '' || substr($line, 0, 2) == '/*') {
            continue;
        }
        $templine .= $line;
        if (substr(trim($line), -1, 1) == ';') {
            db()->query($templine);
            $templine = '';
        }
    }
    
    // Регистрируем страницы для Mobile Legends
    $page = new page();
    
    $page->set_namepage('Mobile Legends Cases');
    $page->set_title('Mobile Legends Cases - Открывай кейсы и получай предметы!');
    $page->set_title_page('Mobile Legends Cases');
    $page->set_meta_des('Открывай кейсы Mobile Legends Bang Bang и получай скины, героев и другие предметы');
    $page->set_meta_key('mobile legends, кейсы, открытие кейсов, скины, герои');
    $page->set_url('/mobilelegends/cases/');
    $page->set_tpl('index.php');
    $page->set_content('<ml-cases></ml-cases>');
    $page->add();
    
    $page->set_namepage('Mobile Legends Профиль');
    $page->set_title('Профиль Mobile Legends - Управляй своими предметами');
    $page->set_title_page('Профиль Mobile Legends');
    $page->set_meta_des('Управляй своими предметами Mobile Legends, просматривай инвентарь');
    $page->set_meta_key('mobile legends, профиль, инвентарь, предметы');
    $page->set_url('/mobilelegends/profile/');
    $page->set_tpl('index.php');
    $page->set_content('<ml-profile></ml-profile>');
    $page->add();
    
    // Добавляем меню в админку
    add_admin_menu_item('Mobile Legends', '/admin/mobilelegends/', 'gamepad');
    add_admin_menu_item('ML Кейсы', '/admin/mobilelegends/cases/', 'gift', 'Mobile Legends');
    add_admin_menu_item('ML Предметы', '/admin/mobilelegends/items/', 'certificate', 'Mobile Legends');
    add_admin_menu_item('ML Настройки', '/admin/mobilelegends/settings/', 'cogs', 'Mobile Legends');
} 