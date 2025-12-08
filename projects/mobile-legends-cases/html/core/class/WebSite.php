<?php
	class WebSite {
		protected static $instance = null;
		protected $db = null;
		protected $settings = null;
		protected $webpage = null;
		protected $pluginmanager = null;
		protected $cache = null;
		protected $device = null;
		protected $user = null;
		protected $admin = null;
		protected $time_start = 0;

		public static function get_instance() {
			if (null === self::$instance) {
				self::$instance = new self();
			}
			return self::$instance;
		}

		protected function __construct() {}
		protected function __clone() {}
	
		function init() {
			$this->start();
			
			$this->preload();
			$this->load_core();

			$this->device = new device(true);
			$this->db = new DataBase();
			$this->cache = new Cache();
			$this->settings = new Settings();
			$this->pluginmanager = new PluginManager();
			$this->webpage = new Webpage();
			
			$this->load_language();
			$this->load_app();
			$this->load_admin();
			$this->admin_panel();
			$this->load_user();
			
			$this->pluginmanager->init();
			$this->webpage->render();
			
			$this->close();
		}

		function start() {
			ob_start();
			session_start();
			$this->time_start = microtime(true);
		}
		
		function close() {
			$this->cache->close();
			$this->db->close();
			ob_end_flush();
		}
		
		function preload() { 
			if (count($_GET) == 0) { 
				$gets = parse_url($_SERVER['REQUEST_URI']);
				parse_str(isset($gets['query'])? $gets['query'] : '', $_GET);
			}
		}
		
		function load_core() {
			$this->load_class();
			$this->load_modules();
		}
		
		function load_class() {
			$dir = COREFOLDER.'/class/';
			if (is_dir($dir)) {
				if ($dh  = opendir($dir)) {
					while ($filename = readdir($dh)) {
						if (strstr($filename,'.php') && $filename != 'WebSite.php')
							require_once($dir.$filename);
					}
				} else {
					echo 'Ошибка открытия директории<br>';
				}
			} else {
				echo $dir.' не является директорией<br>';
			}
		}
		
		function load_modules() {
			$dir = COREFOLDER.'/modules/';
			if (is_dir($dir)) {
				if ($dh  = opendir($dir)) {
					while ($filename = readdir($dh)) {
						if (strstr($filename,'.php'))
							require_once($dir.$filename);
					}
				} else {
					echo 'Ошибка открытия директории<br>';
				}
			} else {
				echo $dir.' не является директорией<br>';
			}
		}
		
		function load_app() {
			$this->load_app_class();
			$this->load_app_modules();
		}
		
		function load_app_class() {
			$dir = APPFOLDER.'/class/';
			if (is_dir($dir)) {
				if ($dh  = opendir($dir)) {
					while ($filename = readdir($dh)) {
						if (strstr($filename,'.php'))
							require_once($dir.$filename);
					}
				} else {
					echo 'Ошибка открытия директории<br>';
				}
			} else {
				echo $dir.' не является директорией<br>';
			}
		}
		
		function load_app_modules() {
			$dir = APPFOLDER.'/modules/';
			if (is_dir($dir)) {
				if ($dh  = opendir($dir)) {
					while ($filename = readdir($dh)) {
						if (strstr($filename,'.php'))
							require_once($dir.$filename);
					}
				} else {
					echo 'Ошибка открытия директории<br>';
				}
			} else {
				echo $dir.' не является директорией<br>';
			}
		}

		function load_admin() {
			$this->admin = new admin();
			$this->admin->auth();
		}
		
		function admin_panel() {
			if (is_admin_uri()) {
				$this->webpage->set_folder(default_admin_template_folder());
				if (preg_match('#^'.ADMINURL.'/$#', uri()) || preg_match('#^'.ADMINURL.'/login/$#', uri()) || is_admin()) 
					require_once(ADMINFOLDER.'/admin.php');
				else 
					redirect(ADMINURL.'/');
			}
		}

		function load_user() {
			$this->user = new user();
			$this->user->auth();
		}
		
		function load_language() {
			if (file_exists(CMSFOLDER.'/'.get_template_folder().'/language/default.php')) {
				require_once(CMSFOLDER.'/'.get_template_folder().'/language/default.php');
			} 
		}

		function get_webpage() {
			return $this->webpage;
		}

		function get_cache() {
			return $this->cache;
		}

		function get_db() {
			return $this->db;
		}

		function get_settings() {
			return $this->settings;
		}

		function get_pluginmanager() {
			return $this->pluginmanager;
		}

		function get_device() {
			return $this->device;
		}

		function get_user() {
			return $this->user;
		}

		function get_admin() {
			return $this->admin;
		}
		
		function get_time_start() {
			return $this->time_start;
		}
	}
?>