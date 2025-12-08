<?php
	class ticket_message
	{
		var $id = '';
		var $ticket_id = '';
		var $text = '';
		var $attachment = '';
		var $time_add = '';
		var $from = '';

		function __construct($id = '')
		{
			if ($id != '')
			{
				$this->load_ticket_message(db()->nomysqlinj($id));
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

		function get_ticket_id()
		{
			return $this->ticket_id;
		}

		function set_ticket_id($ticket_id)
		{
			$this->ticket_id = $ticket_id;
		}

		function get_text()
		{
			return $this->text;
		}
		
		function get_short_text()
		{
			$textArr = explode('\\\n', str_replace('\\r', '', $this->text));
			$text = array_shift($textArr);
			return iconv('windows-1251', 'utf-8', substr(iconv('utf-8', 'windows-1251', $text), 0, 50)).'...';
		}

		function set_text($text)
		{
			$this->text = strip_tags(db()->nomysqlinj($text));
		}

		function get_attachment()
		{
			return $this->attachment;
		}
		
		function get_attachments() {
			if ($this->attachment != '')
				return explode(';', $this->attachment);
			else 
				return false;
		}

		function set_attachment($attachment)
		{
			$this->attachment = db()->nomysqlinj($attachment);
		}

		function get_time_add()
		{
			return $this->time_add;
		}
		
		function get_form_time_add($format = 'd.m.Y H:i:s')
		{
			$timestamp = datef($this->time_add);
			return date($format , $timestamp);
		}

		function set_time_add($time_add)
		{
			$this->time_add = $time_add;
		}

		function get_from()
		{
			return $this->from;
		}

		function set_from($from)
		{
			$this->from = $from;
		}

		function set_parametrs( $id, $ticket_id, $text, $attachment, $time_add, $from)
		{
			$this->set_id($id);
			$this->set_ticket_id($ticket_id);
			$this->set_text($text);
			$this->set_attachment($attachment);
			$this->set_time_add($time_add);
			$this->set_from($from);
		}

		function set_parametrs_from_request()
		{
			if ($_REQUEST['ticket_id'] != '')
				$this->set_ticket_id($_REQUEST['ticket_id']);
			if ($_REQUEST['text'] != '')
				$this->set_text($_REQUEST['text']);
			if ($_REQUEST['attachment'] != '')
				$this->set_attachment($_REQUEST['attachment']);
			if ($_REQUEST['time_add'] != '')
				$this->set_time_add($_REQUEST['time_add']);
			if ($_REQUEST['from'] != '')
				$this->set_from($_REQUEST['from']);
		}

		function clear_parametrs()
		{
			$this->set_id('');
			$this->set_ticket_id('');
			$this->set_text('');
			$this->set_attachment('');
			$this->set_time_add('');
			$this->set_from('');
		}

		function  load_ticket_message($id)
		{
			$ticket_message = db()->query_once('select * from ticket_message where id = "'.$id.'"');
			$this->set_parametrs( $ticket_message['id'], $ticket_message['ticket_id'], $ticket_message['text'], $ticket_message['attachment'], $ticket_message['time_add'], $ticket_message['from']);
		}

		function add_ticket_message()
		{
			db()->query_once('insert into ticket_message( `ticket_id`, `text`, `attachment`, `time_add`, `from`) values ( "'.$this->get_ticket_id().'", "'.db()->nomysqlinj($this->get_text()).'", "'.$this->get_attachment().'", NOW(), "'.$this->get_from().'")');
		}

		function update_ticket_message()
		{
			db()->query_once('update ticket_message set `ticket_id` = "'.$this->get_ticket_id().'", `text` = "'.$this->get_text().'", `attachment` = "'.$this->get_attachment().'", `from` = "'.$this->get_from().'" where id = "'.$this->get_id().'"');
		}

		function delete_ticket_message()
		{
			db()->query_once('delete from ticket_message where id = "'.$this->get_id().'"');
		}
	}
?>