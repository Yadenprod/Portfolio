<?php 
	function current_template_folder() {
		$settings = get_settings();
		if ($settings->get_setting_value('current_template_folder') == '')
			$folder = 'default';
		else {
			if (isset($_COOKIE['template']) && $_COOKIE['template'] != '') {
				$folder = $_COOKIE['template'];
			} else {
				$folder = $settings->get_setting_value('current_template_folder');
			}
		}
		return TPLFOLDER.'/'.$folder.'/';
	}
	
	function default_admin_template_folder() {
		return ADMINFOLDER.'/tpl/';
	}
	
	function get_template_folder() {
		$settings = get_settings();
		if ($settings->get_setting_value('current_template_folder') == '')
			$folder = 'default';
		else {
			if (isset($_COOKIE['template']) && $_COOKIE['template'] != '') {
				$folder = $_COOKIE['template'];
			} else {
				$folder = $settings->get_setting_value('current_template_folder');
			}
		}
		return '/tpl/'.$folder;
	}
	
	function the_template_folder() {
		echo get_template_folder();
	}
	
	function get_admin_template_folder() {
		return '/tpl/admin';
	}
	
	function the_admin_template_folder() {
		echo get_admin_template_folder();
	}
	
	function get_header($tpl = false, $echo = true) {
		$tpl = !$tpl? 'header' : 'header-'.$tpl;
		if ($echo)
			echo get_template($tpl);
		else
			return get_template($tpl);
	}
	
	function get_footer($tpl = false, $echo = true) {
		$tpl = !$tpl? 'footer' : 'footer-'.$tpl;
		if ($echo)
			echo get_template($tpl);
		else
			return get_template($tpl);
	}
	
	function get_sidebar($tpl = false) {
		$tpl = !$tpl? 'sidebar' : 'sidebar-'.$tpl;
		echo get_template($tpl);
	}
	
	function get_tpl_part($tpl) {
		echo get_template($tpl);
	}

	function get_template($tpl) {
		ob_start();
		$tpl = strpos($tpl, '.php') === false? $tpl.'.php' : $tpl;
		foreach (wp()->get_data() as $key => $value) {
			$$key = $value;
		}
		include wp()->get_folder().$tpl;
		return ob_get_clean();
	}
	
	function is_ajax() {
		return isset($_POST['ajax']) && $_POST['ajax'] == true;
	}
	
	function user_extentions($place) {
		$html = '';
		$meta = wp()->get_meta();
		usort($meta, 'scriptSotr');
		foreach ($meta as $m) {
			if ($place == 'header' && count($m['options']) > 0) {
				$options = array();
				if (is_array($m['options'])) {
					foreach($m['options'] as $key => $option) {
						array_push($options, $key.(!empty($option)? ' = "'.$option.'"' : ''));
					}
				}
				$html .= '<meta '.implode(' ', $options).'>';
			}
		}
		$link = wp()->get_link();
		usort($link, 'scriptSotr');
		foreach ($link as $l) {
			if ($place == 'header' && isset($l['src'])) {
				$options = array();
				if (is_array($l['options'])) {
					foreach($l['options'] as $key => $option) {
						array_push($options, $key.(!empty($option)? ' = "'.$option.'"' : ''));
					}
				}
				$html .= '<link href = "'.isset($l['src']).'"'.(count($options) > 0? ' '.implode(' ', $options) : '').'>';
			}
		}
		$css = wp()->get_css();
		usort($css, 'scriptSotr');
		foreach ($css as $cs) {
			if (isset($cs['place']) && $cs['place'] == $place && isset($cs['src'])) {
				$options = array();
				if (is_array($cs['options'])) {
					foreach($cs['options'] as $key => $option) {
						array_push($options, $key.(!empty($option)? ' = "'.$option.'"' : ''));
					}
				}
				$html .= '<link href = "'.$cs['src'].'" rel = "stylesheet" type = "text/css"'.(count($options) > 0? ' '.implode(' ', $options) : '').'>';
			}
		}
		$scripts = wp()->get_scripts();
		usort($scripts, 'scriptSotr');
		foreach ($scripts as $script) {
			if (isset($script['place']) && $script['place'] == $place && isset($script['src'])) {
				$options = array();
				if (is_array($script['options'])) {
					foreach($script['options'] as $key => $option) {
						array_push($options, $key.(!empty($option)? ' = "'.$option.'"' : ''));
					}
				}
				$html .= '<script src = "'.$script['src'].'"'.(count($options) > 0? ' '.implode(' ', $options) : '').'></script>';
			}
		}
		$jscripts = wp()->get_jscripts();
		usort($jscripts, 'scriptSotr');
		foreach ($jscripts as $jscript) {
			if (isset($jscript['place']) && $jscript['place'] == $place && isset($jscript['script']))
				$html .= '<script>'.$jscript['script'].'</script>'; 
		}
		return $html;
	}
	
	function head() {
		echo user_extentions('header');
	}
	
	function footer() {
		echo user_extentions('footer');
	}
	
	function scriptSotr($a, $b) {
		return $a['pos'] == $b['pos']? 0 : $a['pos'] > $b['pos']? 1 : -1;
	}

	function set_menu($key, $menu) {
		wp()->set_menu($key, $menu);
	}

	function add_menu($key, $menu) {
		wp()->add_menu($key, $menu);
	}

	function get_menu($key = false) {
		return wp()->get_menu($key);
	}
	
	function breadcrumbs() {
		$html = '';
		$breadcrumbs = wp()->get_breadcrumbs();
		foreach($breadcrumbs as $breadcrumb) {
			if (isset($breadcrumb['url']) && isset($breadcrumb['name']))
				$html .= '<li><a href="'.$breadcrumb['url'].'">'.($breadcrumb['icon']?'<i class="fa '.$breadcrumb['icon'].'"></i>' : '').' '.$breadcrumb['name'].'</a></li>';
		}
		echo $html;
	}
	
	function add_script($src, $pos = 10, $place = 'footer', $options = array()) {
		$find = false;
		foreach (wp()->get_scripts() as $script) {
			if ($script['src'] == $src)
				$find = true;
		}
		if (!$find)
			wp()->add_script($src, $pos, $place, $options);
	}
	
	function add_jscript($script, $pos = 10, $place = 'footer') {
		wp()->add_jscript($script, $pos, $place);
	}
	
	function add_css($src, $pos = 10, $place = 'header', $options = array()) {
		$find = false;
		foreach (wp()->get_css() as $css) {
			if ($css['src'] == $src)
				$find = true;
		}
		if (!$find)
			wp()->add_css($src, $pos, $place, $options);
	}
	
	function add_meta($options = array(), $pos = 10) {
		if (count($options) == 0)
			return;
		wp()->add_meta($options, $pos);
	}
	
	function add_link($src, $options = array(), $pos = 10) {
		wp()->add_link($src, $options, $pos);
	}
	
	function add_data($key, $value) {
		wp()->add_data($key, $value);
	} 
	
	function set_data($key, $value) {
		add_data($key, $value);
	}
	
	function get_data($key) {
		return wp()->get_data($key);
	}
	
	function add_breadcrumb($name, $url, $icon = '') {
		ws()->get_webpage()->add_breadcrumb($name, $url, $icon);
	}
	
	function cmp($a, $b) {
		if ($a['position'] == $b['position']) {
			return 0;
		}
		return ($a['position'] < $b['position']) ? -1 : 1;
	}
	
	function get_file_hash($filename) {
		if (file_exists(CMSFOLDER.$filename))
			return substr(hash('ripemd160', filectime(CMSFOLDER.$filename)), 0, 8);
		else
			return false;
	}

	function the_file_hash($filename) {
		echo get_file_hash($filename);
	}
	
	function get_tpl_hash($filename) {
		$filename = TPLFOLDER.'/'.get_setval('default_template_folder').'/'.$filename;
		return get_file_hash($filename);
	}

	function the_tpl_hash($filename) {
		echo get_tpl_hash($filename);
	}

	function get_src_hash($filename) {
		$hash = get_file_hash($filename);
		return $filename.($hash? '?hash='.$hash : '');
	}

	function the_src_hash($filename) {
		echo get_src_hash($filename);
	}
?>