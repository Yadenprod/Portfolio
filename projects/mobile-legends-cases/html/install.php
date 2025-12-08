<?php

$config = [
	'uploadUser' => 'admin',
	'adminPassword' => '12345',
	'settings' => [
		'site_name' => 'Mobile Legends Cases',
		'current_template_folder' => 'mlegendsdrop',
		'site_url' => 'localhost',
		'steamauth_loginDomen' => 'localhost',
		'steamauth_apiKey' => '99ED03D2F75DC95ED2FDC17BEC9D93B8',
		'opencase_gameid' => 'ml_bang', // ID для Mobile Legends Bang Bang
	]
];

define('CMSSECRET', 'QVM6REpIQTpTSkQgQVNKIERBU0pORCBB');
define('CMSFOLDER', dirname(__FILE__) . '/');
define('APPFOLDER', CMSFOLDER . '/app');
define('COREFOLDER', CMSFOLDER . '/core');
define('SETTINGSFOLDER', COREFOLDER . '/settings');
define('PLUGINFOLDER', APPFOLDER . '/plugins');
define('ADMINURL', '/admin');

if (!is_dir(CMSFOLDER . 'public/uploads')) {
	mkdir(CMSFOLDER . 'public/uploads');
	exec("chown -R " . $config['uploadUser'] . " " . CMSFOLDER . 'public/uploads');
}

$ws = new WebSite($config);
$ws->loadSQLDump('cms.sql');
autocommit(true);
$ws->init();
$ws->addAdmin();
$ws->generateSSLKeys();
$ws->enablePlugins();
$ws->updateSettings();
$ws->loadItems();

class WebSite {

	private static $instance;
	private static $db;
	private static $pluginmanager;
	private static $settings;
	private static $admin;
	private static $config;
	private static $cache;

	public function __construct($config) {
		self::$config = $config;
		self::$instance = $this;
		$this->load_core();
		self::$db = new DataBase();
	}

	public function init() {
		self::$settings = new Settings();
		self::$pluginmanager = new PluginManager();
		self::$pluginmanager->test_plugins();
		self::$admin = new admin();
		self::$cache = new Cache();
		$_SERVER['REQUEST_METHOD'] = '';
		$_SERVER['REQUEST_URI'] = '';
	}

	public static function get_instance() {
		return self::$instance;
	}
	
	public function get_cache() {
		return self::$cache;
	}

	private function load_core() {
		$this->load_class();
		$this->load_modules();
	}

	private function load_class() {
		$dir = COREFOLDER . '/class/';
		if (is_dir($dir)) {
			if ($dh = opendir($dir)) {
				while ($filename = readdir($dh)) {
					if (strstr($filename, '.php') && $filename != 'WebSite.php')
						require_once($dir . $filename);
				}
			} else {
				echo 'Ошибка открытия директории<br>';
			}
		} else {
			echo $dir . ' не является директорией<br>';
		}
	}

	private function load_modules() {
		$dir = COREFOLDER . '/modules/';
		if (is_dir($dir)) {
			if ($dh = opendir($dir)) {
				while ($filename = readdir($dh)) {
					if (strstr($filename, '.php'))
						require_once($dir . $filename);
				}
			} else {
				echo 'Ошибка открытия директории<br>';
			}
		} else {
			echo $dir . ' не является директорией<br>';
		}
	}

	public function get_db() {
		return self::$db;
	}

	public function get_pluginmanager() {
		return self::$pluginmanager;
	}

	public function get_settings() {
		return self::$settings;
	}

	function get_admin() {
		return self::$admin;
	}

	public function addAdmin() {
		$admin = new admin();
		$admin->set_name('admin');
		$admin->set_password(admin::hash_password(self::$config['adminPassword']));
		$admin->add();
	}

	public function loadSQLDump($filename) {
		$lines = file($filename);
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
		echo "SQL DUMP " . $filename . " LOADED\n";
	}

	public function generateSSLKeys() {
		require_once(APPFOLDER . '/plugins/opencase/class/encrypter.php');
		encrypter::generateKeyPair(encrypter::BOT_KEY_NAME);
		encrypter::generateKeyPair(encrypter::SITE_KEY_NAME);
		echo "SSL KEYS GENERATED\n";
	}

	public function enablePlugins() {
		$pluginList = sel('plugins');
		do {
			$pluginsCount = count($pluginList);
			foreach ($pluginList as $pluginKey => $pluginData) {
				if ($pluginData['enable'] == 0) {
					try {
						require PLUGINFOLDER . '/' . $pluginData['name'];
						$name = str_replace('.php', '', $pluginData['name']);
						foreach (pm()->installers as $installer) {
							if ($installer['plugin'] == $name) {
								$func = $installer['func'];
								if (function_exists($func)) {
									$func();
								}
							}
						}
						qryo('UPDATE plugins SET enable = 1 WHERE id = ' . $pluginData['id'] . '');
						echo $name . " plugin installed\n";						
						self::$pluginmanager->plugins[$pluginData['name']]['enable'] = 1;
						unset($pluginList[$pluginKey]);
					} catch (\Exception $e) {
						
					}
				}
			}
		} while ($pluginsCount != count($pluginList));
	}
	
	public function updateSettings() {
		foreach (self::$config['settings'] as $key => $value) {
			update_setval($key, $value);
		}
		echo "SETTINGS UPDATED\n";
	}
	
	public function loadItems() {
		require_once(APPFOLDER . '/plugins/opencase/class/item.php');
		require_once(APPFOLDER . '/plugins/opencase/modules/functions.module.php');
		$item = new item();
		$success = $item->update_items_list($error);
		if ($success) {
			echo "ITEMS LIST UPDATED\n";
		} else {
			echo "ERROR ON UPDATE ITEMS LIST: " . $error . "\n";
		}
	}

}
