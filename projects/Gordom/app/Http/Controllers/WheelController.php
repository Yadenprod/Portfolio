<?php

namespace App\Http\Controllers;

use App\Http\Requests;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Redis;

use App\Models\User;
use App\Models\Wheel;
use App\Models\WheelBets;
use App\Models\Setting;
use DB;

use Cache;

class WheelController extends Controller
{
    public function __construct()
    {
        parent::__construct();

        $this->positions = [
            'black'  => [700, 724, 748, 772, 804, 828],
            'green'  => [836, 860, 916, 940],
            'orange' => [1356, 1340],
            'red'    => [1244, 1260],
            'pink'   => [796, 956, 1092],
            'violet' => [1100]
        ];
        $this->redis = Redis::connection();
    }

    public function init()
    {
        $bets = $this->parseBets();
        $last = $this->parseHistory();

        return [
            'bets' => $bets,
            'history' => $last
        ];
    }

    public function bet(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'amount' => 'required|numeric|min:1',
            'color' => [
                Rule::in(['black', 'green', 'orange', 'red', 'pink', 'violet']),
                'required'
            ]
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        $amount = $request->amount;
        $color = $request->color;

        DB::beginTransaction();

        $game = Wheel::lockForUpdate()->where('status', 1)->first();
        $user = User::lockForUpdate()->where('id', $this->user->id)->first();

        if($amount > $user->balance) {
            return [
                'error' => true,
                'message' => 'Недостаточно средств'
            ];
        }

        if(!$game) {
            return [
                'error' => true,
                'message' => 'Дождитесь начала игры'
            ];
        }

        if(WheelBets::where('game_id', $game->id)->where('user_id', $user->id)->count() >= 5) {
            return [
                'error' => true,
                'message' => 'Достигнут лимит по ставкам'
            ];
        }

        $wheelBet = new WheelBets();
        $wheelBet->game_id = $game->id;
        $wheelBet->user_id = $user->id;
        $wheelBet->color   = $color;
        $wheelBet->amount  = $amount;
        $wheelBet->save();

        $user->balance -= $amount;
        $user->save();

        DB::commit();

        $this->redis->publish('wheelBets', json_encode([
            'bets' => $this->parseBets()
        ]));

        return [
            'balance' => $user->balance
        ];
    }

    public function getSlider()
    {   
        $settings = Setting::orderBy('id', 'desc')->first();
        $values = [
            'black' => 2, 
            'green' => 3, 
            'orange' => 5, 
            'red' => 10,
            'pink' => 20,
            'violet' => 100
        ];
        $color = $this->getRandomColor();

        DB::beginTransaction();

        $game = Wheel::where('status', 1)->first();
        $bets = WheelBets::where('game_id', $game->id)->where('color', $color)->get();

        foreach($bets as $bet)
        {
            $profit = $bet->amount * $values[$color];
            $user = User::where('id', $bet->user_id)->first();

            $user->balance += $profit;
            $user->save(); 
        }

        $position = $this->findPosition($color);
        $game->status = 2;
        $game->winner_color = $color;
        $game->winner_position = $position;
        $game->save();

        Cache::put('wheelResult-' . $game->id, '', 11);
        DB::commit();

        return [
            'color' => $color,
            'position' => $position
        ];
    }

    public function createGame()
    {
        $game = Wheel::where('status', 1)->first();
        if($game) return null;

        $wheel = new Wheel();
        $wheel->status = 1;
        $wheel->save();
        
        return 200;
    }

    public function getStatus()
    {
        $color = null;
        $bets = [];
        $game = Wheel::orderBy('id', 'desc')->first();

        if(!$game) {
            $this->createGame();
            return ['status' => 1];
        }

        if($game->status == 1) {
            $bets = $this->parseBets();
        }

        if($game->status == 2) {
            $color = $game->winner_color;
        }

        return ['status' => $game->status, 'color' => $color, 'bets' => $bets];
    }

    private function parseHistory()
    {
        $history = Wheel::where('status', 2)
            ->orderBy('id', 'desc')
            ->limit(15)
            ->get();

        return $history;
    }

    private function parseBets()
    {
        $game = Wheel::where('status', 1)
            ->orWhere('status', 2)
            ->orderBy('id', 'desc')
            ->first();

        if(!$game) return null;

        $bets = WheelBets::where('wheel_bets.game_id', $game->id)
			->select(
				'wheel_bets.user_id', DB::raw('SUM(wheel_bets.amount) as sum'), 
				'users.id', 'users.username', 
				'users.avatar', 'wheel_bets.color'
			)
			->join('users', 'users.id', '=', 'wheel_bets.user_id')
			->groupBy('wheel_bets.user_id', 'wheel_bets.color')
			->orderBy('sum', 'desc')
			->get();
			
        return $bets;
    }

    private function findPosition($color)
    {
        $arr = $this->positions[$color];
        $position = $arr[array_rand($arr)];
        
        return $position;
    }

    private function getRandomColor()
    {
        $colors = [];

        for($i = 0; $i <= 60; $i++) $colors[] = 'black';
        for($i = 0; $i <= 15; $i++) $colors[] = 'green';
        for($i = 0; $i <= 9; $i++) $colors[] = 'orange';
        for($i = 0; $i <= 10; $i++) $colors[] = 'red';
        for($i = 0; $i <= 5; $i++) $colors[] = 'pink';
        for($i = 0; $i <= 1; $i++) $colors[] = 'violet';

        shuffle($colors);
        return $colors[array_rand($colors)];
    }
}