<?php 
	function date_sql_to_timestamp($date) {
		$arr1 = explode(" ", $date);
		$arrdate1 = explode("-", $arr1[0]);
		$arrtime1 = explode(":", $arr1[1]);
		return (mktime($arrtime1[0], $arrtime1[1], $arrtime1[2], $arrdate1[1],  $arrdate1[2],  $arrdate1[0]));
	}
	
	function datef($date) {
		return date_sql_to_timestamp($date);
	}

	function data_timestamp_to_sql($date) {
		return date('Y-m-d H:i:s', $date);
	}
	
	function date_delta_sql_time($timestatmp_start, $timestapm_end, $format = 'i') {
		$arr1 = explode(" ", $timestatmp_start);
 	 	$arr2 = explode(" ", $timestapm_end);  
 		$arrdate1 = explode("-", $arr1[0]);
  		$arrdate2 = explode("-", $arr2[0]);
  		$arrtime1 = explode(":", $arr1[1]);
  		$arrtime2 = explode(":", $arr2[1]);
  		$timestamp2 = (mktime($arrtime2[0], $arrtime2[1], 0, $arrdate2[1],  $arrdate2[2],  $arrdate2[0]));
  		$timestamp1 = (mktime($arrtime1[0], $arrtime1[1], 0, $arrdate1[1],  $arrdate1[2],  $arrdate1[0]));
  		if ($form == "i")
  			$difference = floor(($timestamp2 - $timestamp1)/60);
  		if ($form == "h")
  			$difference = floor(($timestamp2 - $timestamp1)/3600);
  		if ($form == "d")
  			$difference = floor(($timestamp2 - $timestamp1)/86400);
  		return ($difference);
	}
	
	function timedelt($timestatmp_start, $timestapm_end, $format = 'i') {
 		return delta_sql_time($timestatmp_start, $timestapm_end, $format);
	}
	
	function date_text_month($num) {
		$month = array(
			'01' => 'Январь',
			'02' => 'Февраль',
			'03' => 'Март',
			'04' => 'Апрель',
			'05' => 'Май',
			'06' => 'Июнь',
			'07' => 'Июль',
			'08' => 'Август',
			'09' => 'Сентябрь',
			'10' => 'Октябрь',
			'11' => 'Ноябрь',
			'12' => 'Декабрь'
		);
		if (is_integer($num) && $num < 10)
			$num = '0'.$num;
		return $month[$num];
	}
	
	function get_text_month($num) {
		return date_text_month($num);
	}
	
	function the_text_month($num) {
		echo get_text_month($num);
	}
	
	function date_day_in_month($num) {
		$month = array(
			'01' => 31,
			'02' => 29,
			'03' => 31,
			'04' => 30,
			'05' => 31,
			'06' => 30,
			'07' => 31,
			'08' => 31,
			'09' => 30,
			'10' => 31,
			'11' => 30,
			'12' => 31
		);
		if (is_integer($num) && $num < 10)
			$num = '0'.$num;
		return $month[$num];
	}
	
	function day_in_month($num) {
		return date_day_in_month($num);
	}
	
	function date_replace_ru_month($date) {
		$month = array(
			'January' => 'Января',
			'February' => 'Февраля',
			'March' => 'Марта',
			'April' => 'Апреля',
			'May' => 'Майя',
			'June' => 'Июня',
			'July' => 'Июля',
			'August' => 'Августа',
			'September' => 'Сентября',
			'October' => 'Октября',
			'November' => 'Ноября',
			'December' => 'Декабря'
		);
		foreach ($month as $key => $value ) {
			$date = str_replace($key, $value, $date);
		}
		return $date;
	}
	
	function replace_text_month($date) {
		return date_replace_ru_month($date);
	}
?>