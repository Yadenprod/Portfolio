<?php

namespace App\Http\Controllers;

use Illuminate\Foundation\Auth\Access\AuthorizesRequests;
use Illuminate\Foundation\Bus\DispatchesJobs;
use Illuminate\Foundation\Validation\ValidatesRequests;
use Illuminate\Routing\Controller as BaseController;

use App\Models\Setting;
use Auth;

class Controller extends BaseController
{
    public function __construct()
    {
        date_default_timezone_set('Europe/Moscow');

        $this->config = Setting::query()->find(1);
        
        view()->share('settings', $this->config);

        $this->middleware(function ($request, $next) {
            $this->user = Auth::User();
            view()->share('u', $this->user);
            return $next($request);
        });
    }

    public function curl($url) 
    {
		$ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        $res = curl_exec($ch);
        curl_close($ch);
        return json_decode($res, true);
	}

    public function getIp() {
        if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } elseif(!empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
            $ip = $_SERVER['HTTP_CF_CONNECTING_IP'];
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }

        return $ip;
    }

    public function getWord($type, $value, $words = null, $show = true)
    {
        if($type == 'hour') $words = ['час', 'часа', 'часов'];
        if($type == 'min') $words = ['минуту', 'минуты', 'минут'];
        if($type == 'sec') $words = ['секунду', 'секунды', 'секунд'];

        $num = $value % 100;
        if ($num > 19) { 
            $num = $num % 10; 
        }
        
        $out = ($show) ?  $value . ' ' : '';
        switch ($num) {
            case 1:  $out .= $words[0]; break;
            case 2: 
            case 3: 
            case 4:  $out .= $words[1]; break;
            default: $out .= $words[2]; break;
        }
        
        return $out;
    }

    public function remainingTime($ss)
    {
        $sec = $ss%60;
        $min = floor(($ss%3600)/60);
        $hour = floor(($ss%86400)/3600);

        if($hour) {
            return $this->getWord('hour', $hour);
        }

        if($min) {
            return $this->getWord('min', $min);
        }

        if($sec) {
            return $this->getWord('sec', $sec);
        }
    }

    public function isGroupMember()
    {
        $data = [
            'group_id'     => $this->config->vk_id,
            'user_id'      => $this->user->vk_id,
            'access_token' => $this->config->vk_token,
            'v'            => 5.131
        ];
        $response = $this->curl('https://api.vk.com/method/groups.isMember?' . http_build_query($data));

        if(isset($response['error'])) return false;
        if(!$response['response']) return false;

        return true;
    }
}
