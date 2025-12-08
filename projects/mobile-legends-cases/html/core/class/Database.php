<?php
	class Database {
		var $db = '';
		var $error = '';
		var $error_reporting = 'all';
		var $last_query = '';
		var $num_rows = 0;
		var $time = 0;
		var $sum_time = 0;
		var $count = 0;
		
		function __construct($settings = false) {
			if (!$settings) {
				require_once SETTINGSFOLDER.'/DataBaseSet.php';
				$settings = $data_base_settings;
			}
			if ($settings['encoding'] == '') {
				$this->connect($settings['servername'], $settings['username'], $settings['password'], $settings['namedb']);
			} else {
				$this->connect($settings['servername'], $settings['username'], $settings['password'], $settings['namedb'], $settings['encoding']);
			}
		}
		
		function get_db() {
			return $this->db;
		}
		
		function get_error() {
			return $this->error;
		}
		
		function set_error($error) {
			$this->error = $error;
			if ($error != '') {
				add_log($error, 'SQL Error');
			}
			if ($this->error_reporting == 'all' && $error != '') {
				//die($error);
			}
		}

		function print_error() {
			echo $this->error;
		}

		function get_error_reporting() {
			return  $this->error_reporting;
		}
		
		function set_error_reporting($error_reporting) {
			$this->error_reporting = $error_reporting;
		}
		
		function get_encoding() {
			return mysqli_character_set_name($this->db);
		}
		
		function set_encoding($encoding) {
			$this->set_error('');
			if ($this->get_encoding() != $encoding) {
				if (mysqli_set_charset($this->db, $encoding)) {
					return true; 
				} else {
					$this->set_error('Ошибка изменения кодировки: '.mysqli_error($this->db));
					return false;
				}
			} else {
				return true;
			}
		}
		
		function connect($servername, $username, $password, $namedb, $encoding = false) {
			$this->set_error('');
			$this->db = mysqli_connect($servername, $username, $password); 
			if ($this->db) {
				if (mysqli_select_db($this->db, $namedb)) {
					if ($encoding) {
						if ($this->set_encoding($encoding)) {
							return true;
						} else {
							return false;
						}
					} else {
						return true;
					}
				} else {
					$this->set_error('Ошибка выбора базы данных: '.mysqli_error($this->db));
					return false;
				}
			} else {
				$this->set_error('Ошибка соеденения с базой данных: '.mysqli_error($this->db));
				return false;
			}
		}
		
		function close() {
			return mysqli_close($this->db);
		}
		
		function base_query($sql) {
			$time_start = microtime(true);
			$result = mysqli_query($this->db, $sql);
			$time_end = microtime(true);
			$this->set_time($time_end - $time_start);
			$this->inc_sum_time();
			$this->inc_count();
			$this->last_query = $sql;
			return $result;
		}
		
		function query($sql) { 
			$this->set_error('');
			$array = array();
			if ($result = $this->base_query($sql)) {
				if (is_object($result)) {
					$this->num_rows = mysqli_num_rows($result);
					$i = 0;
					while ($query = mysqli_fetch_assoc($result)) {
						$array[$i] = $query;
						$i++;
					}
					return $array;
				} else if ($result) {
					return true;
				} else {
					$this->num_rows = 0;
					return false;
				}
			} else {
				$this->set_error('Ошибка выполнения запроса ('.$sql.'): '.mysqli_error($this->db));
				return false;
			}
		}
		
		function query_once($sql) {
			$this->set_error('');
			if ($result = $this->base_query($sql)) {
				$this->set_num_rows(1);
				if  (is_object($result)) { 
					return mysqli_fetch_assoc($result);
				} else { 
					return false;
				}
			} else {
				$this->set_error('Ошибка выполнения запроса ('.$sql.'): '.mysqli_error($this->db));
				return false;
			}
		}
		
		function select($table, $where = false, $order = false, $limit = false) {
			$table = '`'.$this->nosqlinj($table).'`';
			$where = $this->where($where);
			$order = $this->order($order);
			$limit = $this->limit($limit);
			return $this->query('SELECT * FROM '.$table.$where.$order.$limit);
		}
		
		function select_once($table, $where = false, $order = false, $limit = 1) {
			$table = '`'.$this->nosqlinj($table).'`';
			$where = $this->where($where);
			$order = $this->order($order);
			$limit = $this->limit($limit);
			return $this->query_once('SELECT * FROM '.$table.$where.$order.$limit);
		}
		
		function insert($table, $values) {
			$table = '`'.$this->nosqlinj($table).'`';
			$keysArray = array();
			$valuesArray = array();
			foreach ($values as $key => $value) {
				array_push($keysArray, '`'.$this->nosqlinj($key).'`');
				array_push($valuesArray, $this->value($value));
			}
			return $this->query_once('INSERT INTO '.$table.' ('.implode(', ', $keysArray).') VALUES ('.implode(', ', $valuesArray).')');
		}
		
		function update($table, $values, $where = false, $order = false, $limit = false) {
			$table = '`'.$this->nosqlinj($table).'`';
			$valuesArray = array();
			foreach ($values as $key => $value) {
				$resultValue = '`'.$this->nosqlinj($key).'` = '.$this->value($value);
				array_push($valuesArray, $resultValue);
			}
			$values = count($valuesArray) > 0? ' SET '.implode(', ', $valuesArray) : '';
			$where = $this->where($where);
			$order = $this->order($order);
			$limit = $this->limit($limit);
			return $this->query_once('UPDATE '.$table.$values.$where.$order.$limit);
		}
		
		function delete($table, $where = false, $order = false, $limit = false) {
			$table = '`'.$this->nosqlinj($table).'`';
			$where = $this->where($where);
			$order = $this->order($order);
			$limit = $this->limit($limit);
			return $this->query_once('DELETE FROM '.$table.$where.$order.$limit);
		}
		
		function value($value) {
			if (is_int($value)) {
				$value = intval($value);
			} else if (is_float($value)) {
				$value = floatval($value);
			} else if (is_bool($value)) {
				$value = $value? 1 : 0;
			} else if ($value == 'NOW()') {
				$value = 'NOW()';
			} else if (is_string($value)) {
				$value = '"'.$this->nosqlinj($value).'"';
			} else if (is_array($value)) {
				$value = '"'.$this->nosqlinj(json_encode($value)).'"';
			} else {
				$value = '""';
			}
			return $value;
		}
		
		function where($params = false) {
			$whereArray = array();
			if ($params && is_array($params)) {
				foreach ($params as $key => $value) {
					$whereValue = '`'.$this->nosqlinj($key).'` = '.$this->value($value);
					array_push($whereArray, $whereValue);
				}
			} else if ($params && is_string($params)) {
				array_push($whereArray, $params);
			}
			$where = count($whereArray) > 0? ' WHERE '.implode(' and ', $whereArray) : '';
			return $where;
		}
		
		function order($params = false) {
			$orderArray = array();
			if ($params && is_array($params)) {
				foreach ($params as $key => $value) {
					if (is_string($value)) {
						$value = $value == 'DESC'? 'DESC' : 'ASC';
					} else if (is_int($value)) {
						$value = $value? 'DESC' : 'ASC';
					} else if (is_bool($value)) {
						$value = $value? 'DESC' : 'ASC';
					} else {
						$value = false;
					}
					$orderValue = '`'.$this->nosqlinj($key).'`'.($value? ' '.$value : '');
					array_push($orderArray, $orderValue);
				}
			} else if ($params && is_string($params)) {
				array_push($orderArray, $params);
			}
			$order = count($orderArray) > 0? ' ORDER BY '.implode(', ', $orderArray) : '';
			return $order;
		}
		
		function limit($params = false) {
			$limit = '';
			if ($params) {
				if (is_array($params)) {
					if (count($params) == 1) {
						$limit = ' LIMIT '.intval($params[0]);
					} else if (count($params) > 1) {
						$limit = ' LIMIT '.intval($params[0]).', '.intval($params[1]);
					} else {
						$limit = '';
					}
				} else if (is_int($params)) {
					$limit = ' LIMIT '.intval($params);
				} else if (is_string($params) && strlen($params) > 0) {
					$limit = ' LIMIT ' . $params;
				}
			}
			return $limit;
		}
		
		function transaction($name = false) {
			return $name? mysqli_begin_transaction($this->db, 0, $name) : mysqli_begin_transaction($this->db);
		}
		
		function commit($name = false) {
			return $name? mysqli_commit($this->db, 0, $name) : mysqli_commit($this->db);
		}
		
		function rollback($name = false) {
			return $name? mysqli_rollback($this->db, 0, $name) : mysqli_rollback($this->db);
		}
		
		function autocommit($mode = false) {
			return mysqli_autocommit($this->db, $mode);
		}
		
		function savepoint($name = '') {
			return mysqli_savepoint($this->db, $name);
		}
		
		function release_savepoint($name = '') {
			return mysqli_release_savepoint($this->db, $name);
		}

		function get_last_query() {
			return $this->last_query;
		}
		
		function get_last_id() {
			return mysqli_insert_id($this->db);
		}
		
		function nomysqlinj($str) {
			return mysqli_real_escape_string($this->db, $str);
		}
		
		function nosqlinj($str) {
			return $this->nomysqlinj($str);
		}

		function now() {
			$now = $this->query_once('SELECT NOW()');
			return $now['NOW()'];
		}
		
		function get_num_rows() {
			return $this->num_rows;
		}
		
		function set_num_rows($num_rows) {
			$this->num_rows = $num_rows;
		}
		
		function get_time() {
			return $this->time;
		}
		
		function set_time($time) {
			$this->time = $time;
		}
		
		function get_sum_time() {
			return $this->sum_time;
		}
		
		function set_sum_time($time) {
			$this->sum_time = $time;
		}
		
		function inc_sum_time($time = false) {
			$this->sum_time += $time? $time : $this->time;
		}
		
		function get_count() {
			return $this->count;
		}
		
		function set_count($number) {
			$this->count = $number;
		}
		
		function inc_count($number = 1) {
			$this->count += $number;
		}
	}
?>