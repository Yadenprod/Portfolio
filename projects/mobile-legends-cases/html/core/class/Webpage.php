<?php
	class Webpage {
		protected $title = '';
		protected $title_page = '';
		protected $meta_des = '';
		protected $meta_key = '';
		protected $content = '';
		protected $tpl = '';
		protected $folder = '';
		protected $namepage = '';
		protected $url = '';
		protected $time_add = '';
		protected $time_edit = '';
		protected $menu = array();
		protected $css = array();
		protected $scripts = array();
		protected $jscripts = array();
		protected $meta = array();
		protected $link = array();
		protected $data = array();
		protected $breadcrumbs = array();
		protected $render_enable = true;
		protected $render_filters = array();
		protected $output = null;
		
		function __construct($namepage = false) {
			$this->folder = current_template_folder();
			$this->load($namepage);
		}
		
		function get_title() {
			return $this->title;
		}
		
		function set_title($title) {
			$this->title = strip_tags(trim($title));
		}
		
		function get_title_page() {
			return $this->title_page;
		}
		
		function set_title_page($title_page) {
			$this->title_page =  strip_tags(trim($title_page));
		}
		
		function get_meta_des() {
			return $this->meta_des;
		}
		
		function set_meta_des($meta_des) {
			$this->meta_des =  strip_tags(trim($meta_des));
		}
		
		function get_meta_key() {
			return $this->meta_key;
		}
		
		function set_meta_key($meta_key) {
			$this->meta_key =  strip_tags(trim($meta_key));
		}
		
		function get_tpl() {
			if ($this->tpl != '')
				return $this->tpl;
			else
				return 'page.php';
		}
		
		function set_tpl($tpl) {
			if (strpos($tpl, '.php') === false)
				$tpl .= '.php';
			$this->tpl = strip_tags(trim($tpl));
		}
		
		function get_folder() {
			return strpos($this->folder, '/') !== false? $this->folder : $this->folder.'/';
		}
		
		function set_folder($folder) {
			$this->folder = strip_tags(trim($folder));
		}
		
		function get_content() {
			return $this->content;
		}
		
		function set_content($content) {
			$this->content = trim($content);
		}
		
		function get_namepage() {
			return $this->namepage;
		}
		
		function set_namepage($namepage) {
			$this->namepage = strip_tags(trim($namepage));
		}
		
		function get_url() {
			return $this->url;
		}
		
		function set_url($url) {
			$this->url = strip_tags(trim($url));
		}
		
		function get_time_add() {
			return $this->time_add;
		}
		
		function get_format_time_add($format = 'd.m.Y H:i:s') {
			return date($format, date_sql_to_timestamp($this->get_time_add()));
		}

		function set_time_add($time_add) {
			$this->time_add = $time_add;
		}

		function get_time_edit() {
			return $this->time_edit;
		}
		
		function get_format_time_edit($format = 'd.m.Y H:i:s') {
			return date($format, date_sql_to_timestamp($this->get_time_edit()));
		}

		function set_time_edit($time_edit) {
			$this->time_edit = $time_edit;
		}

		function set_menu($key, $menu) { 
			$this->menu[$key] = $menu;
		}

		function add_menu($key, $menu) {
			if (!isset($this->menu[$key]))
				$this->menu[$key] = array();
			array_push($this->menu[$key], $menu);
		}

		function get_menu($key = false) {
			if ($key) return $this->menu[$key];
			return $this->menu;
		}
		
		function add_script($src, $pos = 10, $place = 'header', $options = array()) {
			$this->scripts[] = array('src' => $src, 'pos' => $pos, 'place' => $place, 'options' => $options);
		}

		function get_scripts() {
			return $this->scripts;
		}
		
		function add_jscript($script, $pos = 10, $place = 'footer') {
			$this->jscripts[] = array('script' => $script, 'pos' => $pos, 'place' => $place);
		}

		function get_jscripts() {
			return $this->jscripts;
		}
		
		function add_css($src, $pos = 10, $place = 'header', $options = array()) {
			$this->css[] = array('src' => $src, 'pos' => $pos, 'place' => $place, 'options' => $options);
		}

		function get_css() {
			return $this->css;
		}
		
		function add_meta($options = array(), $pos = 10) {
			$this->meta[] = array('options' => $options, 'pos' => $pos);
		}

		function get_meta() {
			return $this->meta;
		}
		
		function add_link($src, $options = array(), $pos = 10) {
			$this->link[] = array('src' => $src, 'options' => $options, 'pos' => $pos);
		}

		function get_link() {
			return $this->link;
		}
		
		function add_data($key, $value) {
			$this->data[$key] = $value;
		}
		
		function get_data($key = false) {
			if ($key) {
				if (!isset($this->data[$key])) {
					return false;
				}
				return $this->data[$key];
			}
			return $this->data;
		}
		
		function add_breadcrumb($name, $url, $icon = '') {
			$this->breadcrumbs[] = array('name' => $name, 'url' => $url, 'icon' => $icon);
		}

		function get_breadcrumbs() {
			return $this->breadcrumbs;
		}

		function get_render_filters() {
			if (!is_array($this->render_filters))
				return array();
			return $this->render_filters;
		}

		function set_render_filters($render_filters) {
			$this->render_filters = $render_filters;
		}

		function add_render_filter($filter) {
			array_push($this->render_filters, $filter);
		}

		function remove_render_filter($filter) {
			foreach ($this->get_render_filters() as $key => $render_filter) {
				if ($render_filter == $filter) {
					unset($this->render_filters[$key]);
				}
			}
		}

		function get_output() {
			return $this->output;
		}

		function set_output($output) {
			$this->output = $output;
		}

		function set_from_array($webpage) {
			if (isset($webpage['tpl']))
				$this->set_tpl($webpage['tpl']);
			if (isset($webpage['title']))
				$this->set_title($webpage['title']);
			if (isset($webpage['title_page']))
				$this->set_title_page($webpage['title_page']);
			if (isset($webpage['meta_des']))
				$this->set_meta_des($webpage['meta_des']);
			if (isset($webpage['meta_key']))
				$this->set_meta_key($webpage['meta_key']);
			if (isset($webpage['content']))
				$this->set_content($webpage['content']);
			if (isset($webpage['namepage']))
				$this->set_namepage($webpage['namepage']);
			if (isset($webpage['url']))
				$this->set_url($webpage['url']);
			if (isset($webpage['time_add']))
				$this->set_time_add($webpage['time_add']);
			if (isset($webpage['time_edit']))
				$this->set_time_edit($webpage['time_edit']);
		}
		
		function load($namepage = false) {
			if ($namepage) {
				$webpage = selo('webpage', array('namepage' => $namepage)); 
			} else {
				$webpage = selo('webpage', array('url' => uri()), array('namepage' => 'DESC')); 
			}
			if ($webpage) {
				$this->set_from_array($webpage);
			}
		}

		function add() {
			ins('webpage', array(
				'namepage' => $this->get_namepage(),
				'title' => $this->get_title(),
				'title_page' => $this->get_title_page(),
				'meta_des' => $this->get_meta_des(),
				'meta_key' => $this->get_meta_key(),
				'content' => $this->get_content(),
				'tpl' => $this->get_tpl(),
				'url' => $this->get_url()
			));
			$this->load($this->get_namepage());
		}
		
		function update($namepage = false) {
			if (!$namepage)
				$namepage = $this->get_namepage();
			upd('webpage', array(
				'namepage' => $this->get_namepage(),
				'title' => $this->get_title(),
				'title_page' => $this->get_title_page(),
				'meta_des' => $this->get_meta_des(),
				'meta_key' => $this->get_meta_key(),
				'content' => $this->get_content(),
				'tpl' => $this->get_tpl(),
				'url' => $this->get_url()
			), array('namepage' => $namepage));
			$this->load($this->get_namepage());
		}
		
		function delete() {
			del('webpage', array('namepage' => $this->namepage));
		}

		static function get_webpage($where = false, $order = false) {
			$WebpageElement = selo('webpage', $where, $order);
			if (!$WebpageElement['namepage']) 
				return false;
			$webpage = new Webpage();
			$webpage->set_from_array($WebpageElement);
			return $webpage;
		}

		static function get_webpages($where = false, $order = false, $limit = false) {
			$WebpagesArray = sel('webpage', $where, $order, $limit);
			$Webpages = array();
			if (is_array($WebpagesArray)) {
				foreach ($WebpagesArray as $WebpageElement) {
					$webpage = new Webpage();
					$webpage->set_from_array($WebpageElement);
					array_push($Webpages, $webpage);
				}
			}
			return $Webpages;
		}
		
		function render($tpl = false, $folder = false) {
			if ($this->render_enable) {
				if (!$tpl) $tpl = $this->tpl;
				if (!$folder) $folder = $this->folder;
				if ($tpl != '') {
					if (file_exists($folder.$tpl)) {
						foreach ($this->get_data() as $key => $value) {
							$$key = $value;
						}
						include $folder.$tpl;
						$this->set_output(filter(ob_get_contents(), $this->get_render_filters()));
						ob_clean();
						echo $this->get_output();
					} else {
						return false;
					}
				} else {
					wserror(404);
				}
			}
			return true;
		}

		function disable_render() {
			$this->render_enable = false;
		}
		
		function enable_render() {
			$this->render_enable = true;
		}
	}
?>