<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Hash;
use App\Models\User;
use App\Models\Setting;

class TelegramAuthController extends Controller
{
    public function me(Request $request)
    {
        $initData = $request->header('X-Telegram-Init-Data');
        
        if (!$initData) {
            return response()->json([
                'success' => false,
                'message' => 'Telegram init data required'
            ], 400);
        }

        // Валидация initData (в продакшене нужно проверять подпись)
        $data = $this->parseInitData($initData);
        
        if (!$data || !isset($data['user'])) {
            return response()->json([
                'success' => false,
                'message' => 'Invalid init data'
            ], 400);
        }

        $telegramUser = $data['user'];
        
        // Найти или создать пользователя
        $user = User::where('telegram_id', $telegramUser['id'])->first();
        
        if (!$user) {
            $user = User::create([
                'name' => $telegramUser['first_name'] . ' ' . ($telegramUser['last_name'] ?? ''),
                'username' => $telegramUser['username'] ?? 'user_' . $telegramUser['id'],
                'telegram_id' => $telegramUser['id'],
                'email' => 'telegram_' . $telegramUser['id'] . '@example.com',
                'password' => Hash::make(str_random(16)),
                'balance' => 1000, // Начальный баланс
            ]);
        }

        // Обработка реферального кода
        if (isset($data['start_param'])) {
            $this->handleReferral($user, $data['start_param']);
        }

        return response()->json([
            'success' => true,
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'username' => $user->username,
                'telegram_id' => $user->telegram_id,
            ],
            'balance' => $user->balance
        ]);
    }

    private function parseInitData($initData)
    {
        // Простая парсинг initData (в продакшене нужна валидация подписи)
        $pairs = explode('&', $initData);
        $data = [];
        
        foreach ($pairs as $pair) {
            $keyValue = explode('=', $pair, 2);
            if (count($keyValue) === 2) {
                $key = $keyValue[0];
                $value = urldecode($keyValue[1]);
                
                if ($key === 'user') {
                    $data['user'] = json_decode($value, true);
                } elseif ($key === 'start_param') {
                    $data['start_param'] = $value;
                }
            }
        }
        
        return $data;
    }

    private function handleReferral($user, $referralCode)
    {
        if ($user->referral_code) {
            return; // Уже есть реферал
        }

        $referrer = User::where('referral_code', $referralCode)->first();
        if ($referrer && $referrer->id !== $user->id) {
            $user->update([
                'referral_code' => $referralCode,
                'referred_by' => $referrer->id
            ]);
            
            // Бонус рефереру
            $referrer->increment('balance', 100);
        }
    }
}
