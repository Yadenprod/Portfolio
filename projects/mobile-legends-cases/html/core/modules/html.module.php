<?php
	function html($elem) {
		$options = array();
		if (!is_array($elem))
			return $elem;
		foreach($elem as $key => $value) {
			if (!in_array($key, array('tag', 'value', 'singleTag', 'class', 'style', 'data')))
				array_push($options, $key.' = "'.$value.'"');
		}
		if (isset($elem['class'])) {
			if (is_array($elem['class'])) {
				if (count($elem['class']) > 0)
					array_push($options, 'class = "'.implode(' ', $elem['class']).'"');
			} else {
				if ($elem['class'] != '')
					array_push($options, 'class = "'.$elem['class'].'"');
			}
		}
		if (isset($elem['style'])) {
			if (is_array($elem['style'])) {
				if (count($elem['style']) > 0)
					array_push($options, 'style = "'.implode('; ', $elem['style']).'";');
			} else {
				if ($elem['style'] != '')
					array_push($options, 'style = "'.$elem['style'].'"');
			}
		}
		if (isset($elem['data'])) {
			if (is_array($elem['data'])) {
				if (count($elem['data']) > 0)
					foreach($elem['data'] as $key => $value) {
						array_push($options, 'data'.($key != ''? '-'.$key : '').' = "'.$value.'"');
					}
			} else {
				if ($elem['data'] != '')
					array_push($options, 'data = "'.$elem['data'].'"');
			}
		}
		$value = isset($elem['value'])? $elem['value'] : '';
		if (is_array($elem['value'])) {
			$value = '';
			foreach($elem['value'] as $el) {
				$value .= html($el);
			}
		}
		return '<'.(isset($elem['tag'])? $elem['tag'] : 'div').''.(count($options) > 0? ' '.implode(' ', $options) : '').'>'.$value.(!isset($elem['singleTag'])? '</'.(isset($elem['tag'])? $elem['tag'] : 'div').'>' : '');
	}
?>