<?php
    function get_files($directory, $pattern = false, $sort = false) {
        $skip = array('.', '..');
        $files = scandir($directory);
        if ($sort && function_exists($sort)) {
            usort($files, $sort);
        }
        $result = array();
        foreach ($files as $file) {
            if (!in_array($file, $skip) && (!$pattern || preg_match('#'.$pattern.'#', $file))) {
                array_push($result, $file);
            }
        }
        return $result;
    }
?>