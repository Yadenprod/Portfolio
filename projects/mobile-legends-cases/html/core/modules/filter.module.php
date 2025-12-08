<?php
	function filter($str, $name) {
		if (!empty($name)) {
			if (is_array($name)) {
				foreach($name as $filter) {
					if (function_exists('filter_'.$filter)) {
						$str = ('filter_'.$filter)($str);
					}
				}
			} elseif (is_string($name)) {
				if (function_exists('filter_'.$name)) {
					$str = ('filter_'.$name)($str);
				}
			}
		}
		return $str;
	}
?>