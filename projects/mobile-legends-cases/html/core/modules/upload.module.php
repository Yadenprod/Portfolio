<?php 
	function upload_file($tag, $id = -1, $allowed = array('png', 'jpg', 'jpeg', 'gif'), $maxsize = 0) {
		if ($id == -1) {
			if ($_FILES[$tag]['name'] != '') {
				$path_part = explode('.',$_FILES[$tag]['name']);
				$extension = end($path_part);
				if (in_array($extension, $allowed)) {
					if ($maxsize == 0 || $_FILES[$tag]['size'] <= $maxsize * 1024) {
						$filename = md5(sha1($_FILES[$tag]['name'].date('d.m.Y H:i:s').rand())).'.'.strtolower($extension);
						if (!move_uploaded_file($_FILES[$tag]['tmp_name'], 'uploads/'.$filename)) {
							return false;
						}
						return $filename;
					} else {
						return false;
					}
				} else {
					return false;
				}
			} else {
				return false;
			}
		} else {
			if ($_FILES[$tag]['name'][$id] != '') {
				$path_part = explode('.',$_FILES[$tag]['name'][$id]);
				$extension = end($path_part);
				if (in_array($extension, $allowed)) {
					if ($maxsize == 0 || $_FILES[$tag]['size'][$id] <= $maxsize * 1024) {
						$filename = md5(sha1($_FILES[$tag]['name'][$id].date('d.m.Y H:i:s').rand())).'.'.strtolower($extension);
						if (!move_uploaded_file($_FILES[$tag]['tmp_name'][$id], 'uploads/'.$filename)) {
							return false;
						}
						return $filename;
					} else {;
						return false;
					}
				} else {
					return false;
				}
			} else {
				return false;
			}
		}
	}
	
	function upload($file, $allowed = array('png', 'jpg', 'jpeg', 'gif'), $maxsize = 0) {
		if ($file['name'] != '') {
			$path_part = explode('.', $file['name']);
			$extension = end($path_part);
			if (in_array($extension, $allowed)) {
				if ($maxsize == 0 || $file['size'] <= $maxsize * 1024) {
					$filename = md5(sha1($file['name'].date('d.m.Y H:i:s').rand())).'.'.strtolower($extension);
					if (!move_uploaded_file($file['tmp_name'], 'uploads/'.$filename)) {
						return false;
					}
					return $filename;
				} else {
					return false;
				}
			} else {
				return false;
			}
		} else {
			return false;
		}
	}
?>