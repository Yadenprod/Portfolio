<?php
	function query($sql) {
		return db()->query($sql);
	}
	
	function qry($sql) {
		return query($sql);
	}
	
	function q($sql) {
		return query($sql);
	}
	
	function query_once($sql) {
		return db()->query_once($sql);
	}
	
	function qryo($sql) {
		return query_once($sql);
	}
	
	function qo($sql) {
		return query_once($sql);
	}
	
	function sel($table, $where = false, $order = false, $limit = false) {
		return db()->select($table, $where, $order, $limit);
	}
	
	function selo($table, $where = false, $order = false, $limit = 1) {
		return db()->select_once($table, $where, $order, $limit);
	}
	
	function ins($table, $values) {
		return db()->insert($table, $values);
	}
	
	function upd($table, $values, $where = false, $order = false, $limit = false) {
		return db()->update($table, $values, $where, $order, $limit);
	}
	
	function del($table, $where = false, $order = false, $limit = false) {
		return db()->delete($table, $where, $order, $limit);
	}
	
	function value($value) {
		return db()->value($value);
	}
	
	function where($params = false) {
		return db()->where($params);
	}
	
	function order($params = false) {
		return db()->order($params);
	}
	
	function limit($params = false) {
		return db()->limit($params);
	}
	
	function nosqlinj($str) {
		return db()->nosqlinj($str);
	}
	
	function timeq($ms = true) {
		return $ms? intval(db()->get_time() * 1000) : db()->get_time();
	}
	
	function timesq($ms = true) {
		return $ms? intval(db()->get_sum_time() * 1000) : db()->get_sum_time();
	}
	
	function countq() {
		return db()->get_count();
	}

	function last_query() {
		return db()->get_last_query();
	}
	
	function lastID() {
		return db()->get_last_id();
	}
	
	function transaction($name = false) {
		return db()->transaction($name);
	}
	
	function commit($name = false) {
		return db()->commit($name);
	}
	
	function rollback($name = false) {
		return db()->rollback($name);
	}
	
	function autocommit($mode = false) {
		return db()->autocommit($mode);
	}
	
	function savepoint($name = '') {
		return db()->savepoint($name);
	}
	
	function release_savepoint($name = '') {
		return db()->release_savepoint($name);
	}

	function now() {
		return db()->now();
	}
?>