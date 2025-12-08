<?php 
	class PluginManager {
		var $plugins = array();
		var $apps = array();
		var $loaders = array();
		var $installers = array();
		var $uninstallers = array();
		var $stop = false;
		
		function __construct() {
			$plugins = sel('plugins');
			$plugins_array = array();
			if ($plugins) {
				foreach ($plugins as $value) {
					$plugins_array[$value['name']] = $value; 
				}
			}
			$this->plugins = $plugins_array;
		}
		
		function init() {
			$this->test_plugins();
			if ($this->load_plugins()) {
				foreach ($this->loaders as $loader) {
					$func = $loader;
					if (function_exists($func)) $func();
				}
				usort($this->apps, array('PluginManager', 'app_sort'));
				foreach ($this->apps as $app) {
					$args = array();
					if (preg_match_all('#^'.$app['pattern'].'$#', uri(), $args, PREG_SET_ORDER)) {
						array_shift($args[0]);
						$func = $app['func'];
						if (function_exists($func) && !$this->stop) $func($args[0]);
					}
				}
			}
		}
		
		function get_plugins_name() {
			$plugins_name = array();
			if (is_array($this->plugins)) {
				foreach ($this->plugins as $key => $value) {
					$plugins_name[$key] = $value['name'];
				}
			}
			return $plugins_name;
		}
		
		function get_plugins_from_folder() {
			$dir = PLUGINFOLDER.'/';
			$skip = array('.', '..');
			$files = scandir($dir);
			$plugins = array();
			foreach($files as $key => $file) {
				if(!in_array($file, $skip))
					if (strstr($file,'.php')) {
						array_push($plugins, $file);
					}
			}
			return $plugins;
		}
		
		function test_plugins() {
			$folder_plugins = $this->get_plugins_from_folder();
			foreach($folder_plugins as $value) {
				if (!in_array($value, $this->get_plugins_name())) {
					$this->add_plugin($value);
				}
			}
			foreach ($this->get_plugins_name() as $value) {
				if (!in_array($value, $folder_plugins)) {
					$this->delete_plugin($value);
				}
			}
			
		}
		
		function get_plugin_data($plugin_name) {
			return $this->plugins[$plugin_name] ?? false;
		}
		
		function get_plugins_list() {
			return $this->plugins;
		}
		
		function is_plugin_enabled($plugin_name) {
			if (isset($this->plugins[$plugin_name.'.php']) && $this->plugins[$plugin_name.'.php']['enable'] == 1) {
				return true;
			}	
			return false;
		}


		function load_plugin($plugin_name) {
			$dir = PLUGINFOLDER.'/';
			$filename = $plugin_name;
			if ($this->plugins[$filename]['enable'] == '1') {
				try {
					require_once($dir.$filename);
				} catch (\Exception $ex) {
					$this->plugins[$filename]['error'] = $ex->getMessage();
				}
				return true;
			} else {
				return false;
			}
		}
		
		function load_plugins() {
			foreach ($this->plugins as $name => $plugin) {
				$this->load_plugin($name);
			}
			return true;
		}
		
		function add_plugin($name) {
			ins('plugins', array('name' => $name, 'enable' => 0));
			$this->plugins[$name] = array('name' => $name, 'enable' => 0);
		}
		
		function delete_plugin($name) {
			del('plugins', array('name' => $name));
			unset($this->plugins[$name]);
		}
		
		function add_app($pattern, $app, $exec = true, $position = 5) {  
			if ($exec)
				array_push($this->apps, array('pattern' => $pattern, 'func' => $app, 'position' => $position));
		}

		function add_get($pattern, $app, $exec = true, $position = 5) {  
			$this->add_app($pattern, $app, $_SERVER['REQUEST_METHOD'] == 'GET' && $exec, $position);
		}

		function add_post($pattern, $app, $exec = true, $position = 5) {  
			$this->add_app($pattern, $app, $_SERVER['REQUEST_METHOD'] == 'POST' && $exec, $position);
		}
		
		function add_admin_app($pattern, $app, $exec = true, $position = 5) {
			$this->add_app(ADMINURL.$pattern, $app, is_admin() && $exec, $position);
		}
		
		function add_admin_get($pattern, $app, $exec = true, $position = 5) {
			$this->add_app(ADMINURL.$pattern, $app, $_SERVER['REQUEST_METHOD'] == 'GET' && is_admin() && $exec, $position);
		}
		
		function add_admin_post($pattern, $app, $exec = true, $position = 5) {
			$this->add_app(ADMINURL.$pattern, $app, $_SERVER['REQUEST_METHOD'] == 'POST' && is_admin() && $exec, $position);
		}
		
		function add_loader($func, $exec = true) {
			if ($exec)
				array_push($this->loaders, $func);
		}
		
		function add_admin_loader($func) {
			$this->add_loader($func, is_admin());
		}
		
		function add_installer($name, $func) {
			array_push($this->installers, array('plugin' => $name , 'func' => $func));
		}
		
		function add_uninstaller($name, $func) {
			array_push($this->uninstallers, array('plugin' => $name, 'func' => $func));
		}
		
		function stop() {
			$this->stop = true;
		}
		
		function start() {
			$this->stop = false;
		}
		
		static function app_sort($a, $b) {
			if ($a['position'] == $b['position'])
				return 0;
			return $a['position'] < $b['position']? -1 : 1;
		}
	}
?>