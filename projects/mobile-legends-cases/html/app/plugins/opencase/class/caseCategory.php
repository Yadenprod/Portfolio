<?php
	class caseCategory {
		var $id = '';
		var $name = '';
		var $pos = '';
		var $disable = '';

		function __construct($id = '') {
			if ($id != '') {
				$this->load_caseCategory(db()->nomysqlinj($id));
			}
		}

		function get_id() {
			return $this->id;
		}

		function set_id($id) {
			$this->id = $id;
		}

		function get_name() {
			return $this->name;
		}

		function set_name($name) {
			$this->name = $name;
		}

		function get_pos() {
			return $this->pos;
		}

		function set_pos($pos) {
			$this->pos = $pos;
		}
		
		function get_disable() {
			return $this->disable;
		}
		
		function set_disable($disable) {
			$this->disable = $disable;
		}

		function set_parametrs( $id, $name, $pos, $disable) { 
 			$this->set_id($id);
			$this->set_name($name);
			$this->set_pos($pos);
			$this->set_disable($disable);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['name'] != '')
				$this->set_name($_REQUEST['name']);
			if ($_REQUEST['pos'] != '')
				$this->set_pos($_REQUEST['pos']);
			if ($_REQUEST['disable'] != '')
				$this->set_disable($_REQUEST['disable']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_name('');
			$this->set_pos('');
			$this->set_disable('');
		}

		function  load_caseCategory($id) {
			$cache = ch()->get('caseCategory'.$id);
			if (!$cache) {
				$caseCategory = db()->query_once('select * from opencase_category where id = "'.$id.'"');
				$this->set_parametrs( $caseCategory['id'], $caseCategory['name'], $caseCategory['pos'], $caseCategory['disable']);
				if ($this->get_id() != '')
					ch()->set('caseCategory'.$id, $this);
			} else {
				$this->set_parametrs($cache->get_id(), $cache->get_name(), $cache->get_pos(), $cache->get_disable());
			}
		}

		function add_caseCategory() {
			db()->query_once('insert into opencase_category( name, pos, disable) values ( "'.$this->get_name().'", "'.$this->get_pos().'", "'.$this->get_disable().'")');
		}

		function update_caseCategory() {
			db()->query_once('update opencase_category set name = "'.$this->get_name().'", pos = "'.$this->get_pos().'", disable = "'.$this->get_disable().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('caseCategory'.$this->id, $this);
		}

		function delete_caseCategory() {
			db()->query_once('delete from opencase_category where id = "'.$this->get_id().'"');
			ch()->delete('caseCategory'.$this->id);
		}

		function get_caseCategorys($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_category';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$caseCategorysArray = db()->query($sql);
			$caseCategorys = array();
			if (is_array($caseCategorysArray)) {
				foreach ($caseCategorysArray as $caseCategoryElement) {
					$caseCategory = new caseCategory($caseCategoryElement['id']);
					array_push($caseCategorys, $caseCategory);
				}
			}
			return $caseCategorys;
		}
	}
?>