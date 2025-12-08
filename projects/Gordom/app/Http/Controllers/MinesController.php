<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Redis;

use App\Models\User;
use App\Models\Mine;
use App\Models\Setting;
use App\Models\Profit;
use Auth;
use DB;

class MinesController extends Controller
{
    protected $profit;

    public function __construct()
    {
        parent::__construct();
        $this->profit = Profit::first();
    }

    protected $coef = [
        2 => [1.09,1.19,1.3,1.43,1.58,1.75,1.96,2.21,2.5,2.86,3.3,3.85,4.55,5.45,6.67,8.33,10.71,14.29,20,30,50,100,300],
        3 => [1.14,1.3,1.49,1.73,2.02,2.37,2.82,3.38,4.11,5.05,6.32,8.04,10.45,13.94,19.17,27.38,41.07,65.71,115,230,575,2300],
        4 => [1.19,1.43,1.73,2.11,2.61,3.26,4.13,5.32,6.95,9.27,12.64,17.69,25.56,38.33,60.24,100.4,180.71,361.43,843.33,2530,12650],
        5 => [1.25,1.58,2.02,2.61,3.43,4.57,6.2,8.59,12.16,17.69,26.54,41.28,67.08,115,210.83,421.67,948.75,2530,8855,53130],
        6 => [1.32,1.75,2.37,3.26,4.57,6.53,9.54,14.31,22.12,35.38,58.97,103.21,191.67,383.33,843.33,2108.33],
        7 => [1.39,1.96,2.82,4.13,6.2,9.54,15.1,24.72,42.02,74.7,140.06,280.13,606.94,1456.67,4005.83,13352.78],
        8 => [1.47,2.21,3.38,5.32,8.59,14.31,24.72,44.49,84.04,168.08,360.16,840.38,2185,6555,24035,120175,1081575],
        9 => [1.56,2.5,4.11,6.95,12.16,22.12,42.02,84.04,178.58,408.19,1020.47,2857.31,9286.25,37145,204297.5,2042975],
        10 => [1.67,2.86,5.05,9.27,17.69,35.38,74.7,168.08,408.19,1088.5,3265.49,11429.23,49526.67,297160,3268760],
        11 => [1.79,3.3,6.32,12.64,26.54,58.97,140.06,360.16,1020.47,3265.49,12245.6,57146.15,371450,4457400],
        12 => [1.92,3.85,8.04,17.69,41.28,103.21,280.13,840.38,2857.31,11429.23,57146.15,400023.08,5200300],
        13 => [2.08,4.55,10.45,25.56,67.08,191.67,606.94,2185,9286.25,49526.67,371450,5200300],
        14 => [2.27,5.45,13.94,38.33,115,383.33,1456.67,6555,37145,297160,4457400],
        15 => [2.5,6.67,19.17,60.24,210.83,843.33,4005.83,24035,204297.5,3268760],
        16 => [2.78,8.33,27.38,100.4,421.67,2108.33,13352.78,120175,2042975],
        17 => [3.13,10.71,41.07,180.71,948.75,6325,60087.5,1081575],
        18 => [3.57,14.29,65.71,361.43,2530,25300,480700],
        19 => [4.17,20,115,843.33,8855,177100],
        20 => [5,30,230,2530,53130],
        21 => [6.25,50,575,12650],
        22 => [8.33,100,2300],
        23 => [12.5,300],
        24 => [25]
    ];
    
    public function init()
    {
        $game = Mine::where('user_id', $this->user->id)->where('status', 0)->first();

        if(!$game) {
            return 0;
        }

        $grid = json_decode($game->grid, true);
        $totalWin = !$game->step
            ? 0
            : $game->amount * $this->coef[$game->bombs][$game->step - 1];
        
        return [
            'bombs' => $game->bombs,
            'amount' => $game->amount,
            'click' => $grid['click'],
            'total' => $totalWin
        ];
    }

    public function createGame(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'amount' => 'required|numeric|min:1',
            'bombs' => 'required|integer|min:2|max:25',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        if($this->user->ban) {
            return [
                'error' => true,
                'message' => 'Ваш аккаунт заблокирован'
            ];
        }

        try {
            DB::beginTransaction();

            $user = User::where('id', $this->user->id)->lockForUpdate()->first();
            $game = Mine::where('user_id', $this->user->id)->where('status', 0)->first();
    
            if($game) {
                DB::rollback();
                return [
                    'error' => true,
                    'message' => 'У вас есть активная игра'
                ];
            }

            if($request->amount > $user->balance) {
                DB::rollback();
                return [
                    'error' => true,
                    'message' => 'Недостаточно средств'
                ];
            }
            
            $user->decrement('balance', $request->amount);
            $user->decrement('wager', $request->amount);
    
            if($user->wager < 0) $user->update([
                'wager' => 0
            ]);

            Mine::create([
                'user_id' => $user->id,
                'amount'  => $request->amount,
                'bombs'   => $request->bombs,
                'grid'    => $this->generateGrid($request),
                'status'  => 0
            ]);

            if(Mine::where('status', 0)->where('user_id', $user->id)->count() >= 2) {
                DB::rollback();
                return [
                    'error' => true,
                    'message' => 'У вас есть активная игра'
                ];
            }
    
            DB::commit();
        } catch (\Exception $e) {
            DB::rollback();
            return [
                'error' => true,
                'message' => 'Подождите...'
            ];
        }

        return [
            'message' => 'Игра создана',
            'balance' => $user->balance
        ];
    }

