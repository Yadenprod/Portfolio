<?php
	function redirect($url) {
		ob_end_clean();
		header('Location: '.$url);
		exit();
	}
	
	function redirect301($url) {
		ob_end_clean();
		header("HTTP/1.1 301 Moved Permanently");
		header('Location: '.$url);
		exit();
	}
	
	function set_srv_msg($msg, $type = '') {
		if ($type == '')
			$_SESSION['srvmsg'] = $msg;
		else
			$_SESSION[$type] = $msg;
	}
	
	function redirect_srv_msg($msg, $url, $type = '') {
		if ($type == '')
			set_srv_msg($msg);
		else
			set_srv_msg($msg, $type);
		redirect($url);
	}
	
	function alert($msg, $url, $alert_type, $alert_icon, $alert_header, $type = '') {
		$msg = '<div class="alert '.$alert_type.' alert-dismissible">
				<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>
                <h4><i class="icon fa '.$alert_icon.'"></i> '.$alert_header.'</h4>
                '.$msg.'
              </div>';
		redirect_srv_msg($msg, $url, $type);
	}
	
	function alertS($msg, $url, $type = '') {
		alert($msg, $url, 'alert-success', 'fa-check', 'Успех!', $type);
	}
	
	function alertW($msg, $url, $type = '') {
		alert($msg, $url, 'alert-warning', 'fa-warning', 'Предупреждение!', $type);
	}
	
	function alertI($msg, $url, $type = '') {
		alert($msg, $url, 'alert-info', 'fa-info', 'Информация!', $type);
	}
	
	function alertE($msg, $url, $type = '') {
		alert($msg, $url, 'alert-danger', 'fa-ban', 'Ошибка!', $type);
	}

	function get_srv_msg($type = '') {
		if ($type == '') {
			if (isset($_SESSION['srvmsg'])) {
				$srvmsg = $_SESSION['srvmsg'];
				unset($_SESSION['srvmsg']);
				return $srvmsg;
			}
			return '';
		} else {
			if (isset($_SESSION[$type]))
			{
				$srvmsg = $_SESSION[$type];
				unset($_SESSION[$type]);
				return $srvmsg;
			}
			return '';
		}
	}
	
	function get_n_srv_msg($type = '') {
		return $_SESSION['srvmsg'];
	}
	
	function get_cms_msg() {
		return get_srv_msg();
	}
?>