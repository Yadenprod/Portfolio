<?php
	function is_login() {
		return user()->is_login();
	}

	function add_user_field($key, $type, $default = null, $description = '') {
		$field = new user_field();
		$field->set_key($key);
		$field->set_type($type);
		$field->set_description($description);
		$field->set_default($default);
		$field->add_user_field();
		return $field;
	}

	function update_user_field($key, $type = false, $default = false, $description = false) {
		$field = user_field::get_user_field(array('key' => $key));
		if (!$field) return false;
		if ($type) $field->set_type($type);
		if ($description) $field->set_description($description);
		if ($default) $field->set_default($default);
		$field->update_user_field();
		return $field;
	}

	function delete_user_field($key) {
		$field = user_field::get_user_field(array('key' => $key));
		if (!$field) return false;
		$field->delete_user_field();
		return true;
	}
?>