<?php

function getdatetime($date, $format = '') {
	if ($format == '') {
		return date('d.m.Y H:i:s', datef($date));
	}
	return date($format, datef($date));
}
