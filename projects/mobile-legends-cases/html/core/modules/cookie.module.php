<?php
    function set_cookie($keys, $value = null, $expire = false, $path = false, $host = false) {
        if (!$expire) $expire = time() + get_setval('cookies_life_time');
        if (!$path) $path = '/';
        if (!$host) $host = get_host();
        if (is_array($keys)) {
            foreach ($keys as $key => $value) {
                setcookie($key, $value, $expire, $path, $host);
            }
            return true;
        }
        return setcookie($keys, $value, $expire, $path, $host);
    }

    function get_cookie($keys) {
        if (is_array($keys)) {
            $return = array();
            foreach ($keys as $key) {
                if (isset($_COOKIE[$key])) {
                    $return[$key] = $_COOKIE[$key];
                }
            }
            return count($return) > 0? $return : false;
        }
        return isset($_COOKIE[$keys])? $_COOKIE[$keys] : false;
    }

    function the_cookie($keys) {
        echo get_cookie($keys);
    }

    function clear_cookie($keys, $path = false, $host = false) {
        if (!$path) $path = '/';
        if (!$host) $host = get_host();
        if (is_array($keys)) {
            foreach ($keys as $key) {
                setcookie($key, null, time() - 1, $path, $host);
            }
            return true;
        }
        return setcookie($keys, null, time() - 1, $path, $host);
    }
?>