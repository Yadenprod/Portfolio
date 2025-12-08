<?php
	function get_text_error($error) {
		$result = 'Not Found';
		switch($error) {
			case 301:
				$result = 'Moved Permanently';
				break;
			case 302:
				$result = 'Moved Temporarily';
				break;
			case 401:
				$result = 'Unauthorized';
				break;
			case 403:
				$result = 'Forbidden';
				break;
			case 404:
				$result = 'Not Found';
				break;
			case 429:
				$result = 'Too Many Requests';
				break;
			case 500:
				$result = 'Internal Server Error';
				break;
			case 502:
				$result = 'Bad Gateway';
				break;
			case 503:
				$result = 'Service Unavailable';
				break;
			case 504:
				$result = 'Gateway Timeout';
				break;
		}
		return $result;
	}
	
	function header_error($error = 404) {
		header('HTTP/1.0 '.$error.' '.get_text_error($error)); 
		header('HTTP/1.1 '.$error.' '.get_text_error($error)); 
		header('Status: '.$error.' '.get_text_error($error));
	}
	
	function wserror($error = 404) {
		header_error($error);
		set_data('error', $error);
		set_data('error_text', get_text_error($error));
		if (file_exists(wp()->get_folder().$error.'.php')) {
			wp()->set_tpl($error.'.php');
		} else if (file_exists(wp()->get_folder().'error.php')) {
			wp()->set_tpl('error.php');
		} else {
			wsexit();
		}
		wp()->render();
		wsexit();
	}
?>