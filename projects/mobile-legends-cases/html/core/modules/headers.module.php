<?php
    if (!function_exists('getallheaders'))  {
        function getallheaders()
        {
            if (!is_array($_SERVER)) {
                return array();
            }
    
            $headers = array();
            foreach ($_SERVER as $name => $value) {
                if (substr($name, 0, 5) == 'HTTP_') {
                    $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value;
                }
            }
            return $headers;
        }
    }

    function getheader($key) {
        $headers = getallheaders();
        return isset($headers[$key])? $headers[$key] : false;
    }

    function isheader($key) {
        $headers = getallheaders();
        return isset($headers[$key]);
    }

    function isheaders($keys = array()) {
        $isheader = true;
        foreach ($keys as $key) {
            if (!isheader($key)) {
                $isheader = false;
            }
        }
        return $isheader;
    }
?>