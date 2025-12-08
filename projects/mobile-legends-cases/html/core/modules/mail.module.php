<?php
	function send_email($settings) {
		if (isset($settings['to'])) {
			$mail = new PHPMailer(); 
			$mail->CharSet = 'UTF-8'; 
			$mail->From = isset($settings['from'])? $settings['from'] : 'admin@'.get_setval('site_url');      
			$mail->FromName = isset($settings['name'])? $settings['name'] : 'admin';   
			$mail->AddAddress($settings['to'], ''); 
			$mail->IsHTML(true);  
			$mail->Subject = isset($settings['subject'])? $settings['subject'] : 'No subject'; 
			$mail->Body = isset($settings['text'])? $settings['text'] : ''; 
			$mail->Send();
			return true;
		} else {
			return false;
		}
	}
?>