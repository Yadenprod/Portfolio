<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class ReferralController extends Controller
{
    public function stats(Request $request)
    {
        $initData = $request->header('X-Telegram-Init-Data');
        $user = $this->getUserFromInitData($initData);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized'
            ], 401);
        }

        // Генерируем реферальный код, если его нет
        if (!$user->referral_code) {
            $user->update([
                'referral_code' => 'ref' . $user->id . '_' . strtoupper(substr(md5($user->id), 0, 6))
            ]);
        }

        // Подсчитываем статистику
        $invited = User::where('referred_by', $user->id)->count();
        $earnings = User::where('referred_by', $user->id)->sum('balance') * 0.1; // 10% от баланса рефералов
        $pending = User::where('referred_by', $user->id)->where('balance', '>', 0)->count();

        return response()->json([
            'success' => true,
            'invited' => $invited,
            'earnings' => round($earnings, 2),
            'pending' => $pending,
            'referral_code' => $user->referral_code
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
