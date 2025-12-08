<?php
	function get_media($id = false) {
		return Media::get_Medias(($id? array('id' => $id) : false), array('id' => 'DESC'));
	}
	
	function upload_media($tag, $description, $sizes = array('735x300', '545x200', '400x400', '150x100', '30x30'), $convert_to_jpg = false) {
		$media = new Media();
		$filename = upload($_FILES[$tag]);
		if ($convert_to_jpg) {
			$new_path = image_convert_to_jpg('uploads/'.$filename);
			$new_path = explode('/', $new_path);
			$filename = $new_path[count($new_path) - 1];
		}
		if (!$filename) {
			return false;
		}
		$media->set_name($filename);
		$media->set_description($description);
		$data = array();
		if ($sizes && is_array($sizes)) {
			foreach($sizes as $size) {
				if (!in_array($size, $data)) {
					$size = explode('x', $size);
					if (is_array($size) && count($size) == 2) {
						$result = image_resize('uploads/'.$filename, $size[0], $size[1], true, $convert_to_jpg);
						if ($result) {
							array_push($data, $size[0].'x'.$size[1]);
						}
					}
				}
			}
		}
		if ($data) {
			usort($data, 'media_sort');
			$media->set_data(implode(';', $data));
		}
		$media->add_media();
		return $media;
	}
	
	function media_sort($a, $b) {
		$a = explode('x', $a); 
		$b = explode('x', $b); 
		//return -(intval($a[0]) <=> intval($b[0]));
		return intval($a[0]) >= intval($b[0]);
	}
?>