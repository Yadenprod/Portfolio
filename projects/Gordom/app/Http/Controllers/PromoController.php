<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\PromoCode;

class PromoController extends Controller
{
    public function activate(Request $request)
    {
        $initData = $request->header('X-Telegram-Init-Data');
        $user = $this->getUserFromInitData($initData);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized'
            ], 401);
        }

        $code = $request->input('code');
        
        if (!$code) {
            return response()->json([
                'success' => false,
                'message' => 'Promo code required'
            ], 400);
        }

        // Найти промокод
        $promoCode = PromoCode::where('code', $code)
            ->where('is_active', true)
            ->first();

        if (!$promoCode) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid promo code'
            ], 400);
        }

        // Проверить, не использовал ли пользователь уже этот промокод
        if ($user->usedPromoCodes()->where('promo_code_id', $promoCode->id)->exists()) {
            return response()->json([
                'success' => false,
                'message' => 'Promo code already used'
            ], 400);
        }

        // Начислить бонус
        $reward = $promoCode->reward;
        $user->increment('balance', $reward);
        
        // Отметить промокод как использованный
        $user->usedPromoCodes()->attach($promoCode->id);

        return response()->json([
            'success' => true,
            'reward' => $reward,
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