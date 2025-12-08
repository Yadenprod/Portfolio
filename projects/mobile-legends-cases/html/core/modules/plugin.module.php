<?php
	function include_plugin_files($plugindir) {
		$dir = PLUGINFOLDER.'/'.$plugindir.'/';
		$skip = array('.', '..');
		$files = scandir($dir);
		if (in_array('functions.php', $files)) {
			$files = array_splice($files, array_search('functions.php', $files), 1) + $files;
		}
		foreach($files as $key => $filename) {
			if(!in_array($filename, $skip)) {
				if (strstr($filename,'.php')) {
					require_once($dir.$filename);
				}
			}
		}
	}
	
	function get_plugin_data($plugin_name) {
		return pm()->get_plugin_data($plugin_name);
	}
	
	function get_plugins_list() {
		return pm()->get_plugins_list();
	}
	
	function add_plugin_dependencies($list) {
		foreach ($list as $name) {
			if (!pm()->is_plugin_enabled($name)) {
				throw new \Exception("Неудовлетворенная зависимость " . $name);
			}
		}
	}

	function add_app($pattern, $app, $exec = true, $position = 5) {
		pm()->add_app($pattern, $app, $exec, $position);
	}

	function add_get($pattern, $app, $exec = true, $position = 5) {
		pm()->add_get($pattern, $app, $exec, $position);
	}

	function add_post($pattern, $app, $exec = true, $position = 5) {
		pm()->add_post($pattern, $app, $exec, $position);
	}
	
	function add_admin_app($pattern, $app, $exec = true, $position = 5) {
		pm()->add_admin_app($pattern, $app, $exec, $position);
	}
	
	function add_admin_get($pattern, $app, $exec = true, $position = 5) {
		pm()->add_admin_get($pattern, $app, $exec, $position);
	}
	
	function add_admin_post($pattern, $app, $exec = true, $position = 5) {
		pm()->add_admin_post($pattern, $app, $exec, $position);
	}
	
	function add_loader($func, $exec = true) {
		pm()->add_loader($func, $exec);
	}
	
	function add_admin_loader($func) {
		pm()->add_admin_loader($func);
	}
	
	function add_installer($name, $func) {
		pm()->add_installer($name, $func);
	}
	
	function add_uninstaller($name, $func) {
		pm()->add_uninstaller($name, $func);
	}
	
	function pmstop() {
		pm()->stop();
	}
	
	function pmstart() {
		pm()->start();
	}
?>