<?php

namespace App\Http\Controllers\Admin;

use App\Models\Game;
use App\Models\User;
use App\Models\Payment;
use App\Models\Profit;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use DB;

class IndexController extends Controller
{
    public function index()
    {
        $profitDice = Profit::query()->find(1)->earn_dice;
        $profitMines = Profit::query()->find(1)->earn_mines;
        $profitBubbles = Profit::query()->find(1)->earn_bubbles;

        return view('admin.index', compact('profitDice', 'profitMines', 'profitBubbles'));
    }
    public function getUserByMonth() {
        $chart = User::select(DB::raw('DATE_FORMAT(created_at, "%d.%m") as date'), DB::raw('count(*) as count'))
            ->where('is_bot', 0)
            ->whereMonth('created_at', '=', date('m'))
            ->groupBy('date')
            ->get();
        
        return $chart;
    }
    
    public function getDepsByMonth() {
        $chart = Payment::where('status', 1)->select(DB::raw('DATE_FORMAT(created_at, "%d.%m") as date'), DB::raw('SUM(sum) as sum'))
            ->whereMonth('created_at', '=', date('m'))
            ->groupBy('date')
            ->get();
        
        return $chart;
    }
    public function getMerchant() {
        $shop_id = $this->config->kassa_id;
        $api_key = $this->config->kassa_key;
        $data = [
            'shopId' => $shop_id,
            'nonce' => time(),
        ];
        ksort($data);
        $sign = hash_hmac('sha256', implode('|', $data), $api_key);
        $data['signature'] = $sign;
    
        $request = json_encode($data);
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://api.freekassa.ru/v1/balance');
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_FAILONERROR, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $request);
        $result = trim(curl_exec($ch));
        curl_close($ch);
    
        $res = json_decode($result, true);
        return (isset($res['type'])) ? ($res['type'] == 'error') ? $res['message'] : $res['balance'][0]['value'] : $res['msg'];
    }
}
