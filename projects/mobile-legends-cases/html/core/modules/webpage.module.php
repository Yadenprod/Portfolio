<?php
	function set_title($title = '') {
		wp()->set_title($title);
	}
	
	function get_title() {
		return wp()->get_title();
	}
	
	function add_title($title = '') {
		set_title(get_title().$title);
	}
	
	function set_title_page($title_page = '') {
		wp()->set_title_page($title_page);
	}
	
	function get_title_page() {
		return wp()->get_title_page();
	}
	
	function add_title_page($title_page = '') {
		set_title_page(get_title_page().$title_page);
	}
	
	function set_meta_des($meta_des = '') {
		wp()->set_meta_des($meta_des);
	}
	
	function get_meta_des() {
		return wp()->get_meta_des();
	}
	
	function add_meta_des($meta_des = '') {
		set_meta_des(get_meta_des().$meta_des);
	}
	
	function set_meta_key($meta_key = '') {
		wp()->set_meta_key($meta_key);
	}
	
	function get_meta_key() {
		return wp()->get_meta_key();
	}
	
	function add_meta_key($meta_key = '') {
		set_meta_key(get_meta_key().$meta_key);
	}
	
	function set_content($content = '') {
		wp()->set_content($content);
	}
	
	function get_content($namepage = false) {
		if (!$namepage) {
			return wp()->get_content();
		}
		$wp = selo('webpage', array('namepage' => $namepage)); 
		if ($wp['namepage'] != '') {
			return $wp['content'];
		} else {
			return wp()->get_content();
		}
	}
	
	function the_content($namepage = false) {
		echo get_content($namepage);
	}
	
	function add_content($content = '') {
		set_content(get_content().$content);
	}
	
	function set_tpl($tpl = '') {
		wp()->set_tpl($tpl);
	}
	
	function get_tpl() {
		return wp()->get_tpl();
	}
	
	function get_page_tpl() {
		return str_replace('.php', '', get_tpl());
	}
	
	function get_namepage() {
		return wp()->get_namepage();
	}
	
	function get_url() {
		return wp()->get_url();
	}
	
	function set_url($url) {
		return wp()->set_url($url);
	}
	
	function disable_render() {
		wp()->disable_render();
	}
	
	function enable_render() {
		wp()->enable_render();
	}

	function add_render_filter($filter) {
		ws()->get_webpage()->add_render_filter($filter);
	}

	function remove_render_filter($filter) {
		ws()->get_webpage()->remove_render_filter($filter);
	}
?>