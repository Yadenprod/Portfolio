<?php
	function buble($arr, $func) {
		foreach ($arr as $i => $ivalue) {
			foreach ($arr as $j => $jvalue) {
				if($func($arr[$i], $arr[$j])) {
					$temp = $arr[$j];
					$arr[$j] = $arr[$i];
					$arr[$i] = $temp;
				}
			}         
		}
	}
?>