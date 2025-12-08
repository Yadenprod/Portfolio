<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

use App\Models\User;
use DB;
use Symfony\Component\HttpKernel\Exception\HttpException;

class BonusController extends Controller
{
    public function take(Request $request)
    {
        if(!in_array($request->type, ['daily'])) return;

        if(!$this->isGroupMember()) {
            return [
                'error' => true,
                'message' => 'Подпишитесь на группу VK'
            ];
        }

        if($this->user->balance >= 10) {
            return [
                'error' => true,
                'message' => 'Нельзя получить бонус, если ваш баланс более 10!'
            ];
        }

        if(\App\Models\Mine::where('status', 0)->where('user_id', $this->user->id)->first()) {
            return [
                'error' => true,
                'message' => 'Завершите игру в Mines'
            ];
        }

        try {
            DB::beginTransaction();

            $user = User::lockForUpdate()->where('id', $this->user->id)->first();
            $remaining = null;

            switch($request->type) {
                case 'daily':
                    if($user->bonus_daily > time()) {
                        DB::rollback();
                        return [
                            'error' => true,
                            'message' => 'Бонус можно получить через ' . $this->remainingTime($user->bonus_daily - time())
                        ];
                    }
                    
                    $bonus = rand(
                        $this->config->daily_bonus_min, 
                        $this->config->daily_bonus_max
                    );

                    $user->balance += $bonus;
                    $user->bonus_daily = time() + 86400;
                    $user->save();

                    $remaining = $user->bonus_daily;
                break;
            }
            
            DB::commit();
        } catch(\Exception $e) {
            DB::rollback();
            return [
                'error' => true,
                'message' => $e->getMessage()
            ];
        }

        return [
            'balance' => $user->balance,
            'bonus' => $bonus,
            'type' => $request->type,
            'remaining' => $remaining
        ];
    }
}