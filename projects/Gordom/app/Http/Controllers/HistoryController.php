<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Models\GameHistory;

class HistoryController extends Controller
{
    public function index(Request $request)
    {
        $initData = $request->header('X-Telegram-Init-Data');
        $user = $this->getUserFromInitData($initData);
        
        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Unauthorized'
            ], 401);
        }

        $limit = $request->input('limit', 25);
        
        $history = GameHistory::where('user_id', $user->id)
            ->orderBy('created_at', 'desc')
            ->limit($limit)
            ->get()
            ->map(function ($item) {
                return [
                    'id' => $item->id,
                    'game' => $item->game,
                    'amount' => $item->amount,
                    'win' => $item->win,
                    'multiplier' => $item->multiplier,
                    'time' => $item->created_at->diffForHumans()
                ];
            });

        return response()->json([
            'success' => true,
            'items' => $history
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
