<?php 
	function get_image($path) {
		$path_part = explode('.', $path);
		$extension = end($path_part);
		$image = false;
		if (in_array($extension, array('jpg', 'jpeg'))) {
			$image = imagecreatefromjpeg($path);
		} else if (in_array($extension, array('png'))) {
			$image = imagecreatefrompng($path);
		} else if (in_array($extension, array('gif'))) {
			$image = imagecreatefromgif($path);
		}
		return $image;
	}
	
	function image_resize($path, $width, $height = false, $save = false, $convert_to_jpg = false) {
		$path_part = explode('.', $path);
		$extension = end($path_part);
		$image = get_image($path);
		if (!$image) {
			return false;
		}
		if (!$height) {
			$result = imagescale($image, $width);
		} else {
			$swidth = imagesx($image);
			$sheight = imagesy($image);
			$srate = $swidth / $sheight;
			$nrate = $width / $height;
			if ($srate >= $nrate) {
				$rate =  $height / $sheight;
				$result = imagescale($image, $swidth * $rate, $height);
				$result = imagecrop($result, array('x' => ($swidth * $rate - $width) / 2, 'y' => 0, 'width' => $width, 'height' => $height));
			} else {
				$rate =  $width / $swidth;
				$result = imagescale($image, $width, $sheight * $rate);
				$result = imagecrop($result, array('x' => 0, 'y' => ($sheight * $rate - $height) / 2, 'width' => $width, 'height' => $height));
			}
		}
		if (!$result) {
			return false;
		}
		if ($save) {
			$nwidth = imagesx($result);
			$nheight = imagesy($result);
			$path_part[count($path_part) - 2] .= '-'.$nwidth.'x'.$nheight;
			image_save($result, implode('.', $path_part), 100, $convert_to_jpg);
			imagedestroy($result);
			return true;
		}
		imagedestroy($image);
		return $result;
	}
	
	function image_convert_to_jpg($path, $quality = 100) {
		$image = get_image($path);
		$new_path = image_save($image, $path, $quality, true);
		return $new_path;
	}
	
	function image_save($image, $save_path, $quality = 100, $convert_to_jpg = false) {
		$path_part = explode('.', $save_path);
		$extension = end($path_part);
		if ($convert_to_jpg) {
			if (in_array($extension, array('jpg', 'jpeg'))) {
				imagejpeg($image, $save_path, $quality);
			} else {
				$path_part = explode('.', $save_path);
				$path_part[count($path_part) - 1] = 'jpg';
				$save_path = implode('.', $path_part);
				imagejpeg($image, $save_path, $quality);
			}
		} else if (in_array($extension, array('jpg', 'jpeg'))) {
			imagejpeg($image, $save_path, $quality);
		} else if (in_array($extension, array('png'))) {
			imagepng($image, $save_path, intval(($quality - 1) / 10));
		} else if (in_array($extension, array('gif'))) {
			imagegif($image, $save_path);
		}
		return $save_path;
	}
?>