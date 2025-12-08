<?php 
	function is_admin() {
		return admin()->get_login();
	}
	
	function get_admin() {
		return admin();
	}
	
	function get_admin_name() {
		return admin()->get_name();
	}
	
	function add_admin_menu($func) {
		if (is_admin_uri()) {
			if (function_exists($func)) {
				add_menu('admin', $func());
			}
		}
	}
	
	function add_admin_dashboard($func) {
		if (is_admin_uri()) {
			if (function_exists($func)) {
				global $admin_dashboard;
				$admin_dashboard[] = $func();
			}
		}
	}
	
	function add_admin_navbar($func) {
		if (is_admin_uri()) {
			if (function_exists($func)) {
				global $admin_navbar;
				$admin_navbar[] = $func();
			}
		}
	}
	
	function is_admin_uri() {
		return preg_match('#^'.ADMINURL.'/#', uri());
	}
	
	function set_active_admin_menu($needKey) {
		$admin_menu = get_menu('admin');
		if (is_array($admin_menu)) {
			foreach ($admin_menu as $key => $value) {
				if (isset($value['key']) && $value['key'] == $needKey)
					$admin_menu[$key]['active'] = true;
				if (isset($value['menu']) && is_array($value['menu'])) {
					foreach ($value['menu'] as $keym => $valuem ) {
						if (isset($valuem['key']) && $valuem['key'] == $needKey) {
							$admin_menu[$key]['menu'][$keym]['active'] = true;
							$admin_menu[$key]['active'] = true;
						}
					}
				}
			}
		}
		set_menu('admin', $admin_menu);
	}
	
	function admin_menu() {
		$admin_menu = get_menu('admin');
		if (is_array($admin_menu))
			usort($admin_menu, 'cmp');
		return $admin_menu;
	}

	function get_admin_menu() {
        $admin_menu = get_menu('admin');
		$menu = '';
		if (is_array($admin_menu)) {
			usort($admin_menu, 'cmp');
			foreach ($admin_menu as $key => $value) {
				$icon = 'fa-file';
				if (isset($value['icon'])) {
					$icon = $value['icon'];
				}
                $menu .= '
                <li class="'.(isset($value['menu']) && is_array($value['menu'])? 'treeview' : '').(isset($value['active']) && $value['active']?' active':'').'">
					<a href="'.(isset($value['url'])? $value['url'] : '#').'">
                    <i class="fa '.$icon.'"></i> <span>'.$value['name'].'</span>
                        '.(isset($value['menu']) && is_array($value['menu'])?
                        '<span class="pull-right-container">
                            <i class="fa fa-angle-left pull-right"></i>
                        </span>' :
                        '').'
                    </a>';
                if (isset($value['menu'])) {
                    $menu .= '<ul class="treeview-menu">';
                    if (is_array($value['menu'])) {
                        foreach ($value['menu'] as $keym => $valuem ) {
                            $subicon = 'fa-circle-o';
                            if (isset($valuem['icon'])) {
                                $subicon = $valuem['icon'];
                            }
                            $menu .= '<li'.(isset($valuem['active']) && $valuem['active']?' class = "active"':'').'><a href="'.$valuem['url'].'"><i class="fa '.$subicon.'"></i> '.$valuem['text'].'</a></li>';
                        }
                    }
                    $menu .= '</ul>';
                }
                $menu .= '</li>';
			}
		}
		return $menu;
    }
	
	function get_admin_dashboard() {
		global $admin_dashboard;
		$dashboard = '';
		if (is_array($admin_dashboard)) {
			usort($admin_dashboard, 'cmp');
			foreach ($admin_dashboard as $raw) {
				$dashboard .= '<div class = "row">';
				if (is_array($raw['cols'])) { 
					foreach ($raw['cols'] as $col ) {
						$size = array();
						if (!empty($col['size'])) {
							if (is_array($col['size'])) {
								foreach($col['size'] as $s) {
									array_push($size, 'col-'.$s);
								}
							} else {
								array_push($size, 'col-'.$col['size']);
							}
						}
						$size = implode(' ', $size);
						$dashboard .= '
							<section class="'.$size.(isset($col['class']) && $col['class']? ' '.$col['class'] : '').'">
								'.(isset($col['content']) && $col['content']? $col['content'] : '').'
							</section>
						';
					}
				}
				$dashboard .= '</div>';
			}
		}
		return $dashboard;
	}
	
	function the_admin_dashboard() {
		echo get_admin_dashboard();
	}
	
	function get_admin_navbar() {
		global $admin_navbar;
		$navbar = '';
		if (is_array($admin_navbar)) {
			usort($admin_navbar, 'cmp');
			foreach ($admin_navbar as $key => $nav) {
				$navbar .= '
					<li class="dropdown messages-menu" id = "'.(isset($nav['key']) ? $nav['key'] : 'navbar-'.$key).'">
						<a href="#" class="dropdown-toggle" data-toggle="dropdown">
						  <i class="fa '.(isset($nav['icon']) ? $nav['icon'] : 'fa-info').'"></i>
						  '.(isset($nav['label']) && is_array($nav['label']) ? '<span class="label label-'.(isset($nav['label']['class'])? $nav['label']['class'] : 'default').'">'.(isset($nav['label']['content'])? $nav['label']['content'] : '!').'</span>' : '').'
						</a>
						'.(isset($nav['content'])? 
						'<ul class="dropdown-menu">
						'.$nav['content'].'
						</ul>' : '').'
					</li>
				';
			}
		}
		return $navbar;
	}
	
	function the_admin_navbar() {
		echo get_admin_navbar();
	}
?>