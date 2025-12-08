<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\GameHistory;

class GameController extends Controller
{
    public function diceBet(Request $request)
    {
        return $this->processBet($request, 'dice');
    }

    public function wheelBet(Request $request)
    {
        return $this->processBet($request, 'wheel');
    }

    public function minesBet(Request $request)
    {
        return $this->processBet($request, 'mines');
    }

    public function slotsBet(Request $request)
    {
        return $this->processBet($request, 'slots');
    }

    private function processBet(Request $request, $game)
    {
        $initData = $request->header('X-Telegram-Init-Data');
        $user = $this->getUserFromInitData($initData);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized'
            ], 401);
        }

        $amount = $request->input('amount');
        $chance = $request->input('chance', 50);
        
        if (!$amount || $amount < 1 || $amount > $user->balance) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid amount'
            ], 400);
        }

        // Списываем ставку
        $user->decrement('balance', $amount);

        // Генерируем результат
        $roll = rand(0, 99);
        $win = $roll < $chance;
        $multiplier = $win ? (100 / $chance) : 0;
        $winAmount = $win ? ($amount * $multiplier) : 0;

        if ($win) {
            $user->increment('balance', $winAmount);
        }

        // Записываем в историю
        GameHistory::create([
            'user_id' => $user->id,
            'game' => $game,
            'amount' => $amount,
            'win' => $win,
            'multiplier' => $multiplier,
            'result' => $roll,
            'chance' => $chance
        ]);

        return response()->json([
            'success' => true,
            'status' => $win,
            'number' => $roll,
            'balance_delta' => $win ? ($winAmount - $amount) : -$amount,
            'new_balance' => $user->fresh()->balance
        ]);
    }

    private function getUserFromInitData($initData)
    {
        if (!$initData) {
            return null;
        }

        $pairs = explode('&', $initData);
        $data = [];
        
        foreach ($pairs as $pair) {
            $keyValue = explode('=', $pair, 2);
            if (count($keyValue) === 2) {
                $key = $keyValue[0];
                $value = urldecode($keyValue[1]);
                
                if ($key === 'user') {
                    $data['user'] = json_decode($value, true);
                }
            }
        }
        
        if (!isset($data['user']['id'])) {
            return null;
        }

        return User::where('telegram_id', $data['user']['id'])->first();
    }
}
