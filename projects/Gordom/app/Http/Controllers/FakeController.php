<?php

namespace App\Http\Controllers;

use App\Models\Game;
use App\Models\User;
use App\Models\Mine as Mines;

use App\Helpers\Mine;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redis;

class FakeController extends Controller
{
    private $mine;

    public function __construct(Mine $mine)
    {
        parent::__construct();
        $this->mine = $mine;
    }

    public function fake()
    {
        $bot = User::query()->where('is_bot', 1)->inRandomOrder()->first();

        if (!$bot) {
            return 'bot not found';
        }

        $rnd = mt_rand(0, 1);

        if ($rnd === 0) {
            $this->createDiceGame($bot);
        } else {
            $this->createRandomMines($bot);
        }

        return 'ok';
    }

    private function createRandomMines($bot)
    {
        $bet = mt_rand(1, 50);
        $bombs = mt_rand(2, 24); // количество бомб
        $bombsPosition = $this->mine->generateBombs($bombs); // позиция бомб на поле

        $usedPosition = [];
        $win = -1;
        $coef = 0;

        while($win == -1) {
            $path = mt_rand(1, 25);
            
            if (count($usedPosition) > 0) {
                $taked = mt_rand(0, 1);

                if ($taked) {
                    $win = 1;
                }
            }

            if(!in_array($path, $usedPosition)) { // нажимал ли бот на эту клетку
                
                $usedPosition[] = $path;
                if(in_array($path, $bombsPosition)) { // бот проиграл
                    $win = 0;
                }

                if(25 - count($usedPosition) == $bombs) {
                    $win = 1;
                }
            }
        }

        if($win) {
            $coef = $this->mine->coef[$bombs][count($usedPosition) - 1];
        }

        $totalWin = $bet * $coef;

        $game = Mines::create([
            'user_id' => $bot->id,
            'amount'  => $bet,
            'bombs'   => $bombs,
            'grid'    => $this->mine->generateBotGrid($bombsPosition, $usedPosition),
            'step'    => count($usedPosition),
            'status'  => 1,
            'fake'    => 1
        ]);

        Redis::publish('newGame', json_encode([
            'id' => $game->id,
            'type' => 'mines',
            'user' => [
                'username' => $bot->username,
                'avatar' => User::inRandomOrder()->where('avatar', '!=', '')->first()->avatar,
            ],
            'amount' => $bet,
            'coeff' => round($totalWin / $bet, 2),
            'result' => $totalWin,
            'time' => date('H:i')
        ]));
    }

    private function createDiceGame($bot)
    {
        $type = ['min', 'middle', 'max'][rand(0, 2)];
        
        $random = rand(0, 999999);
        $chance = rand(100, 9500) / 100;
        $bet = rand(100, 10000) / 100;

        $min = round(($chance / 100) * 999999, 0);
        $middle['min'] = round((100 - $chance) * 10000 / 2, 0);
        $middle['max'] = round((100 - $chance) * 10000 / 2, 0) + round(($chance / 100) * 999999, 0);
        $max = 999999 - round(($chance / 100) * 999999, 0);

        $win = round((100 / $chance) * $bet, 2);
        $isWin = false;

        switch($type) {
            case 'min':
                if($random <= $min) $isWin = true;
            break;
            case 'middle':
                if($random >= $middle['min'] && $random <= $middle['max']) $isWin = true;
            break;
            case 'max':
                if($random >= $max) $isWin = true;
            break;
        }

        $game = Game::create([
            'user_id' => $bot->id,
            'game' => 'dice',
            'bet' => $bet,
            'chance' => $chance,
            'win' => $isWin ? $win : 0,
            'type' => $isWin ? 'win' : 'lose',
            'fake' => 1
        ]);

        Redis::publish('newGame', json_encode([
            'id' => $game->id,
            'type' => 'dice',
            'user' => [
                'username' => $bot->username,
                'avatar' => User::inRandomOrder()->where('avatar', '!=', '')->first()->avatar,
            ],
            'amount' => $bet,
            'coeff' => round($win / $bet, 2),
            'result' => $isWin ? $win : 0,
            'time' => date('H:i')
        ]));
    }
}
