<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Auth;

class UserController extends Controller
{
    public function init()
    {
        if(!$this->user) return;

        return [
            'user' => [
                'id' => $this->user->id,
                'login' => $this->user->username,
                'avatar' => $this->user->avatar,
                'balance' => $this->user->balance,
                'is_admin' => $this->user->is_admin,
                'is_moderator' => $this->user->is_moderator
            ]
        ];
    }

    public function updateBalance()
    {
        if(!$this->user) return null;

        return [
            'balance' => $this->user->balance
        ];
    }

    public function logout()
    {
        Auth::logout();
        return redirect('/');
    }
}
