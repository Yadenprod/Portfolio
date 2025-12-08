<?php 
	class Media {
		var $id = 0;
		var $name = '';
		var $description = '';
		var $data = '';
		var $time = '';

		function __construct($id = false) {
			if ($id) 
				$this->load($id);
		}

		function get_id() {
			return (int)$this->id;
		}

		function set_id($id) {
			$this->id = (int)$id;
		}

		function get_name($width = false, $height = false) {
			if (!$width && !$height) {
				return $this->name;
			}
			$name = explode('.', $this->name);
			$name[count($name) - 2] .= '-'.($width? $width : $height).'x'.($height? $height : $width);
			return implode('.', $name);
		}

		function set_name($name) {
			$this->name = strip_tags(trim($name));
		}
		
		function get_image($width = false, $height = false, $classes = false) {
			return '<img src = "/uploads/'.$this->get_name($width, $height).'"'.($classes && is_array($classes)? ' class = "'.implode(' ', $classes).'"' : '').' title = "'.$this->get_description().'" alt = "'.$this->get_description().'">';
		}

		function get_description() {
			return strip_tags(trim($this->description));
		}

		function set_description($description) {
			$this->description = strip_tags(trim($description));
		}

		function get_data() {
			return strip_tags(trim($this->data));
		}

		function set_data($data) {
			$this->data = strip_tags(trim($data));
		}

		function get_time() {
			return $this->time;
		}
		
		function get_format_time($format = 'd.m.Y H:i:s') {
			return date($format, date_sql_to_timestamp($this->get_time()));
		}

		function set_time($time) {
			$this->time = $time;
		}

		function set_from_array($media) {
			if (isset($media['id']))
				$this->set_id($media['id']);
			if (isset($media['name']))
				$this->set_name($media['name']);
			if (isset($media['description']))
				$this->set_description($media['description']);
			if (isset($media['data']))
				$this->set_data($media['data']);
			if (isset($media['time']))
				$this->set_time($media['time']);
		}

		function  load($id) {
			$Media = selo('media', array('id' => $id));
			$this->set_from_array($Media);
		}

		function add() {
			ins('media', array(
				'name' => $this->get_name(),
				'description' => $this->get_description(),
				'data' => $this->get_data()
			));
			$this->load(lastID());
		}

		function update() {
			upd('media', array(
				'name' => $this->get_name(),
				'description' => $this->get_description(),
				'data' => $this->get_data()
			), array('id' => $this->get_id()));
			$this->load($this->get_id());
		}

		function delete() {
			del('media', array('id' => $this->get_id()));
		}

		static function get_media($where ='', $order = '') {
			$MediaElement = selo('media', $where, $order);
			if (!$MediaElement['id']) 
				return false;
			$media = new Media();
			$media->set_from_array($MediaElement);
			return $media;
		}

		static function get_medias($where ='', $order = '', $limit = '') {
			$MediasArray = sel('media', $where, $order, $limit);
			$Medias = array();
			if (is_array($MediasArray)) {
				foreach ($MediasArray as $MediaElement) {
					$Media = new Media();
					$Media->set_from_array($MediaElement);
					array_push($Medias, $Media);
				}
			}
			return $Medias;
		}
	}
?>