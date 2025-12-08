<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Setting;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redis;

class SettingsController extends Controller
{
    public function index()
    {
        return view('admin.settings.index');
    }

    public function save(Request $r)
    {
        if ($this->config->bot_timer !== $r->get('bot_timer')) {
            Redis::publish('setNewBotTimer', $r->get('bot_timer'));
        }

        Setting::query()->find(1)->update($r->all());
        return redirect()->back()->with('success', 'Настройки сохранены!');
    }
}
