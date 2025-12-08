<?php
	function fixFloat($num, $decimals = 2) {
		$decimals = 10 ** $decimals;
		return round($num * $decimals) / $decimals;
	}
?>