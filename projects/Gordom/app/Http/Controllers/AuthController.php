<?php

namespace App\Http\Controllers;

use Socialite;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Cookie;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Session;
use App\Models\User;

use DB;
use Auth;

class AuthController extends Controller {

    public function __construct() {
        parent::__construct();
    }

    public function redirect()
    {
        return Socialite::driver('vkontakte')->redirect();
    }

    public function handle()
    {
		try {
			$user = json_decode(json_encode(Socialite::driver('vkontakte')->stateless()->user()));
		} catch (\Exception $e) {
			return redirect('/')->withError('Попробуйте еще раз');
		}

        if(isset($user->returnUrl)) return redirect('/');
        return $this->createOrUpdateUser($user->user);
    }

    public function createOrUpdateUser($user) 
    {
        $candidate = User::where('vk_id', $user->id)->first();
        $username = $user->first_name . ' ' . $user->last_name;

        if(!$candidate) {
            @$ref = User::where('unique_id', Session::get('ref'))->first();
            $ref_use = 0;

            if($ref) {
                $ref_use = $ref->id;
            }

            $user = User::create([
                'unique_id' => \Str::random(8),
                'username' => $username,
                'avatar' => $user->photo_200,
                'vk_id' => $user->id,
                'created_ip' => $this->getIp(),
                'used_ip' => $this->getIp(),
                'referral_use' => $ref_use
            ]);

            Auth::login($user, true);
            return redirect('/');
        }

        $candidate->update([
            'used_ip' => $this->getIp()
        ]);

        Auth::login($candidate, true);
        return redirect('/');
    }
}
