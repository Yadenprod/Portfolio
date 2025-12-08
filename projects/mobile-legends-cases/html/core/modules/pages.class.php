<?php
	class Pages {
		var $first_url = '/';
		var $format_url = '/index/pages/{p}/';
		var $format_text = '{p}';
		var $format_arrow_right = '»';
		var $format_arrow_left = '«';
		var $format_dop_param = '';
		var $pre_page_text = '';
		var $num_object = '';
		var $object_in_page = '10';
		var $pages_num = '';
		var $curent_page = '1';
		
		function __construct() {

		}
		
		function get_first_url() {
			return $this->first_url;
		}
		
		function set_first_url($first_url) {
			$this->first_url = $first_url;
		}
		
		function get_format_url() {
			return $this->format_url;
		}
		
		function set_format_url($format_url) {
			$this->format_url = $format_url;
		}
		
		function get_format_text() {
			return $this->format_text;
		}
		
		function set_format_text($format_text) {
			$this->format_text = $format_text;
		}
		
		function get_format_arrow_right() {
			return $this->format_arrow_right;
		}
		
		function set_format_arrow_right($format_arrow_right) {
			$this->format_arrow_right = $format_arrow_right;
		}
		
		function get_format_arrow_left() {
			return $this->format_arrow_left;
		}
		
		function set_format_arrow_left($format_arrow_left) {
			$this->format_arrow_left = $format_arrow_left;
		}
		
		function get_pre_page_text() {
			return $this->pre_page_text;
		}
		
		function set_pre_page_text($pre_page_text) {
			$this->pre_page_text = $pre_page_text;
		}
		
		function get_num_object() {
			return $this->num_object;
		}
		
		function set_num_object($num_object) {
			$this->num_object = $num_object;
		}
		
		function get_object_in_page() {
			return $this->object_in_page;
		}
		
		function set_object_in_page($object_in_page) {
			$this->object_in_page = $object_in_page;
		}
		
		function get_pages_num () {
			if  ($this->pages_num == '')	
				$this->calculate();
			return $this->pages_num ;
		}
		
		function set_pages_num ($pages_num ) {
			$this->pages_num = $pages_num ;
		}
		
		function get_curent_page() {
			return $this->curent_page;
		}
		
		function set_curent_page($curent_page) {
			if ($curent_page == '')
				$curent_page = 1;
			$this->curent_page = $curent_page;
		}
		
		function get_format_dop_param() {
			return $this->format_dop_param;
		}
		
		function set_format_dop_param($format_dop_param) {
			$this->format_dop_param = $format_dop_param;
		}
		
		function set_parametrs($first_url, $format_url, $format_text, $format_arrow_right, $format_arrow_left, $pre_page_text, $num_object, $object_in_page, $pages_num, $curent_page, $format_dop_param) {
			$this->set_first_url(first_url);
			$this->set_format_url($format_url);
			$this->set_format_text(format_text);
			$this->set_format_arrow_right($format_arrow_right);
			$this->set_format_arrow_left($format_arrow_left);
			$this->set_pre_page_text($pre_page_text);
			$this->set_num_object($num_object);
			$this->set_object_in_page($object_in_page);
			$this->set_pages_num($pages_num);
			$this->set_curent_page($curent_page);
			$this->format_dop_param($format_dop_param);
		}
		
		function clear_parametrs() {
			$this->set_first_url('');
			$this->set_format_url('');
			$this->set_format_text('');
			$this->set_format_arrow_right('');
			$this->set_format_arrow_left('');
			$this->set_pre_page_text('');
			$this->set_num_object('');
			$this->set_object_in_page('');
			$this->set_pages_num ('');
			$this->set_curent_page('');
			$this->format_dop_param('');
		}
		
		function calculate() {
			if ($this->get_num_object() == 0)
				$this->set_num_object(1);
			$pages = ($this->get_num_object()/$this->get_object_in_page());
			if ($pages != (integer)$pages) $pages = (integer)$pages +1;
			$this->set_pages_num($pages);
			return $this->get_pages_num();
		}
		
		function get_html_pages() {
			$this->calculate();
			$pre_page = $this->curent_page - 1;
			$next_page = $this->curent_page + 1;
			$pre_page_url = '';
			if ($this->get_format_dop_param() != '')
					$pre_page_url = $this->get_first_url().$this->get_format_dop_param();
			if ($pre_page != 1)
			{
				if ($this->get_format_dop_param() != '')
					$pre_page_url .= ''.str_replace('{p}', $pre_page, $this->get_format_url());
				else 
					$pre_page_url .= ''.str_replace('{p}', $pre_page, $this->get_format_url());
			}
			else 
			{
				if ($this->get_format_dop_param() == '')
					$pre_page_url .= $this->get_first_url();
			}
			$pre_page_html = '<li><a href = "'.$pre_page_url.'">'.$this->get_format_arrow_left().'</a></li>';
			if ($this->get_format_dop_param() != '')
				$next_page_url = ''.$this->get_format_dop_param().'&'.str_replace('{p}', $next_page, $this->get_format_url());
			else 
				$next_page_url = ''.str_replace('{p}', $next_page, $this->get_format_url());
			$next_page_html = '<li><a href = "'.$next_page_url.'">'.$this->get_format_arrow_right().'</a></li>';	
			$pages_html = '';
			if ($this->get_pages_num() < 10) {
				for ($i = 1; $i <= 9 && $i <= $this->get_pages_num(); $i++)
				{
					$pages_html .= $this->get_page($i);
				}
			} else {
				for ($i = 1; $i <= 3 && $i <= $this->get_pages_num(); $i++)
				{
					$pages_html .= $this->get_page($i);
				}
				
				
				$minus = 1;
				$plus = 1;
				if (($this->get_curent_page() > 5 || $this->get_curent_page() < 3)) {
					$pages_html .= $this->get_page('...');
				} 
				
				if ($this->get_curent_page() <= 2 || $this->get_curent_page() >= $this->get_pages_num() - 1) {
					$half = (int)($this->get_pages_num() / 2);
				}  else {
					$half = $this->get_curent_page();
				}
				
				if ($this->get_curent_page() == 3) {
					$minus = -1;
					$plus = 3;
				}
				if ($this->get_curent_page() == 4) {
					$minus = 0;
					$plus = 2;
				}
				
				if ($this->get_curent_page() == $this->get_pages_num() - 2) {
					$minus = 3;
					$plus = -1;
				}
				if ($this->get_curent_page() == $this->get_pages_num() - 3) {
					$minus = 2;
					$plus = 0;
				}
				
				for ($i = $half - $minus; $i <= $half + $plus && $i <= $this->get_pages_num() && $i > 3; $i++)
				{
					$pages_html .= $this->get_page($i);
				}
				
				
				
				if ($this->get_curent_page() < $this->get_pages_num() - 4 || $this->get_curent_page() > $this->get_pages_num() - 2) {
					$pages_html .= $this->get_page('...');
				} 
				
				for ($i = $this->get_pages_num() - 2; $i <= $this->get_pages_num() && $i <= $this->get_pages_num(); $i++)
				{
					$pages_html .= $this->get_page($i);
				}
			}
			
			$result = $this->get_pre_page_text();
			if ($this->get_curent_page() > 1)
			{
				$result .= $pre_page_html; 
			}
			$result .= $pages_html;
			if ($this->get_curent_page() < $this->get_pages_num())
			{
				$result .= $next_page_html; 
			}
			return $result;
		}
		
		function get_page($page) {
			$page_html = '';
			if ($this->get_curent_page() != $page && gettype($page) != 'string') {
				if ($this->get_format_dop_param() != '') {
					if ($page == 1)
						$page_url = $this->get_first_url().$this->get_format_dop_param();
					else
						$page_url = ''.$this->get_format_dop_param().'&'.str_replace('{p}', $page, $this->get_format_url());
				} else {
					if ($page == 1)
						$page_url = $this->get_first_url();
					else
						$page_url = ''.str_replace('{p}', $page, $this->get_format_url());
				}
				$page_html = '<li><a href = "'.$page_url.'">'.str_replace('{p}', $page, $this->get_format_text()).'</a></li>' ;
			}
			else {
				$page_html = '<li><span>'.str_replace('{p}', $page, $this->get_format_text()).'</span></li>';
			}
			return $page_html;
		}
	}
?>