<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Redis;

use App\Models\User;
use App\Models\Game;
use App\Models\Setting;
use App\Models\Profit;
use Auth;
use DB;

class DiceController extends Controller
{
    public function bet(Request $request) : array {
        $validator = Validator::make($request->all(), [
            'amount' => 'required|numeric|min:1|max:1000',
            'chance' => 'required|numeric|min:1|max:95',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        $bet = $request->amount;
        $chance = $request->chance;
        $type = 'min';

        if($request->amount > $this->user->balance) {
            return [
                'error' => true,
                'message' => 'Недостаточно средств'
            ];
        }

        if($this->user->ban) {
            return [
                'error' => true,
                'message' => 'Ваш аккаунт заблокирован'
            ];
        }

        DB::beginTransaction();

        $this->user = User::where('id', $this->user->id)
            ->lockForUpdate()
            ->first();

        $this->user->decrement('balance', $bet);
        $this->user->decrement('wager', $bet);
        $this->user->decrement('dice', $bet);

        if($this->user->wager < 0) $this->user->update([
            'wager' => 0
        ]);

        $random = rand(0, 100);
        $min = round(($chance / 100) * 100, 0);

        $win = round((100 / $chance) * $bet, 2);
        $isWin = false;

        $setting = Setting::query()->find(1);
        $profit = Profit::query()->find(1);

        if($setting->antiminus == 1 && !$this->user->is_youtuber) {
            if($win - $bet > $profit->bank_dice) {
                $random = rand($chance + 1, 100);
            }
        }

        if($random <= $min) {
            $isWin = true;
        }

        $text = 'Выпало ' . $random;

        if($isWin) {
            $win = number_format($win, 2, '.', '');
            $text = 'Выигрыш ' . $win;
            $this->user->increment('balance', $win);
            $this->user->increment('dice', $win);

            if($setting->antiminus == 1 && !$this->user->is_youtuber) {
                $profit->update([
                    'bank_dice' => $profit->bank_dice - ($win - $bet),
                ]);
            }
        } else {
            if(!$this->user->is_youtuber) {
                $profit->update([
                    'bank_dice' => $profit->bank_dice + ($bet / 100) * (100 - $profit->comission),
                    'earn_dice' => $profit->earn_dice + ($bet / 100) * $profit->comission
                ]);
            }
        }

        $game = Game::create([
            'user_id' => $this->user->id,
            'game' => 'dice',
            'bet' => $bet,
            'chance' => $chance,
            'win' => $isWin ? $win : 0,
            'type' => $isWin ? 'win' : 'lose',
            'fake' => 0
        ]);

        DB::commit();

        Redis::publish('newGame', json_encode([
            'id' => $game->id,
            'type' => 'dice',
            'user' => [
                'username' => $this->user->username,
                'avatar' => $this->user->avatar,
            ],
            'amount' => $bet,
            'coeff' => round($win / $bet, 2),
            'result' => $isWin ? $win : 0,
            'time' => date('H:i')
        ]));

        return [
            'status' => $isWin,
            'text' => $text,
            'balance' => $this->user->balance,
            'number' => $random
        ];
    }
}
