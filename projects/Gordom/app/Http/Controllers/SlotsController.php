<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Support\Facades\Redis;

use App\Models\User;
use App\Models\Slot;
use Auth;
use DB;

class SlotsController extends Controller
{
    public function init(Request $request)
    {
        $slots = Slot::orderBy('priority', 'desc')->where([
            [function ($query) use ($request) {
                if(($provider = $request->provider)) {
                    $query->where('provider', $provider)->get();
                }
                if(($search = $request->search)) {
                    $query->where('title', 'like', '%' .$search. '%')->get();
                }
            }]
        ])->where('active', 1)->paginate(15);

        return $slots;
    }

    public function loadGame(Request $request)
    {
        $slot = Slot::where('game_id', $request->id)->first();

        if(!$this->user) {
            return [
                'error' => true, 
                'message' => 'Авторизуйтесь'
            ];
        }

        if(!$slot) {
            return [
                'error' => true,
                'message' => 'Слот не найден'
            ];
        }

        $id = $slot->id;
        $title = $slot->title;

        $data = [
            "cmd"       => "openGame",
            "hall"      => $this->config->tbs_provider_id,
            "key"       => $this->config->tbs_provider_secret,
            "language"  => "ru",
            "continent" => "eur",
            "login"     => $this->user->unique_id,
            "cdnUrl"    => "https://cdn.lvslot.net/",
            "domain"    => 'https://' . $_SERVER['HTTP_HOST'],
            "exitUrl"   => 'https://' . $_SERVER['HTTP_HOST'] . '/slots',
            "demo"      => "0",
            "gameId"    => $slot->game_id
        ];

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://tbs2api.dark-a.com/API/openGame/');
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $output = curl_exec($ch);
        curl_close($ch);

        $output = json_decode($output, true);
        $link = $output['content']['game']['url'];

        User::where('id', $this->user->id)->update([
            'sessionId' => $output['content']['gameRes']['sessionId']
        ]);

        return [
            'url' => $link,
            'info' => $slot
        ];
    }

    public function parse()
    {
        if(!$this->user->is_admin) return 'access denied';

        $data = json_decode(file_get_contents(public_path() . "/slots.json"), true);
        $slots = $data['content']['gameList'];

        Slot::where('provider_type', 'TBS')->delete();

        foreach($slots as $slot) {
            Slot::create([
                'game_id'       => $slot['id'],
                'title'         => $slot['name'],
                'provider'      => $slot['label'],
                'provider_type' => 'TBS',
                'icon'          => $slot['img']
            ]);
        }

        return 'OK';
    }

    // callback

    public function callback(Request $request)
    {
        $cmd = $request->cmd;

        if($request->key != $this->config->tbs_provider_secret) return 'hacking attempt!';

        switch ($cmd) {
            case 'getBalance': 
                $data = $this->getBalance($request);
                return json_encode($data);
            break;

            case 'writeBet':
                $data = $this->writeBet($request);
                return json_encode($data);
            break;

            default: 
                die('Wrong cmd');
        }
    }

    private function writeBet($request)
    {
        $user = $this->findByLogin($request->login);

        $bet = $request->bet;
        $win = $request->win;

        if(!$user) {
            return [
                'status' => 'fail',
                'error'  => 'user_not_found'
            ];
        }
        
        if($user->balance < $bet) {
            return [
                'status' => 'fail',
                'error'  => 'fail_balance'
            ];
        }

        $user->increment('balance', $win - $bet);
        $user->decrement('wager', $bet);

        if($user->wager < 0) {
            $user->update(['wager' => 0]);
        }

        return [
            "status"      => "success",
            "error"       => "",
            "login"       => $user->unique_id,
            "balance"     => number_format($user->balance, 2, '.', ''),
            "currency"    => "RUB",
            "operationId" => "3234234"
        ];
    }

    private function getBalance($request)
    {
        $user = $this->findByLogin($request->login);

        return [
            "status"   => "success",
            "error"    => "",
            "login"    => $user->unique_id,
            "balance"  => number_format($user->balance, 2, '.', ''),
            "currency" => "RUB"            
        ];
    }

    private function findByLogin($login)
    {
        $user = User::where('unique_id', $login)->first();
        return $user;
    }
}