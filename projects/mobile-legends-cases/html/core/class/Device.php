<?php
    class device {
		private $id = 0;
		private $ip = '';
		private $agent = '';

		function __construct($autoload = false) {
			if ($autoload) {
                $this->ip = getip();
                $this->agent = get_useragent();
            }
		}

		function get_ip() {
            return $this->ip;
        }

        function get_browser() {
            return getbrowser($this->agent);
        }

        function get_os() {
            return getos($this->agent);
        }

        function get_agent_compact() {
            return get_agent_compact($this->agent);
        }

        function get_hash() {
            return md5('DEVICE:'.iptoken($this->ip).':'.$this->agent);
        }
	}
?>