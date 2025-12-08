<?php
	class item {
		var $id = '';
		var $name = '';
		var $image = '';
		var $quality = 0;
		var $price = 0;
		
		var $quality_array = array('Базового класса', 'Ширпотреб', 'Промышленное качество', 'Армейское качество', 'Запрещенное', 'Засекреченное', 'Тайное', 'Высшего класса', 'Примечательного типа', 'Экзотичного вида', 'Контрабандное', 'Экстраординарного типа', 'Нож');
		var $quality_array_en = array('Base Grade', 'Consumer Grade', 'Industrial Grade', 'Mil-Spec Grade', 'Restricted', 'Classified', 'Covert', 'High Grade', 'Remarkable', 'Exotic', 'Contraband', 'Extraordinary', 'Knife');
		var $quality_css = array('common', 'common', 'industrial', 'milspec', 'restricted', 'classified', 'covert', 'milspec', 'restricted', 'classified', 'contraband', 'covert', 'rare');
		var $quality_colors = array('176, 195, 217', '176, 195, 217', '94, 152, 217', '75, 105, 255', '136, 71, 255', '211, 44, 230', '235, 75, 75', '75, 105, 255', '136, 71, 255', '211, 44, 230', '228, 174, 57', '235, 75, 75', '246, 228, 70');
		public static $price_keys_array = [0 => 'avg', 1 => 'steam', 2 => 'bitskins', 3 => 'csgobackpack', 4 => 'market'];
		
		function __construct($id = '') {
			if ($id != '') {
				$this->load_item(db()->nomysqlinj($id));
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

		function get_image() {
			return trim($this->image);
		}
		
		function get_steam_image($width = false, $height = false) {
			return 'https://i.ibb.co/'.$this->get_image().($width && $height? '/'.$width.'x'.$height : '');
		}

		function set_image($image) {
			$this->image = $image;
		}

		function get_quality() {
			return $this->quality;
		}
		
		function get_text_quality() {
			return $this->quality_array[$this->get_quality()];
		}
		
		function get_quality_array() {
			return $this->quality_array;
		}
		
		function get_text_quality_en() {
			return isset($this->quality_array_en[$this->get_quality()])? $this->quality_array_en[$this->get_quality()] : '';
		}
		
		function get_css_quality_class() {
			return isset($this->quality_css[$this->get_quality()])? $this->quality_css[$this->get_quality()] : '';
		}
		
		function get_quality_array_en() {
			return $this->quality_array_en;
		}
		
		function get_quality_color() {
			return $this->quality_colors[$this->get_quality()];
		}
		
		function get_quality_colors() {
			return $this->quality_colors;
		}

		function set_quality($quality) {
			if (is_int(stripos($this->get_name(), '★')))
				$quality = 12;
			$this->quality = $quality;
		}
		
		function get_count_on_bot() {
			$count = db()->query_once('select count(id) from opencase_invitems where name = "'.$this->get_name().'" and status = 0');
			return $count['count(id)'];
		}
		
		function get_price() {
			return (float)$this->price;
		}

		function set_price($price) {
			$this->price = (float)$price;
		}

		function set_parametrs( $id, $name, $image, $quality, $price) { 
 			$this->set_id($id);
			$this->set_name($name);
			$this->set_image($image);
			$this->set_quality($quality);
			$this->set_price($price);
		}

		function set_parametrs_from_request() {
			if ($_REQUEST['name'] != '')
				$this->set_name($_REQUEST['name']);
			if ($_REQUEST['image'] != '')
				$this->set_image($_REQUEST['image']);
			if ($_REQUEST['quality'] != '')
				$this->set_quality($_REQUEST['quality']);
			if ($_REQUEST['price'] != '')
				$this->set_price($_REQUEST['price']);
		}

		function clear_parametrs() {
			$this->set_id('');
			$this->set_name('');
			$this->set_image('');
			$this->set_quality('');
			$this->set_price(0);
		}

		function  load_item($id) {
			$cache = ch()->get('item'.$id);
			if (!$cache) {
				$item = db()->query_once('select * from opencase_items where id = "'.$id.'"');
				$this->set_parametrs( $item['id'], $item['name'], $item['image'], $item['quality'], $item['price']);
				if ($this->get_id() != '')
					ch()->set('item'.$id, $this);
			} else {
				$this->set_parametrs( $cache->get_id(), $cache->get_name(), $cache->get_image(), $cache->get_quality(), $cache->get_price());
			}
		}

		function add_item() {
			db()->query_once('insert into opencase_items( `name`, `image`, `quality`, `price`) values ( "'.$this->get_name().'", "'.$this->get_image().'", "'.$this->get_quality().'", "'.$this->get_price().'")');
		}

		function update_item() {
			db()->query_once('update opencase_items set `name` = "'.$this->get_name().'", `image` = "'.$this->get_image().'", `quality` = "'.$this->get_quality().'", `price` = "'.$this->get_price().'" where id = "'.$this->get_id().'"');
			if ($this->get_id() != '')
				ch()->set('item'.$this->id, $this);
		}

		function delete_item() {
			db()->query_once('delete from opencase_items where id = "'.$this->get_id().'"');
			ch()->delete('item'.$this->id);
		}

		function get_items($where ='', $order = '', $limit = '') {
			$sql = 'select id from opencase_items';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$itemsArray = db()->query($sql);
			$items = array();
			if (is_array($itemsArray)) {
				foreach ($itemsArray as $itemElement) {
					$item = new item($itemElement['id']);
					array_push($items, $item);
				}
			}
			return $items;
		}
		
		function get_name_no_stattrack() {
			return trim(str_replace('StatTrak™', '', $this->get_name()));
		}
		
		function get_name_no_stattrack_no_quality() {
			return trim(str_replace(['(Factory New)', '(Minimal Wear)', '(Field-Tested)', '(Well-Worn)', '(Battle-Scarred)'], '', $this->get_name_no_stattrack()));
		}
		
		function get_clear_name_key() {
			return str_replace(' ', '', $this->get_name_no_stattrack_no_quality());
		}

		function update_items_list(&$error = '') {
			set_time_limit(300);
			$data = file_get_contents('https://steampricer.com/api/items/list/full/' . get_setval('opencase_gameid') . '/');
			if (!$data) {
				$error = 'Ошибка загрузки данных';
				return false;
			}
			$data = json_decode($data, true);
			if (!$data['success']) {
				$error = 'Ошибка загрузки предметов';
				return false;
			}
			$items = $data['list'];
			$values_parts = [];
			$index = 0;
			$j = 0;
			$priceSource = self::$price_keys_array[get_setval('opencase_price_parser_key')];
			foreach ($items as $key => $item) {
				$image = explode('/', $item['image']);
				$image = isset($image[count($image) - 2]) ? $image[count($image) - 2] : false;
				if ($image) {
					if (!isset($values_parts[$index])) {
						$values_parts[$index] = [];
					}
					if (empty($item['quality'])) {
						$item['quality'] = 0;
					}
					foreach ($item['prices'] as $priceKey => $price) {
						if ($price <= 0) {
							unset($item['prices'][$priceKey]);
						}
					}
					unset($item['prices']['steamall']);
					if (empty($item['prices'])) {
						continue;
					}
					if ($priceSource == 'avg' || !isset($item['prices'][$priceSource]) || $item['prices'][$priceSource] <= 0) {
						unset($item['prices']['market']);
						if (empty($item['prices'])) {
						    continue;
					    }
						$totalPrice = get_weighted_arithmetic_mean($item['prices']);
						if (isset($item['prices']['steam']) && $totalPrice > $item['prices']['steam']) {
							$totalPrice = $item['prices']['steam'];
						}
					} else {
						$totalPrice = $item['prices'][$priceSource];
					}
					$totalPrice = ceil($totalPrice);
					if ($totalPrice <= 0) {
						continue;
					}
					array_push($values_parts[$index], '("' . db()->nosqlinj($key) . '", ' . $item['appid'] . ', "' . $image . '", ' . $totalPrice . ', ' . $item['quality'] . ')');
			}
				$j++;
				if ($j % 1000 == 0) {
					$index++;
				}
			}
			if (count($values_parts) == 0) {
				$error = 'Ошибка вставки предметов';
				return false;
			}
			foreach ($values_parts as $key => $values_part) {
				db()->query_once('INSERT INTO `opencase_items` (`name`, `appid`, `image`, `price`, `quality`) VALUES '
						. implode(', ', $values_part)
						. ' ON DUPLICATE KEY UPDATE appid = VALUES(appid), image = VALUES(image), price = VALUES(price), quality = VALUES(quality)'
						. ';');
			}
			ch()->flush();
			return true;
		}

}