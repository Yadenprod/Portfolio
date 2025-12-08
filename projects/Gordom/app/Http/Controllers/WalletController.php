<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\Transaction;

class WalletController extends Controller
{
    public function deposit(Request $request)
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
        
        if (!$amount || $amount < 10 || $amount > 50000) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid amount'
            ], 400);
        }

        // В реальном приложении здесь была бы интеграция с платежной системой
        // Пока просто увеличиваем баланс
        $user->increment('balance', $amount);
        
        // Записываем транзакцию
        Transaction::create([
            'user_id' => $user->id,
            'type' => 'deposit',
            'amount' => $amount,
            'status' => 'completed',
            'description' => 'Пополнение баланса'
        ]);

        return response()->json([
            'success' => true,
            'balance_delta' => $amount,
            'new_balance' => $user->fresh()->balance
        ]);
    }

    public function withdraw(Request $request)
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
        
        if (!$amount || $amount < 100 || $amount > $user->balance) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid amount'
            ], 400);
        }

        // В реальном приложении здесь была бы интеграция с платежной системой
        // Пока просто уменьшаем баланс
        $user->decrement('balance', $amount);
        
        // Записываем транзакцию
        Transaction::create([
            'user_id' => $user->id,
            'type' => 'withdraw',
            'amount' => $amount,
            'status' => 'pending',
            'description' => 'Заявка на вывод средств'
        ]);

        return response()->json([
            'success' => true,
            'balance_delta' => -$amount,
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
