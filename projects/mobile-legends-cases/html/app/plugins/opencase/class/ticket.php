<?php
	class ticket
	{
		var $id = '';
		var $theme = '';
		var $game_id = '';
		var $user_id = '';
		var $status = '';
		var $assessment = '';

		function __construct($id = '')
		{
			if ($id != '')
			{
				$this->load_ticket(db()->nomysqlinj($id));
			}
		}

		function get_id()
		{
			return $this->id;
		}

		function set_id($id)
		{
			$this->id = $id;
		}

		function get_theme()
		{
			return $this->theme;
		}

		function set_theme($theme)
		{
			$this->theme = strip_tags(db()->nomysqlinj($theme));
		}

		function get_game_id()
		{
			return $this->game_id;
		}

		function set_game_id($game_id)
		{
			$this->game_id = intval($game_id);
		}

		function get_user_id()
		{
			return $this->user_id;
		}
		
		function get_user_class()
		{
			$user = new user($this->user_id);
			return $user;
		}

		function set_user_id($user_id)
		{
			$this->user_id = $user_id;
		}

		function get_status()
		{
			return $this->status;
		}

		function set_status($status)
		{
			$this->status = $status;
		}
		
		function get_admin_status_text() {
			if ($this->status == 0) {
				return 'Новая';
			} else if ($this->status == 1) {
				return 'Просмотренна';
			} else if ($this->status == 2) {
				return 'Активная';
			} else if ($this->status == 3) {
				return 'Отвеченно';
			} else if ($this->status == 4) {
				return 'Новый ответ';
			} else if ($this->status == 5) {
				return 'Решено';
			} else if ($this->status == 6) {
				return 'Не решено';
			} else if ($this->status == 7) {
				return 'Требуеться помошь администратора';
			} else if ($this->status == 8) {
				return 'Просмотренна пользователем';
			} 
		}
		
		function get_user_status_text() {
			if ($this->status == 0) {
				return 'Подан';
			} else if ($this->status == 1) {
				return 'В обработке';
			} else if ($this->status == 2) {
				return 'Активный';
			} else if ($this->status == 3) {
				return 'Новый ответ';
			} else if ($this->status == 4) {
				return 'Активный';
			} else if ($this->status == 5) {
				return 'Закрытый';
			} else if ($this->status == 6) {
				return 'Закрытый';
			} else if ($this->status == 7) {
				return 'Активный';
			} else if ($this->status == 8) {
				return 'Активный';
			} 
		}

		function get_assessment()
		{
			return $this->assessment;
		}

		function set_assessment($assessment)
		{
			$this->assessment = $assessment;
		}

		function set_parametrs( $id, $theme, $game_id, $user_id, $status, $assessment)
		{
			$this->set_id($id);
			$this->set_theme($theme);
			$this->set_game_id($game_id);
			$this->set_user_id($user_id);
			$this->set_status($status);
			$this->set_assessment($assessment);
		}

		function set_parametrs_from_request()
		{
			if ($_REQUEST['id'] != '')
				$this->set_id($_REQUEST['id']);
			if ($_REQUEST['theme'] != '')
				$this->set_theme($_REQUEST['theme']);
			if ($_REQUEST['game_id'] != '')
				$this->set_game_id($_REQUEST['game_id']);
			if ($_REQUEST['user_id'] != '')
				$this->set_user_id($_REQUEST['user_id']);
			if ($_REQUEST['status'] != '')
				$this->set_status($_REQUEST['status']);
			if ($_REQUEST['assessment'] != '')
				$this->set_assessment($_REQUEST['assessment']);
		}

		function clear_parametrs()
		{
			$this->set_id('');
			$this->set_theme('');
			$this->set_game_id('');
			$this->set_user_id('');
			$this->set_status('');
			$this->set_assessment('');
		}

		function  load_ticket($id)
		{
			$ticket = db()->query_once('select * from ticket where id = "'.$id.'"');
			$this->set_parametrs( $ticket['id'], $ticket['theme'], $ticket['game_id'], $ticket['user_id'], $ticket['status'], $ticket['assessment']);
		}

		function add_ticket()
		{
			db()->query_once('insert into ticket( theme, game_id, user_id, status, assessment) values ( "'.$this->get_theme().'", "'.$this->get_game_id().'", "'.$this->get_user_id().'", "'.$this->get_status().'", "'.$this->get_assessment().'")');
		}

		function update_ticket()
		{
			db()->query_once('update ticket set theme = "'.$this->get_theme().'", game_id = "'.$this->get_game_id().'", user_id = "'.$this->get_user_id().'", status = "'.$this->get_status().'", assessment = "'.$this->get_assessment().'" where id = "'.$this->get_id().'"');
		}

		function delete_ticket()
		{
			db()->query_once('delete from ticket where id = "'.$this->get_id().'"');
		}
		
		function get_tickets($where ='', $order = '', $limit = '') {
			$sql = 'select id from ticket';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			$ticketsArray = db()->query($sql);
			$tickets = array();
			if (is_array($ticketsArray)) {
				foreach ($ticketsArray as $ticketElement) {
					$ticket = new ticket($ticketElement['id']);
					array_push($tickets, $ticket);
				}
			}
			return $tickets;
		}
		
		function get_tickets_with_message($where ='', $order = '', $limit = '') {
			$sql = 'select id from ticket inner join (select ticket_id, max(time_add) as time_add from ticket_message GROUP by ticket_id) as ticket_message on ticket.id = ticket_message.ticket_id';
			if ($where != '')
				$sql .= ' where '.$where;
			if ($order != '')
				$sql .= ' order by '.$order;
			if ($limit != '')
				$sql .= ' limit '.$limit;
			//var_dump($sql);
			$ticketsArray = db()->query($sql);
			$tickets = array();
			if (is_array($ticketsArray)) {
				foreach ($ticketsArray as $ticketElement) {
					$ticket = new ticket($ticketElement['id']);
					array_push($tickets, $ticket);
				}
			}
			return $tickets;
		}
		
		function get_last_message() {
			$message = db()->query_once('select id from ticket_message where ticket_id = "'.$this->get_id().'" ORDER BY time_add DESC LIMIT 1');
			$message = new ticket_message($message['id']);
			return $message;
		}
		
		function get_first_message() {
			$message = db()->query_once('select id from ticket_message where ticket_id = "'.$this->get_id().'" ORDER BY time_add ASC LIMIT 1');
			$message = new ticket_message($message['id']);
			return $message;
		}
		
		function get_messages() {
			$messages = db()->query('select id from ticket_message where ticket_id = "'.$this->get_id().'" ORDER BY time_add ASC');
			$result_messages = array();
			foreach ($messages as $message) {
				$result_messages[] = new ticket_message($message['id']);
			}
			return $result_messages;
		}
	}
?>