    public function openPath(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'path' => 'required|integer|min:1|max:25',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        try {
            DB::beginTransaction();

            $game = Mine::where('user_id', $this->user->id)
                ->where('status', 0)
                ->sharedLock()
                ->first();
    
            if(!$game) {
                DB::rollback();
                return [
                    'error' => true,
                    'message' => 'У вас нет активной игры'
                ];
            }
    
            $isWin = false;
            $totalWin = 0;
    
            $grid = json_decode($game->grid, true);

            if(in_array($request->path, $grid['click'])) {
                DB::rollback();
                return [
                    'error' => true,
                    'message' => 'Вы уже нажимали на это поле'
                ];
            }
    
            $totalWin = $game->amount * $this->coef[$game->bombs][$game->step];
            
            if(
                $this->config->antiminus &&
                $game->amount * $this->coef[$game->bombs][$game->step] - $game->amount > $this->profit->bank_mines && 
                !in_array($request->path, $grid['bombs']) &&
                !$this->user->is_youtuber
            ) 
            {
                array_splice($grid['bombs'], -1, 1, $request->path);

                $game->grid = $grid;
                $game->save();
            }

            if(!in_array($request->path, $grid['bombs'])) {
                $isWin = true;
                $game->increment('step', 1);

                $grid['click'][] = $request->path;

                $game->grid = $grid;
                $game->save();
            }

            if(!$isWin) {
                $totalWin = $game->amount * $this->coef[$game->bombs][!$game->step ? $game->step : $game->step - 1];

                $game->update(['status' => 1]);
                $this->user->decrement('mines', $game->amount);
                
                if(!$this->user->is_youtuber) {
                    $this->profit->increment('bank_mines', $game->amount * ((100 - $this->profit->comission) / 100));
                    $this->profit->increment('earn_mines', $game->amount * ($this->profit->comission) / 100);
                }
            }

            $instWin = null;

            if($isWin && !isset($this->coef[$game->bombs][$game->step])) {
                $instWin = $this->take();
            }
    
            DB::commit();
        } catch (\Exception $e) {
            DB::rollback();
            return [
                'error' => true,
                'message' => $e->getMessage()
            ];
        }

        return [
            'total' => $totalWin,
            'continue' => $isWin,
            'bombs' => $isWin ? [] : $grid['bombs'],
            'step' => $game->step,
            'instwin' => $instWin
        ];
    }

    public function take()
    {
        DB::beginTransaction();

        $user = User::where('id', $this->user->id)->lockForUpdate()->first();
        $game = Mine::where('status', 0)->where('user_id', $this->user->id)->lockForUpdate()->first();

        if(!$game) {
            DB::rollback();
            return [
                'error' => true,
                'message' => 'У вас нет активной игры'
            ];
        }

        if($game->step == 0) {
            DB::rollback();
            return [
                'error' => true,
                'message' => 'Сделайте 1 ход'
            ];
        }

        $game->status = 1;
        $game->save();

        $totalWin = $game->amount * $this->coef[$game->bombs][$game->step - 1];

        $user->increment('balance', $totalWin);
        $user->increment('mines', $totalWin - $game->amount);

        DB::commit();

        $grid = json_decode($game->grid, true);

        Redis::publish('newGame', json_encode([
            'id' => $game->id,
            'type' => 'mines',
            'user' => [
                'username' => $user->username,
                'avatar' => $user->avatar,
            ],
            'amount' => $game->amount,
            'coeff' => round($totalWin / $game->amount, 2),
            'time' => date('H:i'),
            'result' => $totalWin
        ]));
        
        if(!$user->is_youtuber) {
            $this->profit->decrement('bank_mines', $totalWin - $game->amount);
        }

        return [
            'total' => $totalWin,
            'coeff' => round($totalWin / $game->amount, 2),
            'bombs' => $grid['bombs'],
            'balance' => $user->balance
        ];
    }

    public function generateGrid($data)
    {
        $bombs = range(1,25);
        shuffle($bombs);
        $bombs = array_slice($bombs, 0, $data->bombs);

        $grid = [
            'bombs' => $bombs,
            'click' => []
        ];

        return json_encode($grid, true);
    }
}